import pika
import json
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import time

# Загрузка и обучение модели
df = pd.read_csv('/app/data/housing.csv')
X = df.drop('PRICE', axis=1).values
y = df['PRICE'].values

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(f"Model trained. Score: {model.score(X_test, y_test):.3f}")

# Подключение к RabbitMQ с повторными попытками
def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            
            # ОБЯЗАТЕЛЬНО создаем обе очереди!
            channel.queue_declare(queue='features_queue')
            channel.queue_declare(queue='y_pred_queue')  # <-- ЭТУ очередь создает model
            
            print("✓ Connected to RabbitMQ and created queues")
            return connection, channel
        except Exception as e:
            print(f"Waiting for RabbitMQ... ({e})")
            time.sleep(5)

connection, channel = connect_to_rabbitmq()

def callback(ch, method, properties, body):
    data = json.loads(body)
    
    # Получение признаков
    features = np.array(data['features']).reshape(1, -1)
    
    # Предсказание
    prediction = model.predict(features)[0]
    
    # Добавление случайного шума для реалистичности
    noise = np.random.normal(0, prediction * 0.1)  # 10% шума
    prediction += noise
    
    # Подготовка ответа
    response = {
        'id': data['id'],
        'body': float(prediction)
    }
    
    # Отправка предсказания
    channel.basic_publish(
        exchange='',
        routing_key='y_pred_queue',
        body=json.dumps(response)
    )
    
    print(f"Prediction made: ID={data['id']}, Pred=${prediction:,.0f}")

# Подписка на очередь признаков
channel.basic_consume(
    queue='features_queue',
    on_message_callback=callback,
    auto_ack=True
)

print("Model service started. Waiting for messages...")
channel.start_consuming()
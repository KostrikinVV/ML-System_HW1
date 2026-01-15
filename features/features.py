import pika
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
import random

# Загрузка данных
df = pd.read_csv('/app/data/housing.csv')
X = df.drop('PRICE', axis=1).values
y = df['PRICE'].values

# Подключение к RabbitMQ с повторными попытками
def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            
            # Создаем очереди
            channel.queue_declare(queue='features_queue')
            channel.queue_declare(queue='y_true_queue')
            
            print("✓ Connected to RabbitMQ")
            return connection, channel
        except Exception as e:
            print(f"Waiting for RabbitMQ... ({e})")
            time.sleep(5)

connection, channel = connect_to_rabbitmq()

print("Features service started. Sending data...")

while True:
    # Случайный выбор строки
    idx = random.randint(0, len(X) - 1)
    
    # Генерация ID
    message_id = datetime.timestamp(datetime.now())
    
    # Подготовка сообщений
    features_msg = {
        'id': message_id,
        'features': X[idx].tolist(),
        'feature_names': df.drop('PRICE', axis=1).columns.tolist()
    }
    
    y_true_msg = {
        'id': message_id,
        'body': float(y[idx])
    }
    
    # Отправка в очереди
    channel.basic_publish(
        exchange='',
        routing_key='features_queue',
        body=json.dumps(features_msg)
    )
    
    channel.basic_publish(
        exchange='',
        routing_key='y_true_queue',
        body=json.dumps(y_true_msg)
    )
    
    print(f"Sent: ID={message_id}, Price=${y[idx]:,.0f}")
    
    # Задержка
    time.sleep(5)
import pika
import json
import random
import time
from datetime import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Объявление очередей
channel.queue_declare(queue='features_queue')
channel.queue_declare(queue='y_true_queue')

print("Отправка тестовых сообщений...")

for i in range(100):
    message_id = datetime.timestamp(datetime.now())
    
    # Тестовые признаки
    features_msg = {
        'id': message_id,
        'features': [
            random.uniform(0.5, 15.0),  # MedInc
            random.randint(1, 52),      # HouseAge
            random.uniform(0.8, 10.0),  # AveRooms
            random.uniform(0.5, 5.0),   # AveBedrms
            random.randint(1, 3500),    # Population
            random.uniform(0.8, 10.0),  # AveOccup
            random.uniform(32.5, 42.0), # Latitude
            random.uniform(-124.3, -114.1)  # Longitude
        ],
        'feature_names': ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 
                         'Population', 'AveOccup', 'Latitude', 'Longitude']
    }
    
    # Тестовый истинный ответ
    y_true_msg = {
        'id': message_id,
        'body': random.uniform(50000, 500000)
    }
    
    # Отправка
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
    
    print(f"Отправлено сообщение {i+1}: ID={message_id}")
    time.sleep(1)

connection.close()
print("Готово!")
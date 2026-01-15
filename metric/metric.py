import pika
import json
import csv
import os
from collections import defaultdict
import time

# Создание папки logs если не существует
os.makedirs('/app/logs', exist_ok=True)

# Инициализация CSV файла
csv_file = '/app/logs/metric_log.csv'
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'y_true', 'y_pred', 'absolute_error'])

# Буфер для хранения данных
buffer = defaultdict(lambda: {'y_true': None, 'y_pred': None})

def write_to_csv(row_data):
    """Запись строки в CSV файл"""
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row_data)
    print(f"Logged: {row_data}")

def process_message(ch, method, properties, body, queue_type):
    data = json.loads(body)
    msg_id = data['id']
    
    # Добавление в буфер
    buffer[msg_id][queue_type] = data['body']
    
    # Проверка наличия обеих величин
    if buffer[msg_id]['y_true'] is not None and buffer[msg_id]['y_pred'] is not None:
        y_true = buffer[msg_id]['y_true']
        y_pred = buffer[msg_id]['y_pred']
        
        # Вычисление ошибок
        absolute_error = abs(y_true - y_pred)
        
        # Запись в CSV
        write_to_csv([
            msg_id,
            round(y_true, 2),
            round(y_pred, 2),
            round(absolute_error, 2)
        ])
        
        # Удаление из буфера
        del buffer[msg_id]

def callback_y_true(ch, method, properties, body):
    process_message(ch, method, properties, body, 'y_true')

def callback_y_pred(ch, method, properties, body):
    process_message(ch, method, properties, body, 'y_pred')

# Подключение к RabbitMQ с повторными попытками
def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            
            # Проверяем существование очередей
            try:
                channel.queue_declare(queue='y_true_queue', passive=True)
                channel.queue_declare(queue='y_pred_queue', passive=True)
                print("✓ Queues exist")
            except pika.exceptions.ChannelClosedByBroker:
                print("Queues don't exist yet, waiting...")
                time.sleep(5)
                continue
            
            return connection, channel
        except Exception as e:
            print(f"Waiting for RabbitMQ... ({e})")
            time.sleep(5)

connection, channel = connect_to_rabbitmq()

# Подписка на очереди
channel.basic_consume(
    queue='y_true_queue',
    on_message_callback=callback_y_true,
    auto_ack=True
)

channel.basic_consume(
    queue='y_pred_queue',
    on_message_callback=callback_y_pred,
    auto_ack=True
)

print("Metric service started. Waiting for messages...")
channel.start_consuming()
# producer/producer.py
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# --- Connect to Kafka ---
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = 'stock_prices'

STOCKS = ['RELIANCE', 'TCS', 'INFOSYS', 'WIPRO', 'HDFC']

def generate_stock_data(symbol):
    return {
        'symbol': symbol,
        'price': round(random.uniform(500, 5000), 2),
        'volume': random.randint(100, 10000),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

print("Producer started. Sending stock data to Kafka...")

while True:
    for symbol in STOCKS:
        data = generate_stock_data(symbol)
        producer.send(TOPIC_NAME, value=data)
        print(f"Sent: {data}")
    
    time.sleep(2)   # every 2 seconds new data bhejo
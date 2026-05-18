# consumer/consumer.py
import json
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text
from datetime import datetime

DB_URL = "mysql+pymysql://root:root@localhost/stock_streaming"

engine = create_engine(DB_URL)

# --- Create table if not exists ---
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            symbol      VARCHAR(20)    NOT NULL,
            price       DECIMAL(10,2)  NOT NULL,
            volume      INT            NOT NULL,
            timestamp   DATETIME       NOT NULL
        )
    """))
    conn.commit()
print("Database table ready.")

# --- Connect to Kafka topic ---
consumer = KafkaConsumer(
    'stock_prices',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest',      # sirf naye messages lo
    group_id='stock_consumer_group'
)

print("Consumer started. Listening to Kafka topic 'stock_prices'...")

for message in consumer:
    data = message.value

    # --- Insert into MySQL ---
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO stock_prices (symbol, price, volume, timestamp)
            VALUES (:symbol, :price, :volume, :timestamp)
        """), {
            'symbol':    data['symbol'],
            'price':     data['price'],
            'volume':    data['volume'],
            'timestamp': datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        })
        conn.commit()

    print(f"Saved to DB: {data['symbol']} | Price: {data['price']} | Volume: {data['volume']}")
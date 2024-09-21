from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(bootstrap_servers='localhost:29092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_transaction():
    transaction = {
        "transaction_id": str(random.randint(1000, 9999)),
        "account_id": str(random.randint(1, 100)),
        "transaction_amount": random.uniform(1, 20000),
        "transaction_type": random.choice(["purchase", "withdrawal"]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return transaction

while True:
    transaction = generate_transaction()
    producer.send('transactions', transaction)
    print(f"Produced: {transaction}")
    time.sleep(10)

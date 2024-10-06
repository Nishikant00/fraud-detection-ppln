import csv
import json
import time
import random
import gzip
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_transaction_amounts_from_gzip(file_path):
    with gzip.open(file_path, mode='rt') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield float(row["amt"])

def generate_transaction(amount):
    transaction = {
        "transaction_id": str(random.randint(1000, 9999)),
        "account_id": str(random.randint(1, 100)),
        "transaction_amount": amount, 
        "transaction_type": random.choice(["purchase", "withdrawal"]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return transaction

csv_file_path = 'fraudTest.csv.gz'

for amount in read_transaction_amounts_from_gzip(csv_file_path):
    transaction = generate_transaction(amount)
    producer.send('transactions', transaction)
    print(f"Produced: {transaction}")

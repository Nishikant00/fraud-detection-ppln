from kafka import KafkaConsumer
import json
import psycopg2
from datetime import datetime, timedelta

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = psycopg2.connect(
    dbname="fraud_db", 
    user="user", 
    password="root", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS fraud_transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(255),
    account_id VARCHAR(255),
    transaction_amount NUMERIC,
    transaction_type VARCHAR(50),
    timestamp TIMESTAMP,
    fraud_reason VARCHAR(255)
);
''')
conn.commit()

LARGE_TRANSACTION_AMOUNT = 15000  # A transaction amount above this value is suspicious
FREQUENT_TRANSACTIONS_WINDOW = 5  # 5 minutes window for transaction frequency checks
TRANSACTION_LIMIT_IN_WINDOW = 3  # More than 3 transactions in a 5-minute window

recent_transactions = {}

def is_large_transaction(transaction):
    """Flag transaction as fraudulent if amount exceeds threshold."""
    return transaction['transaction_amount'] > LARGE_TRANSACTION_AMOUNT

def is_frequent_transactions(transaction):
    """Flag accounts making too many transactions in a short period."""
    account_id = transaction['account_id']
    current_time = datetime.strptime(transaction['timestamp'], "%Y-%m-%d %H:%M:%S")

    if account_id not in recent_transactions:
        recent_transactions[account_id] = []

    recent_transactions[account_id].append(current_time)

    recent_transactions[account_id] = [
        tx_time for tx_time in recent_transactions[account_id]
        if current_time - tx_time <= timedelta(minutes=FREQUENT_TRANSACTIONS_WINDOW)
    ]

    return len(recent_transactions[account_id]) > TRANSACTION_LIMIT_IN_WINDOW

def is_suspicious_withdrawals(transaction):
    """Flag suspicious withdrawals, e.g., multiple large withdrawals."""
    return transaction['transaction_type'] == "withdrawal" and transaction['transaction_amount'] > 10000

def detect_fraud(transaction):
    """Main fraud detection logic."""
    fraud_reasons = []

    if is_large_transaction(transaction):
        fraud_reasons.append(f"Large transaction over ${LARGE_TRANSACTION_AMOUNT}")

    if is_frequent_transactions(transaction):
        fraud_reasons.append(f"Too many transactions within {FREQUENT_TRANSACTIONS_WINDOW} minutes")

    if is_suspicious_withdrawals(transaction):
        fraud_reasons.append("Suspicious large withdrawal")

    return fraud_reasons

def save_fraudulent_transaction(transaction, reasons):
    """Insert fraudulent transaction into the database."""
    cur.execute('''
        INSERT INTO fraud_transactions (transaction_id, account_id, transaction_amount, transaction_type, timestamp, fraud_reason)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (
        transaction['transaction_id'],
        transaction['account_id'],
        transaction['transaction_amount'],
        transaction['transaction_type'],
        transaction['timestamp'],
        ", ".join(reasons) 
    ))
    conn.commit()

for message in consumer:
    transaction = message.value
    print(f"Received: {transaction}")
    
    fraud_reasons = detect_fraud(transaction)

    if fraud_reasons:
        print(f"Fraud detected: {transaction}")
        save_fraudulent_transaction(transaction, fraud_reasons)

cur.close()
conn.close()

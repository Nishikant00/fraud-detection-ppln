# Fraud Detection System

This project uses Kafka for streaming transactions, a fraud detection consumer to process suspicious transactions, and PostgreSQL to store detected fraudulent transactions.

## Features:
- Kafka Producer generates random transactions.
- Kafka Consumer detects suspicious transactions based on predefined rules.
- Fraudulent transactions are stored in a PostgreSQL database.
  
---

### Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Python 3.7+](https://www.python.org/downloads/)
- [Kafka Python](https://kafka-python.readthedocs.io/en/master/) library
- [PostgreSQL](https://www.postgresql.org/download/)

STEPS TO RUN
# step 1
cd kafka_only_new

docker-compose up -d
# step 2
- For Linux/macOS
python3 -m venv fraud-detection-env
source fraud-detection-env/bin/activate

- For Windows
python -m venv fraud-detection-env
fraud-detection-env\Scripts\activate

# step 3
pip install -r requirements.txt

Make sure step 4,5,6 are in seperate terminals

# step 4
python producer.py

# step 5
python fraud_consumer.py

# step 6
docker exec -it kafka_only_new-postgres-1 psql -U user -d fraud_db

```




# Fraud Detection Project Setup

This README documents the commands executed to set up the Fraud Detection project using Kafka and PostgreSQL.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.x installed
- Python virtual environment (`venv`) module

## Clone the Repository

```bash
git clone https://github.com/Nishikant00/fraud-detection-ppln.git
cd fraud-detection-ppln/kafka_only_new
```

## Docker Setup

### Step 1: Start Docker Containers

Run the following command to start the necessary services:

```bash
docker-compose up -d
```

### Step 2: Verify Running Containers

Check the status of the running containers:

```bash
docker ps
```

## Python Environment Setup

### Step 3: Create a Virtual Environment

Create and activate a Python virtual environment:

```bash
python3 -m venv fraud-detection-env
source fraud-detection-env/bin/activate  # For Linux/macOS
# For Windows: fraud-detection-env\Scripts\activate
```

### Step 4: Install Required Packages

Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Application

### Step 5: Start the Producer

Open a new terminal and run the producer:

```bash
python kafka_producer.py
```

### Step 6: Start the Consumer

Open another terminal and run the consumer:

```bash
python kafka_consumer.py
```

### Step 7: Access the PostgreSQL Database

Run the following command to access the PostgreSQL database:

```bash
docker exec -it kafka_only_new_postgres_1 psql -U user -d fraud_db
```

### Step 8: Query the Database

After accessing the database, you can run queries, such as:

```sql
SELECT * FROM fraud_transactions;
```

## Stopping the Services

When done, you can stop the services with:

```bash
docker stop $(docker ps -q)
```

## Notes

- Ensure that the required ports are available before starting the Docker containers.
- Modify any configurations as necessary in the `docker-compose.yml` or other files as per your requirements.

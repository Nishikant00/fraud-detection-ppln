FROM bitnami/spark:latest

RUN pip install pyspark==3.5.2 kafka-python  

COPY fraud-detection.py /app/fraud-detection.py
WORKDIR /app

CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2", "fraud-detection.py"]

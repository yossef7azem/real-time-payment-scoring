import pandas as pd
import json
from kafka import KafkaProducer

#intialize the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# function to Read the CSV file and produce dictionary row data 
def read_and_produce(csv_file, topic):
    data = pd.read_csv(csv_file)

    print(f"Loaded {len(data)} rows from {csv_file}")
    print(data.head())

    # Send each row to Kafka
    for _, row in data.iterrows():
        row_dict = row.to_dict()  
        producer.send(topic, value=row_dict)
        print(f"Produced: {row_dict}")
    
    # Ensure all messages are sent
    producer.flush()
    print("Finished producing messages.")


if __name__ == "__main__":
    topic_name = "credit_scoring" # I creted a topic with this name in my Kafka cluster containg 3 partitions
    csv_file = "C:\Users\Yossef Hazem\real-time-payment-scoring\Data\testing_features_sc.csv"  
    read_and_produce(csv_file, topic_name)

import pandas as pd
import json
from kafka import KafkaProducer

#intialize the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_and_produce(csv_file, topic):
    data = pd.read_csv(csv_file)

    print(f"Loaded {len(data)} rows from {csv_file}")
    print(data.head())

    transaction_id = 1  # make transaction_id incrementally
    for _, row in data.iterrows():
        row_dict = row.to_dict()
        true_score = row_dict.pop("Credit Score")  # Remove true_score from features dictionary
        message = {
            "transaction_id": transaction_id,
            "features": row_dict,
            "true_score": true_score
        }

        producer.send(topic, value=message)
        print(f"Produced: Transaction ID {transaction_id}")

        transaction_id += 1  

    producer.flush() # Waiting untile all the messages sent
    print("Finished producing messages.")


if __name__ == "__main__":
    topic_name = "credit-scoring" # I created a topic with this name in my Kafka cluster containg 3 partitions
    csv_file = r"Data\final_data.csv"  
    read_and_produce(csv_file, topic_name)

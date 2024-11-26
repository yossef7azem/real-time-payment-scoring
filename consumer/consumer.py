import json
from kafka import KafkaConsumer
import mysql.connector
import pandas as pd
import joblib


# mysql database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'root',  
    'database': 'credit_scoring_system'
}

# Load the pre-trained model
MODEL_PATH = 'Model\Credit_Scoring_final.joblib'  
model = joblib.load(MODEL_PATH)

FEATURES_TO_STORE = ["CurrentLoanAmount", "Annual Income", "Monthly Debt"]

def process_transaction(transaction ,connection):

    try:
        transaction_id = transaction['transaction_id']
        true_score = transaction['true_score']
        features = transaction['features']

        # features in the model
        model_input = pd.DataFrame([features]) 
        predicted_score = model.predict(model_input)[0]

        # Get some features to store in database
        selected_features = {key: features[key] for key in FEATURES_TO_STORE}

        # write into database
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO credit_scores (transaction_id, predicted_score, true_score, current_loan_amount, annual_income, monthly_debt)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            transaction_id,
            predicted_score,
            true_score,
            selected_features["CurrentLoanAmount"],
            selected_features["Annual Income"],
            selected_features["Monthly Debt"]
        ))
        connection.commit()

        cursor.close()
        

        print(f"Processed transaction: ID = {transaction_id}, Predicted Score = {predicted_score}, True Score = {true_score}")

    except Exception as e:
        print(f"Error : {e}")

#setup consumer 
def consume_transactions():
    consumer = KafkaConsumer(
        'credit-scoring',
        group_id='credit-scoring-group',  ## set in consumer group to avoid consuming same messages twice(dynamic partition assignment)
        bootstrap_servers = ['localhost:9092']  ,
        value_deserializer=lambda m: json.loads(m.decode('utf-8') ), 
        )

    print("Consumer started. Waiting for messages...")
    #set databae connection
    connection = mysql.connector.connect(**db_config)
    for message in consumer:
        transaction = message.value
        process_transaction(transaction,connection)
        
    connection.close()

if __name__ == '__main__':
    
    consume_transactions()
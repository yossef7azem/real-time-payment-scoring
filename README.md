# Real-Time Credit Scoring System
## Project Overview
This project implements a real-time credit scoring system using Apache Kafka for data streaming, a pre-trained machine learning model for transaction scoring, and a MySQL database to store the results. The system is designed to process financial transaction data in real-time, score transactions for creditworthiness, and store the results for further analysis.

 <a href="https://drive.google.com/file/d/1tFarsEG1i7S-sJtgZs-4uMnc9LH_lUwB/view?usp=sharing" target="_blank"> Video showing the project in action </a>
The process is divided into three main components:

- `Producer:` Reads transaction data from a CSV file and sends it to a Kafka topic.
- `Consumer:` Consumes the data from Kafka, applies a credit scoring model, and writes the results to a MySQL database.
- `Database:` Stores the results, including a subset of transaction features, predicted credit scores, and true values for comparison.

## Structure
Real-Time-Credit-Scoring/
├── Data/
│   └── final_data.csv                 # Example CSV file with transaction data
├── Model/
│   └── credit_scoring_model.joblib    # Pre-trained credit scoring model
├── consumer/
│   └── consumer.py                    # Consumer script to score transactions
├── producer/
│   └── producer.py                    # Producer script to send transactions to Kafka
├── DataBase-Creation-script.sql       # SQL script to create the MySQL database and table
├── README.md                          # Project documentation (this file)
├── docker-compose.yml                 # Docker Compose configuration for Kafka and zookeeper
├── Requirements.txt 

## Setup and Installation
### Prerequisites
- Docker and Docker Compose
- Python

### Step 1: Clone the Repository
### Step 2: Set Up Kafka and MySQL
- `docker-compose up -d`
- The topic `credit-scoring` is divided into 3 partitions for parallel processing. 
- Running multiple consumers with the same group_id `credit-scoring-group` ensures each partition is processed by one consumer.
### Step 3: Create the Database
- use script provided in mysql-workbensh to setup the database
### Step 4: Install Python Dependencies
- `pip install -r requirements.txt`


## Running the System
1. Consumers
-`python consumer/consumer.py`
2. Producer
- `python producer/producer.py` 


## Contact
- Name: Yusef Hazem
- Email: hazemyossef0@gmail.com
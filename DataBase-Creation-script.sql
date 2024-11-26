CREATE DATABASE credit_scoring_system;

USE credit_scoring_system;

CREATE TABLE credit_scores (
    transaction_id INT PRIMARY KEY,
    predicted_score FLOAT NOT NULL,
    true_score FLOAT NOT NULL,
    current_loan_amount FLOAT,
    annual_income FLOAT,
    monthly_debt FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

select * from credit_scores ;




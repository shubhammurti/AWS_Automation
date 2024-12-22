import boto3
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# AWS S3 details
BUCKET_NAME = 'your-s3-bucket-name'
FILE_NAME = 'path/to/your/file.csv'

# RDS details (for MySQL)
RDS_HOST = 'your-rds-hostname'  # e.g. 'mydbinstance.c8lfg7kssw5u.us-east-1.rds.amazonaws.com'
RDS_PORT = 3306  # Default MySQL port
RDS_USER = 'your-db-username'
RDS_PASSWORD = 'your-db-password'
RDS_DB_NAME = 'your-db-name'

# Step 1: Download the file from S3
def download_s3_file(bucket_name, file_name, local_filename):
    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, file_name, local_filename)
    print(f"File {file_name} downloaded to {local_filename}")

# Step 2: Load CSV data into pandas DataFrame
def load_csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    print(f"Data loaded from {file_path} into DataFrame with shape {df.shape}")
    return df

# Step 3: Insert data into RDS (MySQL)
def insert_data_into_rds(df, table_name):
    # Establish database connection
    connection_string = f'mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB_NAME}'
    engine = create_engine(connection_string)
    
    # Load the DataFrame into the RDS table
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data successfully inserted into {table_name} table in RDS")
    except Exception as e:
        print(f"Error inserting data into RDS: {e}")

def main():
    # Define local file path to download the CSV
    local_file_path = '/tmp/temp_file.csv'
    
    # Step 1: Download CSV from S3
    download_s3_file(BUCKET_NAME, FILE_NAME, local_file_path)
    
    # Step 2: Load CSV into pandas DataFrame
    df = load_csv_to_dataframe(local_file_path)
    
    # Step 3: Insert data into RDS MySQL
    table_name = 'your_table_name'  # Ensure this table exists in your RDS DB
    insert_data_into_rds(df, table_name)

if __name__ == "__main__":
    main()

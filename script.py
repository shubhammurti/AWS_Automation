# For Dockerfile "pip install boto3 mysql-connector-python"

#CREATE TABLE customers (
#    customer_id INT PRIMARY KEY,
#    Genre VARCHAR(100),
#    Age VARCHAR(100),
#    Annual_Income VARCHAR(20)
#);

#SELECT * FROM customers;

import boto3
import mysql.connector
import csv
from mysql.connector import Error


s3_bucket = "my-s3-bucket-for-jenkins"
s3_key = "Customers.csv"


rds_host = "database-1.cva6gege0wff.us-east-1.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_dbname = "myrdsdb"


def download_file_from_s3():
    s3_client = boto3.client('s3')
    print(f"Downloading {s3_key} from S3 bucket {s3_bucket}...")
    local_file = 'C:/Users/DELL/Desktop/AWS_Automation/temp/Customers.csv'
    s3_client.download_file(s3_bucket, s3_key, local_file)
    print(f"File downloaded to {local_file}")
    return local_file


def insert_data_to_rds(file_path):
    try:
        connection = mysql.connector.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            database=rds_dbname
        )

        if connection.is_connected():
            cursor = connection.cursor()

            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                
                for row in csv_reader:
                    cursor.execute("""
                        INSERT INTO customers (customer_id, Genre, Age, Annual_Income)
                        VALUES (%s, %s, %s, %s)
                    """, (row[0], row[1], row[2], row[3]))

            connection.commit()
            print("Data inserted successfully!")

            cursor.close()
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed.")

def main():
    file_path = download_file_from_s3()
    insert_data_to_rds(file_path)

if __name__ == "__main__":
    main()

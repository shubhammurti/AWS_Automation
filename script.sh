#!/bin/bash

# Ask the user for AWS Access Key ID
read -p "Enter your AWS Access Key ID: " AWS_ACCESS_KEY_ID

# Ask the user for AWS Secret Access Key
read -sp "Enter your AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
echo

# Export the AWS credentials as environment variables
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

# Enable debugging to see what's happening
set -x

# Step 1: Clone the GitHub repo
git clone https://github.com/Dark-Cookie/Jenkins-Pipeline.git
cd Jenkins-Pipeline/


# Step 2: Initialize Terraform
terraform init

# Step 3: Validate Terraform configurations
terraform validate

# Step 4: Generate the Terraform execution plan
terraform plan

# Step 5: Apply Terraform plan
terraform apply -auto-approve

# Step 6: Get the database endpoint from Terraform output
DB_ENDPOINT=$(terraform output)
echo "DB Endpoint: $DB_ENDPOINT"

# Extract DB Host from the endpoint
DB_HOST=$(echo "$DB_ENDPOINT" | sed 's/^rds_endpoint = "//;s/:3306"$//')
echo "DB Host: $DB_HOST"

# Step 7: Connect to MySQL
mysql -h "$DB_HOST" -P 3306 -u admin -padmin123 --ssl-ca=us-east-1-bundle.pem

# Step 8: Build Docker image
docker build -t my-docker-image .

# Disable debugging to stop printing the commands after this point
set +x


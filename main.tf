provider "aws" {
  region     = "us-east-1"
  access_key = ""
  secret_key = ""
}



resource "aws_s3_bucket" "bucket" {
  bucket = "bucket-automation-testing"
}


resource "aws_s3_object" "object" {
bucket = aws_s3_bucket.bucket.bucket
key    = "Customers.csv"
source = "C:/Users/DELL/Desktop/AWS_Automation/Customers.csv"
}


resource "aws_db_instance" "myrdsdb" {
  allocated_storage    = 5
  max_allocated_storage = 10
  db_name              = "myrdsdb"
  engine               = "mysql"
  engine_version       = "8.0.40"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "admin123"
  parameter_group_name = "default.mysql8.0"
  storage_type         = "gp2"
  skip_final_snapshot  = true
  publicly_accessible = true
  identifier = "database-1"
  
}


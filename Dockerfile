FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install boto3 mysql-connector-python

ENV AWS_ACCESS_KEY_ID=your-aws-access-key-id
ENV AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
ENV AWS_DEFAULT_REGION=us-east-1

ENV RDS_HOST=database-1.cnkemg6yuu9r.us-east-1.rds.amazonaws.com
ENV RDS_USER=admin
ENV RDS_PASSWORD=admin123
ENV RDS_DBNAME=myrdsdb

EXPOSE 80

CMD ["python", "script.py"]

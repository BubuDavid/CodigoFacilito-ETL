from io import BytesIO

import boto3
import pandas as pd
from sqlalchemy import create_engine

#### NOTE: Credentials are hardcoded for demo purposes. Do not hardcode credentials in production code. ####
# PostgreSQL connection details
pg_host = "localhost"
pg_port = "5432"
pg_user = "myuser"
pg_password = "mypassword"
pg_database = "mydb"

# MinIO connection details
minio_endpoint = "localhost:9000"
minio_access_key = "minioadmin"
minio_secret_key = "minioadmin"
minio_bucket = "my-demo-bucket"
minio_filename = "Enjambreee.xlsx"

# Connect to PostgreSQL using SQLAlchemy
engine = create_engine(
    f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
)

# Connect to MinIO
minio_client = boto3.client(
    "s3",
    endpoint_url=f"http://{minio_endpoint}",
    aws_access_key_id=minio_access_key,
    aws_secret_access_key=minio_secret_key,
)

# Download file from MinIO
response = minio_client.get_object(Bucket=minio_bucket, Key=minio_filename)
data = response["Body"].read()

# Use BytesIO to handle the data for pandas
excel_data = BytesIO(data)

# Transform data to pandas
df = pd.read_excel(excel_data)

# Here you can do any data transformation you need
# For example, you can rename columns


# Upload DataFrame to PostgreSQL
df.to_sql("enjambre", engine, if_exists="replace", index=False)

print("Data uploaded successfully to PostgreSQL")

# Close the SQLAlchemy engine connection
engine.dispose()

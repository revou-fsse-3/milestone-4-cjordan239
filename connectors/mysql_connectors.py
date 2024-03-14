from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_URL')
database = os.getenv('DB_NAME')

# Connect to the database
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database}')


# Test the connection
connection = engine.connect()
Session = sessionmaker(connection)
print(f'Connected to the MySQL Database at {host}')
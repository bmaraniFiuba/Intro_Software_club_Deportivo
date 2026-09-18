from flask import Flask, jsonify
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "Club_Deportivo")
    )

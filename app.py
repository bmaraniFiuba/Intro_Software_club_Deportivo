import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "Club_Deportivo"),
        port=int(os.getenv("DB_PORT", 3306))
    )

@app.route("/")
def ping():
    return jsonify({"mensaje": "API del Club Deportivo en línea"}), 200

app.run(host="0.0.0.0", port=8080, debug=True)
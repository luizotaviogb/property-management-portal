from flask import Flask
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="property_management",
        user="user",
        password="password",
        host="db",
        port="5432"
    )
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM properties;')
    properties = cur.fetchall()
    cur.close()
    conn.close()
    return {'properties': properties}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
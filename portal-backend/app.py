from app import create_app
import tenacity
import psycopg2
from psycopg2 import OperationalError
import os

@tenacity.retry(stop=tenacity.stop_after_attempt(20), wait=tenacity.wait_fixed(5))
def wait_for_db():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'property_management'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )
    conn.close()

if __name__ == '__main__':
    wait_for_db()
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)))
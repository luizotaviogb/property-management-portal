from app import create_app
import tenacity
import psycopg2
from psycopg2 import OperationalError

@tenacity.retry(stop=tenacity.stop_after_attempt(20), wait=tenacity.wait_fixed(5))
def wait_for_db():
    conn = psycopg2.connect(
        dbname="property_management",
        user="user",
        password="password",
        host="db",
        port="5432"
    )
    conn.close()

if __name__ == '__main__':
    wait_for_db()
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
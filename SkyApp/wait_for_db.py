import time
import psycopg2

while True:
    try:
        conn = psycopg2.connect(
            dbname="skyapp",
            user="skyuser",
            password="skypass",
            host="db",
            port="5432"
        )
        print("✅ PostgreSQL prêt !")
        break
    except psycopg2.OperationalError:
        print("⏳ En attente de PostgreSQL...")
        time.sleep(2)
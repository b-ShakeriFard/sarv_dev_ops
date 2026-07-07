
from flask import Flask, render_template
from sqlalchemy import create_engine
import psycopg2
import os

app = Flask(__name__)

# Database connection parameter 
DB_HOST = "postgres_db"
DB_NAME = "postgresdb"
DB_USER = "behroox"
DB_PASSWORD = "junk00"

DATABASE_URL = "postgresql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":5432/" + DB_NAME

print(DATABASE_URL)

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is not a match")

@app.route('/')
def index():

    try:
        # Connect to the Postgres DB
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # execute a simple query
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()

        # close the database connection
        cursor.close()
        connection.close()

        # pass data to index.html
        return render_template('index.html', rows=rows)

    except Exception as e:
        return f"Error connection to the database: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

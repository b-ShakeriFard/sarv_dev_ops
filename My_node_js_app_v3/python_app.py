import csv
import calendar
import pandas as pd

import os
import redis
from flask import Flask

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("python_app")

app = Flask(__name__)

# define path to csv file
LOG_DIR = "/data" # later to be mapped to PV
LOG_FILE = os.path.join(LOG_DIR, "calendar_log.csv")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Only generate CSV once
if not os.path.exists('test_data.csv'):
    DataFrame = pd.DataFrame(index=range(9), columns=[1, 2, 3])
#    for i in range(9):
#        for j in range(1, 4):
#            DataFrame.loc[i, j] = str(i * j)
    DataFrame.to_csv('test_data.csv')
    logging.info("CSV file created.")

else:
    DataFrame = pd.read_csv('test_data.csv', index_col=0)
    logging.info("CSV file loaded.")

def get_redis_connection():
    redis_host = os.environ.get("REDIS_HOST", "redis-service")
    redis_port = int (os.environ.get("REDIS_PORT","6379"))

    try:
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        r.ping()
        logging.info("Connected to Redis from Python.")
        return r

    except redis.connectionError as e:
        logging.error(f"Redis Connection failed. {e}")
        return None 

@app.route('/')
def generate_calendar():
    try:
        r = get_redis_connection()
        year = r.get("key1")
        month = r.get("key2")

        logger.info(f"Retrieved from Redis: year={year}, month={month}")
        
        # validate input
        if not (year and month and year.isdigit() and month.isdigit()):
            return "<h3> Invalid input. </h3> <p> Awaiting correct format for year and month</p>"

        # convert to integer
        year = int(year)
        month = int(month)

        if month < 1 or month > 12:
            return "<h3> Invalid month! Month must be between 1 and 12 </h3>"

        cal = calendar.month(year, month)
        
        # Create log files each time the function runs
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), year, month])
            logger.info(f"Logged to CSV: {year}-{month}")


        return f"<h2> Calendar for {calendar.month_name[month]} {year} </h2> <pre> {cal} </pre>"
    except Exception as e:
        logger.error(f"Error generating calendar: {e}")
        return f"<h3> Internal Error:</h3> <p> {str(e)} </p>",500

# print(calendar.month(year,month))
# print(DataFrame)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

from flask import Flask, render_template, request, g
from redis import Redis, ConnectionError
import os
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def get_redis():
    redis_host = os.environ.get('REDIS_HOST','localhost')
    if not hasattr(g, 'redis'):

        try:
            
            g.redis = Redis(host=redis_host, port=6379, db=0, socket_timeout=5, decode_responses=True)
            g.redis.ping()

            logger.info("Connected to Redis successfully.")

        except ConnectionError as e:
            g.redis = None
            logger.info(f"Failed to connect to Redis: {e}")
    return g.redis


@app.route('/', methods=['GET','POST'])
def handle_keys():

    # check connection 
    redis_client = get_redis()
    connection_status = ""
    value1 = ""
    value2 = ""

    if request.method == 'POST':
        key1 = 'key1'
        key2 = 'key2'
        value1 = request.form.get('value1')
        value2 = request.form.get('value2')

        if redis_client:
            try:
                redis_client.set(key1, value1)
                redis_client.set(key2, value2)
                connection_status =  "Values set successfully in Redis!"

                # insert python related stuff here
                try:
                    r = requests.get("http://python-service:5004/")
                    logger.info("python service responded with:")
                    logger.info(r.text[:100]) # preview response
                except Exception as e:
                    logger.warning(f"Could not reach python service: {e}")

                connection_status = "Values set and Python app triggered!"

            except Exception as e:
                connection_status = f"Error setting value: {e}"
                logger.error(connection_status)
        else:
            connection_status = "Failed to connect to Redis!"

    else:
        if redis_client:
            connection_status = "Connected to Redis successfully!"
            value1 = redis_client.get('key1') or "Key not found!"
            value2 = redis_client.get('key2') or "Key not found!"
        else:
            connection_status = "Failed to connect to Redis!"
            value1 = "No connection!"
            value2 = "No connection!"

    
    return render_template('index.html', connection_status=connection_status, value1=value1, value2= value2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

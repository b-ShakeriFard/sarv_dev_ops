import os
from flask import Flask, render_template, g
from redis import Redis, ConnectionError

app = Flask(__name__)

def get_redis():
    redis_host = os.environ.get('REDIS_HOST','localhost')
    if not hasattr(g, 'redis'):

        try:
            g.redis = Redis(host=redis_host, port=6379, db=0, socket_timeout=5, decode_responses=True)
            g.redis.ping()
        except ConnectionError:
            g.redis = None
    return g.redis


@app.route('/')
def get_key():

    # check connection 
    redis_client = get_redis()
    if redis_client:
        connection_status = "Connected to Redis successfully!"
        value = redis_client.get('key1') or "Key not found"
    else:
        connection_status = "Failed to connect to Redis!"
        value = "No connection!"

    
    return render_template('index.html', connection_status=connection_status, value=value)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

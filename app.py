import flask
from flask import Flask
from flask import Flask, jsonify, request
import docker
import time
from orchestrator import *

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/run_test')
def run_docker_test():
    request_config =  request.get_json()
    nodes = request_config.get('nodes')
    tweets_to_retrieve =  request_config.get('tweets_to_retrieve')
    pool_max =  request_config.get('pool_max')

    inital_time = time.time()
    run_test(nodes, pool_max, tweets_to_retrieve)
    duration_time = time.time() - inital_time

    return jsonify(code = 200, body={"nodes": nodes, "pool_max": pool_max, "duration_time": duration_time})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=5000)
	
import hashlib
import docker
import logging
import time
import random
from docker import client
from helpers.json_helpers import *

from concurrent.futures import ThreadPoolExecutor, as_completed



def retrieve_clients(clients_number = None):
    docker_clients = []
    model = load_json('./model/clients')
    clients_to_retrieve =  clients_number if clients_number else len(model)
    for i, (node_id, node) in  enumerate(model.items()):
        if i > clients_to_retrieve-1:
            break;
        try:
            logging.info(f'Starting docker client: {node_id}')
            url = node.get('url')
            client = docker.DockerClient(base_url=f'tcp://{url}:4243',  tls=False)
            docker_clients.append(client)
        except Exception as e:
            logging.error(e)

    return docker_clients

def run_test(clients_num = None, pool_max = 3, tweets_to_retrieve = 10):
    docker_clients = retrieve_clients(clients_num)
    users = load_json('./model/twitter_usernames').get('users')
    futures = []
    responses = []

    #pool = ThreadPoolExecutor(pool_max)
    with ThreadPoolExecutor(max_workers=pool_max) as pool:
        for user in users:
            future = pool.submit(run_docker, random.choice(docker_clients), (user), tweets_to_retrieve)
            futures.append(future)

        for future in as_completed(futures):
            responses.append(future.result())

    return len(responses)
    
        
def run_docker (client, user, count):
    container = client.containers.run(f'viniciusalves/tweet_extractor',f'--u {user}  --n {count}', detach=True)
    logs = container.logs()
    
    for line in container.logs(stream=True):
       print(line.strip())





	










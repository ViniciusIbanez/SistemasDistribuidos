import hashlib
import docker
import logging
import time
import random
from docker import client
from helpers.json_helpers import *
from concurrent.futures import ThreadPoolExecutor


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
    
    with ThreadPoolExecutor(len(docker_clients)*pool_max) as e:
        for user in users:
            future = e.submit(run_docker, random.choice(docker_clients), user, tweets_to_retrieve)
        
    
def run_docker (client, user, count):
    container = client.containers.run(f'viniciusalves/tweet_extractor',f'--u {user}  --n {count}', detach=True, name=user)
    logs = container.logs()
    
    for line in container.logs(stream=True):
        logging.info(line.strip())





	










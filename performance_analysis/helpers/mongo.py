import pymongo
import logging
from dictionaries import Dict
from pymongo import MongoClient
import dns
import os


def connect(credentials: Dict,
            collection: str = None ) -> MongoClient:
    try:
        database = credentials.get("MONGO_DATABASE")
        username = credentials.get('MONGO_USER')
        password = credentials.get('MONGO_PASSWORD')
        connector = credentials.get('MONGO_CONNECTOR')

        url = connector.format(username=username, password=password)
        print(url)
        client = pymongo.MongoClient(url)
        db = client[database]
        connection = db[collection]
        logging.info('MongoConnector: Connecting to DataBase')
        return connection
    except Exception as ex:
        logging.error(f'MongoConnector: {ex}')
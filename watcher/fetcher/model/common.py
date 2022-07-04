import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pymongo

def getHttpClient():

    retry_strategy = Retry(
        total=10,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    return http

def getLatestNearest(conn, db_name:str, col_name:str, loc:dict, max_dist:int):
    # connection = pymongo.MongoClient('localhost', 27017)

    if db_name not in conn.list_database_names():
        logging.error(f'No such DB: {db_name}')
        return []
    db = conn[db_name]

    if col_name not in db.list_collection_names():
        logging.error(f'No such collection({col_name}) in DB{db_name}')
        return []
    
    collection = db[col_name]
    collection.create_index([ ('LOCATION', pymongo.GEOSPHERE ) ])

    res = []
    try:
        res = db.wog.aggregate([
            {'$geoNear': {
                'near': {
                    'type': 'Point',
                    'coordinates':  [loc['longitude'], loc['latitude']]
                }, 
                'maxDistance': max_dist,
                'spherical': False,
                'distanceField': 'DISTANCE',
                'distanceMultiplier': 1
                }
            },
            {'$sort': {'DATE': 1, '_id': 1}
            },
            {'$group': {
                '_id': '$ID',
                'DOC': {'$last': '$$ROOT'}
                }
            },
            {'$sort': {'DOC.DISTANCE': 1, '_id': 1}
            }
        ])
        return [r['DOC'] for r in res]
    except Exception as e:
        logging.error(f'Error in  query: {e}')
        return []


import pymongo
import logging

class FuelStationDB:
    def __init__(self, creds):
        self.db_name = creds['db_name']
        self.host = creds['host']
        self.port = creds['port']
        self.connection = None

    def connect(self):
        self.connection = pymongo.MongoClient(self.host, self.port)

    def db(self):
        return self.connection[self.db_name]

    def collection(self, col_name):
        return self.db()[col_name]

    # TODO: move to a different place
    def getLatestNearest(self, col_name:str, loc:dict, max_dist:int):
    
        # if db_name not in conn.list_database_names():
        #     logging.error(f'No such DB: {db_name}')
        #     return []
        # db = conn[db_name]

        # if col_name not in db.list_collection_names():
        #     logging.error(f'No such collection({col_name}) in DB{db_name}')
        #     return []
        
        collection = self.collection(col_name)
        collection.create_index([ ('LOCATION', pymongo.GEOSPHERE ) ])

        res = []
        try:
            res = collection.aggregate([
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

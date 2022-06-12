import math
import logging
from logging.handlers import RotatingFileHandler
import pickle
import pandas as pd

def prepare_logger(path_to_log):
    log = logging.getLogger()  
    for hdlr in log.handlers[:]:  
        log.removeHandler(hdlr)

    fileh = RotatingFileHandler(path_to_log, maxBytes=10*1000*1000, backupCount=5)

    formatter = logging.Formatter('%(asctime)s [%(name)s:%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s')
    fileh.setFormatter(formatter)
    
    log.addHandler(fileh)
    log.setLevel(logging.DEBUG)

def read_pickle(path_to_pkl): 
    try:
        logging.debug(f'Read data from: {path_to_pkl}')
        with open(path_to_pkl, 'rb') as f:
            return pickle.load(f)
        
    except Exception as e:
        logging.error(e)
        return None

def save_pickle(data, path_to_pkl): 
    try:
        logging.debug(f'Save data to: {path_to_pkl}')
        with open(path_to_pkl, 'wb') as f:
            pickle.dump(obj=data, file=f)

    except Exception as e:
        logging.error(e)
class Coords:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self):
        return f'({self.longitude}, {self.latitude})'
class Stats:
    def distance(mk1:Coords, mk2:Coords):
        R = 6371.0710 # Radius of the Earth in kms
        rlat1 = mk1.latitude * (math.pi/180) # Convert degrees to radians
        rlat2 = mk2.latitude * (math.pi/180) # Convert degrees to radians
        difflat = rlat2-rlat1 # Radian difference (latitudes)
        difflon = (mk2.longitude-mk1.longitude) * (math.pi/180) # Radian difference (longitudes)
        d1 = 2*R*math.asin(math.sqrt(math.sin(difflat/2)*math.sin(difflat/2)+math.cos(rlat1)*math.cos(rlat2)*math.sin(difflon/2)*math.sin(difflon/2)))

        return d1

def get_closest_stations(df:pd.DataFrame, user_location:Coords):
    pass
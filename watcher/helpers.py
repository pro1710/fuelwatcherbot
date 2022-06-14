import math
import logging
import pickle
import datetime
import pandas as pd

from logging.handlers import RotatingFileHandler

def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

def get_closest(data_loc, user_loc):
    df = pd.read_pickle(data_loc)
    mk1 = Coords(**user_loc)
    def foo(lat2, long2):
        mk2 = Coords(latitude=lat2, longitude=long2)
        return round(Stats.distance(mk1, mk2), 1)

    df['DISTANCE'] = df.apply(lambda r: foo(r['LATITUDE'], r['LONGITUDE']), axis=1)
    dfByDist = df.sort_values(by=['DISTANCE'])
    df12km= dfByDist[dfByDist['DISTANCE'] < 12]

    def has(val):
        try:
            return 'Готівка, банк.картки' in val 
        except:
            return False

    closest = []

    first = dfByDist[dfByDist['A95'].apply(has) | dfByDist['A95E'].apply(has)].iloc[0]
    has95 = '+' if has(first['A95']) else '-'
    has95E = '+' if has(first['A95E']) else '-'
    closest.append('{:<7}{:<6}{:<6}\n{}'.format(first['DISTANCE'], f'95({has95})', f'95E({has95E})', first['ADDRESS']))
    
    for _, row in df12km.iterrows():
        has95 = '+' if has(row['A95']) else '-'
        has95E = '+' if has(row['A95E']) else '-'

        resp = '{:<5}{:<6}{:<6}\n{}'.format(row['DISTANCE'], f'95({has95})', f'95E({has95E})', row['ADDRESS'])
        closest.append(resp)
        # print(status_str)
        # print('-'*80)

    return closest
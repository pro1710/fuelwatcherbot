# main.py

#%%
import os
import pandas as pd
from pymongo import MongoClient
import time

import logging

import helpers
from fetcher.providers import wog

PATH_TO_DATA = './data/'


#%%

def main():
    
    if not os.path.isdir(PATH_TO_DATA):
        print(f'No such directory: {PATH_TO_DATA}')
        return

    connection = MongoClient('localhost', 27017)
    db = connection['fuel_stations']
    wog_collection = db['wog']

    epoch = 0
    while True:
        ts = time.time()
        wog_data =  wog.getData()
        # for station_data in wog.getData():
            # wog_data.append(station_data)

        res = wog_collection.insert_many(wog_data)
        # print(res)
        # df_wog = pd.DataFrame(wog_data)

        # path_to_wog_data = f'{PATH_TO_DATA}/wog/'
        # if not os.path.isdir(path_to_wog_data):
        #     print(f'No such directory: {path_to_wog_data}')
        #     return

        # pd.to_pickle(df_wog, f'{PATH_TO_DATA}/wog/last.pkl')

        # fname = f'{path_to_wog_data}/out_{time.time():.3f}.csv'
        # df_wog.to_csv(fname) 
        
        # print(f'{helpers.current_time()} Finished[{epoch}]. Data saved into: {fname} [{time.time()-ts:.3f}]')
        print(f'{helpers.current_time()} Finished[{epoch}]. Data saved [{time.time()-ts:.3f}]')
        epoch += 1
        time.sleep(15*60)



if __name__ == '__main__':
    print('Started')
    helpers.prepare_logger('./log/poller.log')

    logging.info('Started')
    main()
    logging.info('Finished')



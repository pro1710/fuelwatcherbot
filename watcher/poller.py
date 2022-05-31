# main.py

#%%
import os
import pandas as pd
import time
import logging
from fetcher.providers import wog

# from importlib import reload
# logging = reload(logging)

PATH_TO_DATA = './data/'

def prepareLogger():
    log = logging.getLogger()  
    for hdlr in log.handlers[:]:  
        log.removeHandler(hdlr)

    fileh = logging.FileHandler('./log/bot.log', 'a')
    formatter = logging.Formatter('%(asctime)s [%(name)s:%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s')
    fileh.setFormatter(formatter)
    
    log.addHandler(fileh)
    log.setLevel(logging.DEBUG)

#%%

def main():
    ts = time.time()
    if not os.path.isdir(PATH_TO_DATA):
        print(f'No such directory: {PATH_TO_DATA}')
        return

    df_wog = wog.getData()

    path_to_wog_data = f'{PATH_TO_DATA}/wog/'
    if not os.path.isdir(path_to_wog_data):
        print(f'No such directory: {path_to_wog_data}')
        return

    fname = f'{path_to_wog_data}/out_{time.time():.3f}.csv'
    df_wog.to_csv(fname) 
    print(f'Finished. Data saved into: {fname} [{time.time()-ts:.3f}]')


if __name__ == '__main__':

    prepareLogger()

    logging.info('Started')
    main()
    logging.info('Finished')



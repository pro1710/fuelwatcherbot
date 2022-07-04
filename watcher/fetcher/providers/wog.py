import logging
import time

import datetime
# import pandas as pd

import geojson

from collections import defaultdict

from fetcher.model.types import Fuel, FuelStation, FuelStationState
from fetcher.model.common import getHttpClient

STATION_LIST_API_URL = 'https://api.wog.ua/fuel_stations'

def getFuelStationList():
    logging.debug(f'GET: {STATION_LIST_API_URL}')
    # fuel_stations_rsp = requests.get(STATION_LIST_API_URL)
    http = getHttpClient()
    fuel_stations_rsp = http.get(STATION_LIST_API_URL)

    try:
        return fuel_stations_rsp.json()['data']['stations']
    except Exception as e:
        logging.error(f'Failed to get station list: {STATION_LIST_API_URL} {e}')
        raise

def getStationInfo(fuel_station):
    station_info_api_url = fuel_station['link']
    logging.debug(f'GET: {station_info_api_url}')
    # station_state_rsp = requests.get(station_info_api_url)
    http = getHttpClient()
    station_state_rsp = http.get(station_info_api_url)
    try:
        return station_state_rsp.json()['data']['workDescription']
    except Exception as e:
        logging.error(f'Failed to get station info: {station_info_api_url} {e}')
        raise

station_state_mapping = defaultdict(lambda: FuelStationState.UNKNOWN)
fuel_category_mapping = defaultdict(lambda: Fuel.Other.UNKNOWN)
fuel_status_mapping = defaultdict(lambda: Fuel.Status.UNKNOWN)

wog_station_state_mapping = {
    'Працює тільки з сервісом WOG PAY.': FuelStationState.LIMITED, 
    'АЗК працює згідно графіку.': FuelStationState.OPEN
}
station_state_mapping.update(wog_station_state_mapping)

wog_fuel_category_mapping = {
    'М95': Fuel.Gasoline.A95E,
    'М100': Fuel.Gasoline.A100E,
    'А95': Fuel.Gasoline.A95,
    'А92': Fuel.Gasoline.A92,
    'ДП': Fuel.Diesel.DP,
    'МДП+': Fuel.Diesel.DPE,
    'ГАЗ': Fuel.Other.IRRELEVANT,
}
fuel_category_mapping.update(wog_fuel_category_mapping)

wog_fuel_status_mapping = {
    'Готівка, банк.картки 20л. Гаманець ПРАЙД до 100л. Талони до 40л. Паливна картка (ліміт картки).': Fuel.Status.LIMITED,
    'Пальне відсутнє.': Fuel.Status.MISSING,
    'тільки спецтранспорт.': Fuel.Status.SPECONLY,
    'Тільки спецтранспорт.': Fuel.Status.SPECONLY
}
fuel_status_mapping.update(wog_fuel_status_mapping)

def convert2station(station_descr, station_info):
    fuel_station = FuelStation.getTemplate()
    
    fuel_station['PROVIDER'] = 'WOG'
    fuel_station['ID'] = station_descr['id']
    fuel_station['LINK'] = station_descr['link']
    fuel_station['CITY'] = station_descr['city']
    fuel_station['LOCATION'] = geojson.Point((station_descr['coordinates']['longitude'], station_descr['coordinates']['latitude']))
    # fuel_station['LATITUDE'] = station_descr['coordinates']['latitude']
    # fuel_station['LONGITUDE'] = station_descr['coordinates']['longitude']
    fuel_station['ADDRESS'] = station_descr['name']
    fuel_station['DATE'] = datetime.datetime.now()
    fuel_station['STATUS'] = station_info

    # state_rows = station_info.strip().split('\n')
    # fuel_station['STATUS'] = station_state_mapping[state_rows[0]].name

    # for fuel_info in state_rows[1:]:
    #     # print(station_info)
    #     raw_fuel_category, raw_fuel_status = tuple(map(lambda x: x.strip(), fuel_info.split(' - ')))
    #     # convers to functions
    #     fuel_category = fuel_category_mapping[raw_fuel_category]
    #     # fuel_status = fuel_status_mapping[raw_fuel_status] 
        
    #     fuel_station[fuel_category.name] = raw_fuel_status

    return fuel_station

def getData():
    logging.info('Getting data using WOG api')
    ts = time.time()
    
    fuel_station_data = []
    fuel_station_list = getFuelStationList()
    for i, station_descr in enumerate(fuel_station_list):
        station_info = getStationInfo(station_descr)
        try:
            fuel_station = convert2station(station_descr, station_info)
        except Exception as e:
            logging.warning(f'Failed to process: {station_descr} [{e}]')
            continue
         
        fuel_station_data.append(fuel_station)
        
        time.sleep(0.05)

    return fuel_station_data

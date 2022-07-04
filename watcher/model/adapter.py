from entities import *
from fuelwatcherbot.watcher.model.entities import GenericFuelStation
from collections import defaultdict
import logging

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

def WogToFuelStation(data:dict):
    fs = GenericFuelStation(data)

    status, *storage= fs.DATA.strip().split('\n')
    if status not in station_state_mapping:
        logging.warn(f'Unknown station state ID({fs.ID}) record({fs._id}): {status}')

    fs.set('STATUS', station_state_mapping[status])

    storage = dict()

    for fuel_info in storage:
        # print(station_info)
        fuel_category, fuel_status = tuple(map(lambda x: x.strip(), fuel_info.split(' - ')))

        if fuel_category not in fuel_category_mapping:
            logging.warn(f'Unknown fuel category ID({fs.ID}) record({fs._id}): "{fuel_category}" in "{fuel_info}"')
        
        storage[fuel_category] = fuel_category_mapping[fuel_category]
        
        if fuel_status not in fuel_status_mapping:
            logging.warn(f'Unknown fuel status ID({fs.ID}) record({fs._id}): "{fuel_category}" in "{fuel_info}"')

        storage[fuel_category] = fuel_status_mapping[fuel_category]

    return fs, storage
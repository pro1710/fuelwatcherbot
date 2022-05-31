# common.py

import math

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


# def readWogPickle(stations_pkl_file, fuel_pkl_file): 
#     try:
#         logging.debug(f'Read station info pkl from: {stations_pkl_file}')
#         with open(stations_pkl_file, 'rb') as f:
#             raw_stations = pickle.load(f)

#         logging.debug(f'Read fuel state pkl from: {fuel_pkl_file}')
#         with open(fuel_pkl_file, 'rb') as f:
#             raw_fuels = pickle.load(f)
#     except Exception as e:
#         logging.error(e)
#         return None, None

#     return raw_stations, raw_fuels

# def saveToPickle(raw_stations, raw_fuels, path2dir='./data'): 
#     try:
#         stations_pkl_file = f'{path2dir}/stations_{time.time()}.pkl'
#         logging.debug(f'Save station info to: {stations_pkl_file}')
#         with open(stations_pkl_file, 'wb') as f:
#             pickle.dump(obj=raw_stations, file=f)

#         fuel_pkl_file = f'{path2dir}/fuel_{time.time()}.pkl'
#         logging.debug(f'Save fuel state to: {fuel_pkl_file}')
#         with open(fuel_pkl_file, 'wb') as f:
#             pickle.dump(obj=raw_fuels, file=f)
#     except Exception as e:
#         logging.error(e)
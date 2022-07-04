
#%% 
import helpers
import config
from fetcher.model.types import Fuel
from fetcher.model.common import *

import pandas as pd
import pymongo

#%%


connection = pymongo.MongoClient('localhost', 27017)

print(connection.list_database_names())
db = connection['fuel_stations']

print(db.list_collection_names())
collection = db['wog']

#%%

collection.create_index([ ('LOCATION', pymongo.GEOSPHERE ) ])

print(sorted(list(collection.index_information())))
#%%
res = collection.find(
     {'LOCATION': {
        '$nearSphere':  [
            config.user_location['longitude'],
            config.user_location['latitude']
        ]
     }  
    }).limit(5)
  

for fs in res:
    print(fs)


#%%
res = collection.aggregate( [
     {'$match': {
        'ID': {'$in': [807, 902]}
    }},
    {'$group': {
        '_id': '$ID',
        'DOC': {'$last': '$$ROOT'}
    }}
    ] )

for fs in res:
    print(fs)

#%%
res = collection.aggregate( [
     {'$geoNear': {
        'near': {
            config.user_location['longitude'],
            config.user_location['latitude']
        },
        'distanceField': 'dist.calculated',
        'key': 'LOCATION'
        }
    },
    {'$group': {
        '_id': '$ID',
        'DOC': {'$last': '$$ROOT'}
    }}
    ] 
)

#%%
res = db.wog.aggregate([
    {'$geoNear': {
        'near': {
            'type': 'Point',
            'coordinates':  [
                config.user_location['longitude'],
                config.user_location['latitude']
            ]
        }, 
        'maxDistance': 15000,
        'spherical': False,
        'distanceField': 'DISTANCE',
        'distanceMultiplier': 0.001
        }
    },
    {'$group': {
        '_id': '$ID',
        'DOC': {'$max': 'DATE'}
        }
    },
    {
        '$sort': {'DOC.DISTANCE': 1, '_id': 1}
    }
])

#%%
res = db.wog.aggregate([
    {'$geoNear': {
        'near': {
            'type': 'Point',
            'coordinates':  [
                config.user_location['longitude'],
                config.user_location['latitude']
            ]
        }, 
        'maxDistance': 15000,
        'spherical': False,
        'distanceField': 'DISTANCE',
        'distanceMultiplier': 0.001
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
for fs in res:
    # print(fs)
    doc = fs['DOC']
    print(doc['ID'], doc['DISTANCE'], doc['DATE'], doc['CITY'])
#%%

connection = pymongo.MongoClient('localhost', 27017)
res = getLatestNearest(connection, 
                       db_name='fuel_station', 
                       col_name='wog',
                       loc=config.user_location,
                       max_dist=10000
                       )
# collection.create_index([ ('LOCATION', pymongo.GEOSPHERE ) ])

#%%

# df = pd.read_pickle('../../data/wog/last.pkl')

# mk1 = helpers.Coords(**user_location)
# def foo(lat2, long2):
#         mk2 = helpers.Coords(latitude=lat2, longitude=long2)
#         return round(helpers.Stats.distance(mk1, mk2), 1)

# df['DISTANCE'] = df.apply(lambda r: foo(r['LATITUDE'], r['LONGITUDE']), axis=1)
# dfByDist = df.sort_values(by=['DISTANCE'])
# df12km= dfByDist[dfByDist['DISTANCE'] < 12]

# def has(val):
#     try:
#         return 'Готівка, банк.картки' in val 
#     except:
#         return False



# dfByDist[dfByDist['A95'].apply(has)].head()








# print(get_closest('../../data/wog/last.pkl', user_location))

# #%%
# # 
# df = pd.read_pickle('../../data/wog/last.pkl')
# #%%

# mk1 = helpers.Coords(**user_location)
# def foo(lat2, long2):
#     mk2 = helpers.Coords(latitude=lat2, longitude=long2)
#     return round(helpers.Stats.distance(mk1, mk2), 1)

# 

# #%%

# dfByDist = df.sort_values(by=['DISTANCE'])
# df12km= dfByDist[dfByDist['DISTANCE'] < 12]

# #%%

# def has(val):
#     try:
#         return 'Готівка, банк.картки' in val 
#     except:
#         return False

# for index, row in df12km.iterrows():
#     has95 = '+' if has(row['A95']) else '-'
#     has95E = '+' if has(row['A95E']) else '-'

#     template = '{:<5}{:<6}{:<6}\n{}'
#     status_str = template.format(row['DISTANCE'], f'95({has95})', f'95E({has95E})', row['ADDRESS'])
#     print(status_str)
#     print('-'*80)
#     #print(row['ADDRESS'], row['DISTANCE'], row['A95'], row['A95E'])

# #%%

# dfByDist[dfByDist['A95'].apply(has) | dfByDist['A95E'].apply(has)].head()

# #%%
# dfByDist[dfByDist['A95'].apply(has) | dfByDist['A95E'].apply(has)].iloc[0]

# #%%

# dfByDist['A95'].value_counts()
# #%%
# if __name__ == '__main__':
#     main()




# # %%
# import sqlite3
# # %%
# from fetcher import model
# # %%

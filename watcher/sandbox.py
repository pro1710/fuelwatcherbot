#%%
import helpers
import pandas as pd
from fetcher.entities.types import Fuel

from config import user_location
#%%






#%%

df = pd.read_pickle('../../data/wog/last.pkl')

mk1 = helpers.Coords(**user_location)
def foo(lat2, long2):
        mk2 = helpers.Coords(latitude=lat2, longitude=long2)
        return round(helpers.Stats.distance(mk1, mk2), 1)

df['DISTANCE'] = df.apply(lambda r: foo(r['LATITUDE'], r['LONGITUDE']), axis=1)
dfByDist = df.sort_values(by=['DISTANCE'])
df12km= dfByDist[dfByDist['DISTANCE'] < 12]

def has(val):
    try:
        return 'Готівка, банк.картки' in val 
    except:
        return False



dfByDist[dfByDist['A95'].apply(has)].head()








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




# %%

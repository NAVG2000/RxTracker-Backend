from pymongo import MongoClient
from pprint import pprint

from drugClass import drugObj
import datetime

client = MongoClient('mongodb://localhost:27017/')
client.drop_database('vascepa')
db = client.vascepa


def populate(db, df):
    db.weekly.insert_many(df.to_dict('records'))


df = drugObj('Vascepa', 500, 'updated', False, 156).masterDf
df['Week'] = df.apply(lambda row: datetime.datetime.combine(
    row.Week, datetime.time.min), axis=1)
populate(db, df)


def print_each(collection):
    for document in collection:
        pprint(document)


lt5percent = db.weekly.find(
    {'NRx_Wow_Growth': {"$gte": .025}, 'Month': 12, 'Week_Of_Year': {"$gte": 50}})
print_each(lt5percent)

lt5percentCount = db.weekly.find(
    {'NRx_Wow_Growth': {"$gte": .025}, 'Month': 12, 'Week_Of_Year': {"$gte": 50}}).count()
print(lt5percentCount)

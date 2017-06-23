from pymongo import Connection
from bson.son import SON
from pymongo import MongoClient
import json
import pprint


connection2 = Connection ('localhost', 27017)
db2 = connection2.geoBCN
collection2 = db2.geodatos


barrio = collection2.find_one({
    "properties.BARRI": "08"
})

print(barrio["geometry"])

connection = Connection ('localhost', 27017)
db = connection.CByelp2
collection = db.cbs

pub = collection.find({
    "loc": {"$geoWithin": {'$geometry': barrio['geometry']}}
})

for doc in pub:
     print(doc)
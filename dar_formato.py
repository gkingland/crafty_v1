from pymongo import Connection
import pymongo
import json

# The MongoDB connection info.
connection = Connection('localhost', 27017)
db = connection.geoBCN
collection = db.BarriosBCN

#Formating data from Open Data Barcelona
cursor = collection.find()
for b in cursor:
    datos = b['features']

collection2 = db.geodatos

for dat in datos:
    collection2.insert(dat)
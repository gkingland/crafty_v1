from pymongo import Connection
from bson.son import SON
from pymongo import MongoClient
import json
import pprint
from bson.json_util import dumps
from flask import Flask

app = Flask(__name__)

#Conection to DB with barrios information
def conecction2():
    connection2 = Connection ('localhost', 27017)
    db2 = connection2.geoBCN
    collection2 = db2.geodatos

#conection to DB with yelp information about pubs
def conecction():
    connection = Connection ('localhost', 27017)
    db = connection.CByelp2
    collection = db.cbs
    
    
#for API

#home
@app.route("/")
def hello():
    return "Hello World! CRAFT BEER IS HERE"

#find all the barrios in Barcelona
@app.route("/crafty/V1.0/buscar/barrios")
def buscar_barrios():
    conecction2()
    barrios = collection2.find()
    return dumps(barrios)

#find one specific barrio in Barcelona
@app.route("/crafty/V1.0/buscar/barrios/<barrio_id>")
def buscar_barrios_one(barrio_id):
    conecction2()
    barrio_one = collection2.find_one({
    "properties.BARRI": str(barrio_id)
    })
    
    if not barrio_one:
        #devolver status 404
        return ("BARRIO NO ENCONTRADO") 
        
    else:
        return dumps(barrio_one)

#find all craft beer pubs in Barcelona
@app.route("/crafty/V1.0/buscar/pubs")
def buscar_pubs():
    conecction()
    pubs = collection.find()
    return dumps(pubs)

#find one specific pub in Barcelona
@app.route("/crafty/V1.0/buscar/pubs/<pub_id>")
def buscar_pubs_one(pub_id):
    conecction()
    pub_one = collection.find_one({
    "id": pub_id
    })
    
    if not pub_one:
        #devolver status 404
        return ("BAR NO ENCONTRADO") 
        
    else:
        return dumps(pub_one)

#find one specific barrio and all the pubs within
@app.route("/crafty/V1.0/buscar/barrios/<barrio_id>/pubs")
def buscar_barrios_pubs(barrio_id):
    
    #conecction to the barrios DB
    conecction2()
    
    #find one specific barrio information
    barrio = collection2.find_one({
    "properties.BARRI": str(barrio_id)
    })
   
    if not barrio:
        #devolver status 404
        return ("BARRIO NO ENCONTRADO") 
        
    else:
        
        #conecction to the pubs DB
        conecction()
    
        #find all the pubs inside the polygon above
        pubs = collection.find({
            "loc": {"$geoWithin": {'$geometry': barrio['geometry']}}
            })
    
        a = list (pubs)
        if len(a) == 0:
            return ("NINGUN REGISTRO ENCONTRADO")
        else:
            return dumps(a)
    

if __name__ == "__main__":
    app.run()
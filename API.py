from pymongo import Connection
from bson.son import SON
from pymongo import MongoClient
import json
import pprint
from bson.json_util import dumps
from flask import Flask
from flask.ext.autodoc import Autodoc

app = Flask(__name__)
auto = Autodoc(app)

#Conection to DB with barrios information
def conecction2():
    connection2 = Connection('localhost', 27017)
    db2 = connection2.geoBCN
    collection2 = db2.geodatos
    return (collection2)

#conection to DB with yelp information about pubs
def conecction():
    connection = Connection('localhost', 27017)
    db = connection.CByelp2
    collection = db.cbs
    return (collection)

#for API

#home
@app.route("/")
@auto.doc()
def hello():
    """Home page, muestra mensaje de bienvenida"""
    return "Hello World! CRAFT BEER IS HERE"

#find all the barrios in Barcelona
@app.route("/Crafty/V1.0/buscar/barrios")
@auto.doc()
def buscar_barrios():
    """Busca todos los barrios, devuelve todos los barrios que existen en la base de datos"""
    collection2 = conecction2()
    barrios = collection2.find()
    return dumps(barrios)

#find one specific barrio in Barcelona
@app.route("/Crafty/V1.0/buscar/barrios/<barrio_id>")
@auto.doc()
def buscar_barrios_one(barrio_id):
    """Busca un barrio, devuelve un barrio correspondiente con el barrio_id especificado"""
    collection2 = conecction2()
    barrio_one = collection2.find_one({
    "properties.BARRI": str(barrio_id)
    })

    if not barrio_one:
        #devolver status 404
        return ("BARRIO NO ENCONTRADO")

    else:
        return dumps(barrio_one)

#find all craft beer pubs in Barcelona
@app.route("/Crafty/V1.0/buscar/pubs")
@auto.doc()
def buscar_pubs():
    """Busca un pub, devuelve todos los pubs que existen en la base de datos"""
    collection = conecction()
    pubs = collection.find()
    return dumps(pubs)

#find one specific pub in Barcelona
@app.route("/Crafty/V1.0/buscar/pubs/<pub_id>")
@auto.doc()
def buscar_pubs_one(pub_id):
    """Busca un pub, devuelve un pub correspondiente con el pub_id especificado"""
    collection = conecction()
    pub_one = collection.find_one({
    "id": pub_id
    })

    if not pub_one:
        #devolver status 404
        return ("BAR NO ENCONTRADO")

    else:
        return dumps(pub_one)

#find one specific barrio and all the pubs within
@app.route("/Crafty/V1.0/buscar/barrios/<barrio_id>/pubs")
@auto.doc()
def buscar_barrios_pubs(barrio_id):
    """Busca un pubs en un barrio, devuelve un todos los pubs dentro del barrio correspodiente al barrio_id especificado"""
    #conecction to the barrios DB
    collection2 = conecction2()

    #find one specific barrio information
    barrio = collection2.find_one({
    "properties.BARRI": str(barrio_id)
    })

    if not barrio:
        #devolver status 404
        return ("BARRIO NO ENCONTRADO")

    else:

        #conecction to the pubs DB
        collection = conecction()

        #find all the pubs inside the polygon above
        pubs = collection.find({
            "loc": {"$geoWithin": {'$geometry': barrio['geometry']}}
            })

        a = list (pubs)
        if len(a) == 0:
            return ("NINGUN REGISTRO ENCONTRADO")
        else:
            return dumps(a)

# Documentation
@app.route('/docs')
def documentation():
    return auto.html()

if __name__ == "__main__":
    app.run()


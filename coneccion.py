from pymongo import Connection
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json


# The MongoDB connection info.
connection = Connection('localhost', 27017)
db = connection.CByelp2
db.cbs.ensure_index("id", unique=True, dropDups=True)
collection = db.cbs

terms = ['craft beer', 'cerveza artesanal','brewery', 'microbrewery']

# read API keys
auth = Oauth1Authenticator(

)

#funciona

client = Client(auth)
coordinates= []
todos = []

#Saving important parameters
for term in terms:
    params = {'term': term, 'lang': 'es, en' }
    response = client.search('Barcelona', **params)
    for b in response.businesses:
        #print(b.location.coordinate.__dict__)
        #print(b.address1)
        ref = b.id
        name = b.name
        coord = b.location.coordinate
        coordinates = [coord.longitude, coord.latitude]
        location = b.location.display_address
        phone = b.phone
        rating = b.rating
        business = {'id': ref, 'name': name, 'location': location, 'phone': phone, 'rating': rating, 'loc': coordinates}
        #print(business)
        collection.save(business)
        #todos.append(b)
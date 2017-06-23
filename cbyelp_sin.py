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
# with io.open('config_secret.json') as cred:
#     creds = json.load(cred)
#     auth = Oauth1Authenticator(**creds)
#     client = Client(auth)
auth = Oauth1Authenticator(
    consumer_key="",
    consumer_secret= "",
    token="",
    token_secret=""
)

# esta es la otra forma sin cargarlo con un json
# no eso asi ya esta bien , lo que seguia es la otra forma

#funciona

client = Client(auth)
coordinates= []
todos = []

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
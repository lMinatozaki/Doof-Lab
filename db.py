import pymongo

client = pymongo.MongoClient("localhost", 27017)

db = client['DoofenshmirtzDaniela']

examCollection = db['examenes']
userCollection = db['users']
categoryCollection = db['categorias']
indicationCollection = db['indicaciones']
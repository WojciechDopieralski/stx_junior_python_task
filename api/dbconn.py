import pymongo
import urllib 
import pickle

with open("pass.p", "rb") as f:
    mongo_db_pass = pickle.load(f)

uri = 'mongodb+srv://test_user:{}@stxtest.z2ugu.mongodb.net/stxtest?retryWrites=true&w=majority'.format(urllib.parse.quote(mongo_db_pass))

client = pymongo.MongoClient(uri)

db = client.stxtest

with open('pass_example.p', 'wb') as f:
    pickle.dump("example_pass", f)
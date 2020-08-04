import pymongo
import urllib 

uri = 'mongodb+srv://test_user:{}@stxtest.z2ugu.mongodb.net/stxtest?retryWrites=true&w=majority'.format(urllib.parse.quote('STx2020Test@$'))

client = pymongo.MongoClient(uri)

db = client.stxtest


from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client.Test
users = db["Users"]

users.insert_one({
                    'username':"Test",
                    'password':"0106",
                    'sentences':"",
                    'tokens':5
                })
import pymongo
import bcrypt
from urllib.parse import urlparse
import getpass
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://bhanu:iamBhanu%40911@passwordmanager.5wgae8x.mongodb.net/?retryWrites=true&w=majority&appName=passwordmanager"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.passwords_db
app_users = db.app_users
passwords = db.passwords

current_user_id = None 
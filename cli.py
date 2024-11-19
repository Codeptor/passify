import pymongo
import bcrypt
from urllib.parse import urlparse
import getpass
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = 
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

def register():
    username = input("Enter app username: ")
    password = getpass.getpass("Enter app password: ")

    user = app_users.find_one({"username": username})
    if user:
        print("Error: Username already exists!")
        return
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    app_users.insert_one({"username": username, "password": hashed})
    print("\nRegistration successful!")
    print("Please proceed to login.")

def login():
    global current_user_id

    username = input("\nEnter app username: ")
    password = getpass.getpass("Enter app password: ")

    user = app_users.find_one({"username": username})          
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        print("\nInvalid credentials!")
        return
    
    current_user_id = user['_id']
    print("\nLogged in successfully!")

def add_password():
    platform_link = input("\nEnter platform link (e.g., https://example.com): ")
    platform_name = urlparse(platform_link).netloc.split('.')[0]
    platform_username = input("Enter platform username: ")
    platform_password = getpass.getpass("Enter platform password: ")
    tags = input("Enter comma-separated tags (up to 3): ").split(",")[:3]
    
    passwords.insert_one({
        "platform": platform_name,
        "link": platform_link,
        "username": platform_username,
        "password": platform_password,
        "tags": tags,
        "user_id": current_user_id
    })
    print("\nPassword added successfully!")


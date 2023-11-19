# User/Client/user_info.py
from pymongo import MongoClient
from datetime import datetime
import bcrypt
from config import MONGO_DB_URI
from database.db import DB

class ClientUserInfo:
    def __init__(self, db_instance=None):
        self.db = db_instance or MongoClient(MONGO_DB_URI)['User']  # Replace with your actual database name

    def signup(self, username, email, password):
        collection = self.db['clients']

        if collection.find_one({'username': username}):
            return {'error': "Username already exists. Please choose a different username."}
        else:
           # During Signup
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_document = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow(),
            }
            collection.DB.perform_insert_one(user_document)

            collection.DB.perform_insert_one(user_document)
            return {'user_created': True, 'message': "Account created successfully. You can now log in."}
    
    def authenticate_user(self, username, password, user_type):
        # Import inside the method to avoid circular import
        from User.Client.user_info import ClientUserInfo

        collection = self.db[user_type.lower() + "s"]
        user = collection.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user.get('password', b'').encode('utf-8')):
            return user
        else:
            return {}  # Return an empty dictionary if the user is not found or the password is incorrect

    def login(self, username, password):
        # Import inside the method to avoid circular import
        from User.Client.user_info import ClientUserInfo

        user = self.authenticate_user(username, password)
        if user:
            return {'user_id': str(user['_id']), 'message': f"Login successful. Welcome, {username}!"}
        else:
            return {'error': "Invalid username or password. Please try again."}

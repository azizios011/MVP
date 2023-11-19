# User/Client/base.py
from database.db import DB
from config import MONGO_DB_URI

class ClientBase:
    def __init__(self, db_instance=None):
        # Import ClientUserInfo inside the constructor to avoid circular import
        from User.Client.user_info import ClientUserInfo
        self.user_info = ClientUserInfo()
        self.db = db_instance or DB(MONGO_DB_URI)

    def handle_login_or_signup(self, data):
        # Import ClientUserInfo inside the function to avoid circular import
        from User.Client.user_info import ClientUserInfo
        result = ClientUserInfo().authenticate_user(data['username'], data['password'], data['user_type'])

        if data['action'] == 'login':
            self.db.handle_database(result, data)

        elif data['action'] == 'signup':
            signup_result = ClientUserInfo().signup(data['username'], data['email'], data['password'])

            if 'user_created' in signup_result and signup_result['user_created']:
                result = signup_result
                self.db.handle_database(result, data)

        return result

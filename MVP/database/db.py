import requests
from datetime import datetime

class DB:
    def __init__(self):
        from config import MONGO_DB_URI
        self.connection_string = MONGO_DB_URI
        self.api_url = "https://eu-central-1.aws.data.mongodb-api.com/app/data-jzjrj/endpoint/data/v1"
        self.api_key = "2Du7DLdl6SPgEBqw6RX9vwXFhuapqtVCU1EAwojT5OFs6JNVGK9uZX0gQp0ptQWb"

    def get_collection_name(self, data):
        # Analyze the data to determine its type and return the collection name
        # Replace this logic with your actual type detection mechanism
        if 'user_type' in data:
            return f"{data['user_type'].lower()}s"
        else:
            return "default_collection"

    def authenticate_user(self, username, password, user_type):
        url = f"{self.api_url}/action/findOne"
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Request-Headers": "*",
            "api-key": self.api_key
        }
        data = {
            "collection": f"{user_type.lower()}s",
            "database": "User",
            "dataSource": "Cluster0",
            "query": {"username": username, "password": password}
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result:
                return result
            else:
                return {}  # Return an empty dictionary if the user is not found or the password is incorrect

        except Exception as e:
            print("Error authenticating user using Data API:", e)
            return {}

    def handle_database(self, result, data):
        action = data.get('action')
        user_type = data.get('user_type')

        if action == 'login':
            if 'user_id' in result:
                print("Login data stored successfully.")

        elif action == 'signup':
            if 'user_created' in result and result['user_created']:
                print("Signup data stored successfully.")

                # Use Data API to perform findOne operation
                self.perform_find_one()

    def perform_find_one(self):
        url = f"{self.api_url}/action/findOne"
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Request-Headers": "*",
            "api-key": self.api_key
        }
        data = {
            "collection": "clients",
            "database": "User",
            "dataSource": "Cluster0",
            "projection": {"_id": 1}
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            print("FindOne Result:", result)
        except Exception as e:
            print("Error performing findOne operation using Data API:", e)

    def perform_insert_one(self, data):
        # Get the collection name based on the type of data
        collection_name = self.get_collection_name(data)

        url = f"{self.api_url}/insert"
        headers = {
            "Content-Type": "application/json",
            "Api-Key": self.api_key
        }

        try:
            # Include the collection name in the data being sent to the API
            data_to_insert = {**data, "collection": collection_name}

            response = requests.post(url, json=data_to_insert, headers=headers)
            response.raise_for_status()
            result = response.json()
            print("Insert Result:", result)
        except Exception as e:
            print("Error inserting data using Data API:", e)

        if result.get('status') == 'success':
            print(f"Data inserted successfully. ID: {result.get('inserted_id')}")
            return {'data_inserted': True, 'data_id': result.get('inserted_id')}
        else:
            print("Failed to insert data")
            return {'data_inserted': False, 'error': 'Failed to insert data'}

    def store_signup_data(self, data):
        print("Storing signup data using Data API.")
        url = f"{self.api_url}/insert"  # Adjust the endpoint based on the Data API documentation

        # Assuming 'data' is a dictionary containing signup information
        user_document = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': data.get('password'),
            'created_at': datetime.utcnow().isoformat(),
        }
        print('user_document:', user_document)

        headers = {
            "Content-Type": "application/json",
            "Api-Key": self.api_key
        }

        try:
            response = requests.post(url, json=user_document, headers=headers)
            response.raise_for_status()
            result = response.json()
            print("Insert Result (Signup):", result)
        except Exception as e:
            print("Error inserting data using Data API:", e)

        if result.get('status') == 'success':
            print(f"User created successfully. User ID: {result.get('inserted_id')}")
            return {'user_created': True, 'user_id': result.get('inserted_id')}
        else:
            print("Failed to create user")
            return {'user_created': False, 'error': 'Failed to create user'}

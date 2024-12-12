from pymongo import MongoClient
import os


class Database:
    def __init__(self):
        # Set up the MongoDB client
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        # Access a specific database
        self.db = self.client.get_database(os.getenv("MONGODB_DATABASE"))

        # Access collections within the database
        self.conversations_collection = self.db["conversations"]

    def save_conversation(self, conversation_data):
        try:
            self.conversations_collection.insert_one(conversation_data)
        except Exception as e:
            print(f"An error occurred while saving the conversation: {e}")
            # raise e

    def get_conversations(self):
        return list(self.conversations_collection.find(
            {},
            {"_id": 0}
        ))

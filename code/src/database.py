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
        self.extracted_info_collection = self.db["extracted_info"]

    def save_conversation(self, conversation_data):
        try:
            self.conversations_collection.insert_one(conversation_data)
        except Exception as e:
            print(f"An error occurred while saving the conversation: {e}")
            # raise e

    def get_conversation(self, conversation_id):
        return self.conversations_collection.find_one(
            {"conversation_id": conversation_id}
        )

    def save_extracted_info(self, extracted_info_data):
        try:
            self.extracted_info_collection.insert_one(extracted_info_data)
        except Exception as e:
            print(f"An error occurred while saving the extracted info: {e}")
            # raise e

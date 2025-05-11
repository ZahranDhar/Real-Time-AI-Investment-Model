from pymongo import MongoClient

# Class with run method for stocks processing
class stocksprocessor:

  def run(self):

    # Connect to MongoDB (default port)
    client = MongoClient("mongodb://localhost:27017/")

    # Select a database and collection
    db = client["stocks"]
    collection = db["apiKeys"]

    # Retrieve FINHUB API KEY Document from Database
    apiKeyDocument = collection.find_one({"available":True})

    # Retrieve API Key
    apiKey = apiKeyDocument.get("key")
    
    # Update the Database
    collection.update_one({"key": apiKey},{"$set": {"available": False}})

    print("API Key used:", apiKey)
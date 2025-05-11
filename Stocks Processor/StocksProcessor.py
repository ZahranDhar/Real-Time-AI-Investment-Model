from pymongo import MongoClient

# Class with run method for stocks processing
class stocksprocessor:

  def __init__(self):

    self.apiKey = None
    self.symbol = None
    self.open = None

  def run(self):

    # API KEY Method
    self.retrieveApiKey()

    # Retrieve Symbol Method
    self.retrieveStockSymbol()



  def retrieveApiKey(self):
    
    # Connect to MongoDB (default port)
    client = MongoClient("mongodb://localhost:27017/")

    # Select a database and collection
    db = client["stocks"]
    collection = db["apiKeys"]

    # Retrieve FINHUB API KEY Document from Database
    apiKeyDocument = collection.find_one({"available":True})

    # Retrieve API Key
    self.apiKey = apiKeyDocument.get("key")
    
    # Update the Database
    collection.update_one({"key": self.apiKey},{"$set": {"available": False}})

    print("API Key used:", self.apiKey)



  def retrieveStockSymbol(self):

    # Connect to MongoDB (default port)
    client = MongoClient("mongodb://localhost:27017/")

    # Select a database and collection
    db = client["stocks"]
    collection = db["symbols"]

    # Retrieve Symbol Document from Database
    symbolDocument = collection.find_one({"available":True})

    # Retrieve API Key
    self.symbol = symbolDocument.get("symbol")
    
    # Update the Database
    collection.update_one({"symbol": self.symbol},{"$set": {"available": False}})

    print("Symbol used:", self.symbol)





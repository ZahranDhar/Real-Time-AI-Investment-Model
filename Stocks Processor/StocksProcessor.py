import time
from pymongo import MongoClient
import requests

# Class with run method for stocks processing
class stocksprocessor:

  def __init__(self):

    self.apiKey = None
    self.symbol = None
    self.openPriceInitialized = False
    self.openPrice = None

  def run(self):

    # API KEY Method
    self.retrieveApiKey()

    # Retrieve Symbol Method
    self.retrieveStockSymbol()

    # Process the Stock
    self.processStock()



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



  def processStock(self):

    url = f"https://finnhub.io/api/v1/quote?symbol={self.symbol}&token={self.apiKey}"

    for i in range(60):
      response = requests.get(url)

      if response.status_code == 200:
            
            data = response.json()

            if self.openPriceInitialized == False:
               
              # Open price of the day
              self.openPrice = data.get("o")    
              self.openPriceInitialized = True

            # Live price
            livePrice = data.get("c")  

            # Calculate change percentage
            percentChange = ((livePrice-self.openPrice)/self.openPrice)*100

            if percentChange > 15 or percentChange < -5:

               # Change Symbol   
              self.changeSymbol()
              self.openPriceInitialized = False

      else:
            print("Server Error Occurred")

      # Wait for 1 second
      time.sleep(1)  


  def changeSymbol(self):
     self.retrieveStockSymbol





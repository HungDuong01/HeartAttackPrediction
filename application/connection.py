from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Replace the following URI with your MongoDB Atlas connection string.
# Make sure to replace <username>, <password>, and <cluster-url> with your information.
# Additionally, replace `test` with your database name if different.
MONGO_URI = 'mongodb+srv://cduong:Hungyeuem2001@cluster0.gu7twaw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(MONGO_URI)
db = client.test  # Use the database name you want to connect to.
if __name__ == '__main__':
    app.run(debug=True)
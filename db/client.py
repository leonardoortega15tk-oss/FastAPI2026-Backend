from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

#---BASE DE DATOS LOCAL---
# db_client=MongoClient().local #Si no le pongo nada, por defecto se conecta a LocalHost 

#---BASE DE DATOS REMOTA---
db_client = MongoClient(os.getenv("MONGO_URI")).test_db

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

#---BASE DE DATOS LOCAL---
# db_client=MongoClient().local #Si no le pongo nada, por defecto se conecta a LocalHost 

#---BASE DE DATOS REMOTA---
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("Falta la variable de entorno MONGO_URI")

db_client = MongoClient(MONGO_URI).users_db
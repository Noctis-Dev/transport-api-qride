import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la ruta del archivo de credenciales desde las variables de entorno
SERVICE_ACCOUNT_KEY = os.getenv("SERVICE_ACCOUNT_KEY")

# Inicializar la aplicación de Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)

# Obtener una instancia de Firestore
db = firestore.client()

def get_db():
    return db
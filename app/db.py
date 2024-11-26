import firebase_admin
from firebase_admin import credentials, firestore
import os

# Obtener la ruta del archivo de credenciales desde las variables de entorno
current_directory = os.path.dirname(os.path.abspath(__file__))
service_account_key_path = os.path.join(current_directory, 'qride-22a76-firebase-adminsdk-vc15e-5d8263c05f.json')


# Inicializar la aplicación de Firebase
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred)

# Obtener una instancia de Firestore
db = firestore.client()

def get_db():
    return db
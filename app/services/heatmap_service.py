from prophet import Prophet
from app.db import get_firestore_db, get_realtime_db
from geopy.distance import geodesic
import time
import pandas as pd

class HeatmapService:
    def __init__(self):
        self.db_firestore = get_firestore_db()
        self.db_realtime = get_realtime_db()
        
    def generate_heatmap(self):
        firestore_db = self.db_firestore
        activities_ref = firestore_db.collection('user_activities')
        activities = activities_ref.where('is_active', '==', True).stream()
        
        heatmap_data = {}
        for activity in activities:
            data = activity.to_dict()
            
            # Validar y corregir los valores de latitud y longitud
            latitude = data['latitude']
            longitude = data['longitude']
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                print(f"Coordenadas inválidas: {latitude}, {longitude}")
                continue
            
            # Reemplazar puntos con guion bajo
            location = f"{str(latitude).replace('.', '_')},{str(longitude).replace('.', '_')}"
            found = False
            for loc in heatmap_data:
                if geodesic(loc.replace('_', '.').split(','), location.replace('_', '.').split(',')).kilometers <= 0.1:
                    heatmap_data[loc] += 1
                    found = True
                    break
            if not found:
                heatmap_data[location] = 1
        
        # Imprimir el diccionario heatmap_data para depuración
        print("heatmap_data:", heatmap_data)
        
        # Guardar en Realtime Database
        realtime_db = self.db_realtime
        timestamp = int(time.time())
        heatmap_ref = realtime_db.child('heatmap').child(str(timestamp))
        
        # Imprimir los datos que se van a enviar a Firebase
        print("Datos que se envían a Firebase:", heatmap_data)
        
        heatmap_ref.set(heatmap_data)
        
        
    def predict_user_density(self):
        db = self.db_realtime
        heatmap_ref = db.child('heatmap')
        end_time = int(time.time())
        start_time = end_time - (60 * 60)  # Últimos 60 minutos
        
        # Obtener todas las ubicaciones únicas
        unique_locations = set()
        for timestamp in range(start_time, end_time + 1):
            data = heatmap_ref.child(str(timestamp)).get()
            if data:
                for location in data.keys():
                    unique_locations.add(location)
        
        # Predecir la densidad de usuarios para cada ubicación
        predictions = {}
        for location in unique_locations:
            heatmap_data = []
            for timestamp in range(start_time, end_time + 1):
                data = heatmap_ref.child(str(timestamp)).get()
                if data and location in data:
                    density = data[location]
                    heatmap_data.append({'timestamp': timestamp, 'density': density})
            
            if heatmap_data:
                df = pd.DataFrame(heatmap_data)
                df['ds'] = pd.to_datetime(df['timestamp'], unit='s')
                df['y'] = df['density']
                
                model = Prophet()
                model.fit(df[['ds', 'y']])
                
                future = model.make_future_dataframe(periods=30, freq='T')
                forecast = model.predict(future)
                
                # Obtener el último valor de yhat
                last_prediction = forecast.iloc[-1]
                predictions[location] = last_prediction['yhat']
        
        # Guardar las predicciones en Realtime Database
        predict_heatmap_ref = db.child('predict_heatmap').child(str(end_time))
        predict_heatmap_ref.set(predictions)
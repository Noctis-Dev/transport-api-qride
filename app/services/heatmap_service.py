from prophet import Prophet
import pandas as pd
from app.db import get_firestore_db, get_realtime_db
from geopy.distance import geodesic
import random
import math

class HeatmapService:
    def __init__(self):
        self.db_firestore = get_firestore_db()
        self.db_realtime = get_realtime_db()
        
    def generate_heatmap(self, timestamp):
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
        heatmap_ref = realtime_db.child('heatmap').child(str(timestamp))
        
        # Imprimir los datos que se van a enviar a Firebase
        print("Datos que se envían a Firebase:", heatmap_data)
        
        heatmap_ref.set(heatmap_data)
        
    def predict_user_density(self, timestamp):
        print("Iniciando predicción de densidad de usuarios...")
        db = self.db_realtime
        heatmap_ref = db.child('heatmap')
        end_time = timestamp
        start_time = end_time - (60 * 60)  # Últimos 60 minutos
        
        print(f"Tiempo de inicio: {start_time}, tiempo de fin: {end_time}")
        
        # Obtener todas las ubicaciones únicas y combinar las cercanas
        unique_locations = {}
        for ts in range(start_time, end_time + 1, 60):  # Incrementar de 60 en 60 segundos (1 minuto)
            print(f"Obteniendo datos para timestamp {ts}...")
            data = heatmap_ref.child(str(ts)).get()
            if data:
                print(f"Datos obtenidos para timestamp {ts}: {data}")
                for location, density in data.items():
                    found = False
                    for unique_location in unique_locations.keys():
                        if geodesic(unique_location.replace('_', '.').split(','), location.replace('_', '.').split(',')).kilometers <= 0.1:
                            unique_locations[unique_location] += density
                            found = True
                            break
                    if not found:
                        unique_locations[location] = density
        
        print(f"Ubicaciones únicas obtenidas: {unique_locations}")
        
        
        # Predecir la densidad de usuarios para cada ubicación
        predictions = {}
        for location in unique_locations:
            heatmap_data = []
            for ts in range(start_time, end_time + 1, 60):  # Incrementar de 60 en 60 segundos (1 minuto)
                data = heatmap_ref.child(str(ts)).get()
                if data and location in data:
                    density = data[location]
                    heatmap_data.append({'timestamp': ts, 'density': density})
            
            print(f"Datos de heatmap para la ubicación {location}: {heatmap_data}")
            
            if len(heatmap_data) >= 2:  # Asegurarse de que hay al menos dos puntos de datos
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
            else:
                print(f"No hay suficientes datos para la ubicación {location} para hacer una predicción.")
        
        # Guardar las predicciones en Realtime Database
        predict_heatmap_ref = db.child('predict_heatmap').child(str(end_time))
        
        # Imprimir las predicciones que se van a enviar a Firebase
        print("Predicciones que se envían a Firebase:", predictions)
        
        predict_heatmap_ref.set(predictions)
    
    def generate_random_data(self, timestamp):
        print("Generando datos aleatorios...")
        db = self.db_realtime
        end_time = timestamp
        reference_point = (16.623413, -93.100081)
        lat_range = 0.6 / 111  # 1 km in degrees of latitude
        lon_range = 0.6 / (111 * math.cos(math.radians(reference_point[0])))  # 1 km in degrees of longitude
        
        # Definir 5 ubicaciones fijas dentro de 1 km del punto de referencia
        fixed_locations = [
            (reference_point[0] + lat_range / 2, reference_point[1] + lon_range / 2),
            (reference_point[0] - lat_range / 2, reference_point[1] - lon_range / 2),
            (reference_point[0] + lat_range / 3, reference_point[1] - lon_range / 3),
            (reference_point[0] - lat_range / 3, reference_point[1] + lon_range / 3),
            (reference_point[0], reference_point[1] + lon_range / 4)
        ]
        
        for i in range(30):  # Generar datos para los últimos 30 minutos
            ts = end_time - (i * 60)
            heatmap_data = {}
            for location in fixed_locations:
                latitude, longitude = location
                location_str = f"{str(latitude).replace('.', '_')},{str(longitude).replace('.', '_')}"
                density = random.randint(1, 10)
                heatmap_data[location_str] = density
            
            # Imprimir los datos generados para depuración
            print(f"Datos generados para timestamp {ts}: {heatmap_data}")
            
            # Guardar en Realtime Database
            heatmap_ref = db.child('heatmap').child(str(ts))
            heatmap_ref.set(heatmap_data)
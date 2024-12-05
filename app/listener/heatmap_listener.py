import schedule
import time
import threading
from app.services.heatmap_service import HeatmapService

heatmap_service = HeatmapService()
random_data_generated = False  # Bandera para controlar la ejecución de generate_random_data

def job_generate_heatmap():
    timestamp = int(time.time())
    heatmap_service.generate_heatmap(timestamp)
    
    # Ejecutar generate_random_data una vez después de predict_user_density
    global random_data_generated
    if not random_data_generated:
        heatmap_service.generate_random_data(timestamp)
        random_data_generated = True

def job_predict_user_density():
    timestamp = int(time.time())
    heatmap_service.predict_user_density(timestamp)

def run_scheduler():
    schedule.every(10).seconds.do(job_generate_heatmap)
    # Ejecutar predict_user_density al segundo minuto
    schedule.every(2).minutes.do(job_predict_user_density).tag('initial_predict')
    while True:
        schedule.run_pending()
        time.sleep(1)  # Esperar 1 segundo entre cada verificación de tareas pendientes
        # Verificar si el job 'initial_predict' se ha ejecutado
        if not schedule.get_jobs('initial_predict'):
            # Cancelar el job 'initial_predict' y programar predict_user_density cada media hora
            schedule.clear('initial_predict')
            schedule.every(30).minutes.do(job_predict_user_density)

# Iniciar el hilo del scheduler
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
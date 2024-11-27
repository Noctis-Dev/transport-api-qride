import schedule
import time
import threading
from app.services.heatmap_service import HeatmapService

heatmap_service = HeatmapService()
random_data_generated = False  # Bandera para controlar la ejecución de generate_random_data

def job_generate_heatmap_and_predict():
    global random_data_generated
    timestamp = int(time.time())
    heatmap_service.generate_heatmap(timestamp)
    heatmap_service.predict_user_density(timestamp)
    
    # Ejecutar generate_random_data una vez después de predict_user_density
    if not random_data_generated:
        heatmap_service.generate_random_data(timestamp)
        random_data_generated = True

def run_scheduler():
    schedule.every(1).minutes.do(job_generate_heatmap_and_predict)
    while True:
        schedule.run_pending()
        # Calcular el tiempo restante hasta el próximo minuto
        now = time.time()
        sleep_time = 60 - (now % 60)
        time.sleep(sleep_time)

# Iniciar el hilo del scheduler
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
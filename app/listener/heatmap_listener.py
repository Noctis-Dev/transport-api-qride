import schedule
import time
import threading
from app.services.heatmap_service import HeatmapService

heatmap_service = HeatmapService()

def job_generate_heatmap():
    heatmap_service.generate_heatmap()

def run_scheduler():
    schedule.every(1).minutes.do(job_generate_heatmap)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Iniciar el hilo del scheduler
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
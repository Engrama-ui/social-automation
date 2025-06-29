import time
import requests
from datetime import datetime
from database import db
from models import SystemStatus

class SystemMonitor:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        
    def check_services(self):
        """Verifica lo stato di tutti i servizi"""
        services = [
            "/api/content",
            "/api/engagement",
            "/api/hashtags",
            "/api/platforms"
        ]
        
        results = {}
        for service in services:
            try:
                response = requests.get(f"{self.base_url}{service}/health")
                results[service] = response.status_code == 200
            except:
                results[service] = False
                
        return results
        
    def log_status(self):
        """Registra lo stato del sistema"""
        status = SystemStatus(
            timestamp=datetime.now(),
            services_status=self.check_services(),
            cpu_usage=self._get_cpu_usage(),
            memory_usage=self._get_memory_usage()
        )
        
        db.session.add(status)
        db.session.commit()
        
    def _get_cpu_usage(self) -> float:
        """Ottieni l'utilizzo della CPU"""
        # Implementazione reale userebbe psutil
        return 0.0
        
    def _get_memory_usage(self) -> float:
        """Ottieni l'utilizzo della memoria"""
        # Implementazione reale userebbe psutil
        return 0.0
        
    def run(self):
        """Esegui il monitoraggio continuo"""
        while True:
            self.log_status()
            time.sleep(60)

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run()
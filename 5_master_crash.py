import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time

fruits = [("Pomme", 2), ("Poire", 3), ("Banane", 1), ("Kiwi", 2), ("Mangue", 4)] * 2
results = []
lock = threading.Lock()
TOTAL_FRUITS = len(fruits)

class MasterService(rpyc.Service):
    def exposed_get_task(self):
        with lock:
            if fruits:
                return fruits.pop(0)
            return None

    def exposed_submit_result(self, result):
        with lock:
            results.append(result)

if __name__ == "__main__":
    server = ThreadedServer(MasterService, port=18812)
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    start_time = time.time()
    
    while True:
        with lock:
            if len(results) == TOTAL_FRUITS:
                break
        time.sleep(0.5)
    
    end_time = time.time()
    print(f"Salade terminee en {end_time - start_time:.2f} secondes.")

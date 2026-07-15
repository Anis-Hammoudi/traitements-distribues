import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time

fruits = [(i, name, dur) for i, (name, dur) in enumerate([("Pomme", 2), ("Poire", 3), ("Banane", 1), ("Kiwi", 2), ("Mangue", 4)] * 2)]
TOTAL_FRUITS = len(fruits)

pending_tasks = {}
results = {}
lock = threading.Lock()
TIMEOUT = 6

class MasterService(rpyc.Service):
    def exposed_get_task(self):
        with lock:
            if fruits:
                task = fruits.pop(0)
                pending_tasks[task[0]] = (task, time.time())
                return task
            return None

    def exposed_submit_result(self, task_id, result):
        with lock:
            if task_id in pending_tasks:
                del pending_tasks[task_id]
            results[task_id] = result

def check_timeouts():
    while True:
        time.sleep(1)
        with lock:
            if len(results) == TOTAL_FRUITS:
                break
            
            now = time.time()
            to_requeue = []
            
            for task_id, (task, start_time) in pending_tasks.items():
                if now - start_time > TIMEOUT:
                    to_requeue.append(task_id)
            
            for task_id in to_requeue:
                task, _ = pending_tasks.pop(task_id)
                fruits.append(task)

if __name__ == "__main__":
    server = ThreadedServer(MasterService, port=18812)
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    timeout_thread = threading.Thread(target=check_timeouts)
    timeout_thread.daemon = True
    timeout_thread.start()
    
    start_time = time.time()
    
    while True:
        with lock:
            if len(results) == TOTAL_FRUITS:
                break
        time.sleep(0.5)
    
    end_time = time.time()
    print(f"Salade terminee en {end_time - start_time:.2f} secondes.")

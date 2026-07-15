import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time
import sys
import os

fruits = [(i, name, dur) for i, (name, dur) in enumerate([("Pomme", 2), ("Poire", 3), ("Banane", 1), ("Kiwi", 2), ("Mangue", 4)] * 2)]
TOTAL_FRUITS = len(fruits)

pending_tasks = {}
results = {}
lock = threading.Lock()

TASK_TIMEOUT = 6
GLOBAL_TIMEOUT = 10 # P2 : Timeout global si inactivite totale
last_activity = time.time()

class MasterService(rpyc.Service):
    def exposed_get_task(self):
        global last_activity
        with lock:
            last_activity = time.time() # P2 : Mise a jour de l'activite
            if fruits:
                task = fruits.pop(0)
                pending_tasks[task[0]] = (task, time.time())
                return task
            return None

    def exposed_submit_result(self, task_id, result):
        global last_activity
        with lock:
            last_activity = time.time() # P2 : Mise a jour de l'activite
            if task_id in pending_tasks:
                del pending_tasks[task_id]
            results[task_id] = result
            print(f"Resultat recu pour la tache {task_id}")

def check_timeouts():
    while True:
        time.sleep(1)
        with lock:
            if len(results) == TOTAL_FRUITS:
                break
            
            now = time.time()
            
            # P2: Verification de l'inactivite totale du cluster
            if now - last_activity > GLOBAL_TIMEOUT:
                print("\n[!] ALERTE CRITIQUE : Inactivite totale du cluster depuis plus de 10s.")
                print("[!] Tous les esclaves semblent etre morts. Maitre Zombie evite !")
                print("[!] Annulation de la salade et arret du systeme.")
                os._exit(1) # Arret forcé
            
            to_requeue = []
            for task_id, (task, start_time) in pending_tasks.items():
                if now - start_time > TASK_TIMEOUT:
                    to_requeue.append(task_id)
            
            for task_id in to_requeue:
                task, _ = pending_tasks.pop(task_id)
                fruits.append(task)
                print(f"Timeout (6s) sur la tache {task_id}, remise en file d'attente.")

if __name__ == "__main__":
    server = ThreadedServer(MasterService, port=18814)
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
    print(f"Salade terminee avec succes en {end_time - start_time:.2f} secondes.")

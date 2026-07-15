import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import time

# Format: task_id: (name, duration, [dependencies])
recipe = {
    1: ("Sortir le saladier", 1, []),
    2: ("Eplucher la pomme", 2, [1]),
    3: ("Couper la pomme", 2, [2]),
    4: ("Eplucher la banane", 1, [1]),
    5: ("Couper la banane", 1, [4]),
    6: ("Melanger la salade", 2, [3, 5])
}

tasks = dict(recipe) # Taches en attente
results = {} # Resultats termines
lock = threading.Lock()
TOTAL_FRUITS = len(recipe)

class MasterService(rpyc.Service):
    def exposed_get_task(self):
        with lock:
            if len(results) == TOTAL_FRUITS:
                return ("DONE", None, None)
            
            # Chercher une tache dont toutes les dependances sont dans results
            for task_id, (name, dur, deps) in list(tasks.items()):
                if all(dep in results for dep in deps):
                    del tasks[task_id]
                    return (task_id, name, dur)
                    
            # Si on arrive ici, il y a des taches, mais leurs dependances ne sont pas pretes
            return ("WAIT", None, None)

    def exposed_submit_result(self, task_id, result):
        with lock:
            results[task_id] = result
            print(f"[Master] Resultat recu: {result}")

if __name__ == "__main__":
    server = ThreadedServer(MasterService, port=18813)
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
    print(f"Recette dynamique avec dependances terminee en {end_time - start_time:.2f} s.")

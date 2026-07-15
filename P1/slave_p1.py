import rpyc
import time

def main():
    conn = rpyc.connect("localhost", 18813)
    while True:
        task_id, name, duration = conn.root.get_task()
        
        if task_id == "DONE":
            break # Tout est fini
        elif task_id == "WAIT":
            # Pas de tache prete immediatement, on attend un peu
            time.sleep(1)
            continue
            
        time.sleep(duration)
        conn.root.submit_result(task_id, f"Tache [{name}] preparee")
        
    conn.close()

if __name__ == "__main__":
    main()

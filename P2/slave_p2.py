import rpyc
import time
import random
import sys

def main():
    conn = rpyc.connect("localhost", 18814)
    while True:
        task = conn.root.get_task()
        if not task:
            break
            
        task_id, name, duration = task
        
        # P2 : On simule un crash tres frequent pour forcer la mort du cluster
        if random.random() < 0.4:
            sys.exit(1)
            
        time.sleep(duration)
        conn.root.submit_result(task_id, f"{name} preparee")
        
    conn.close()

if __name__ == "__main__":
    main()

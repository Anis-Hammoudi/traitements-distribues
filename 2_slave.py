import rpyc
import time

def main():
    conn = rpyc.connect("localhost", 18812)
    while True:
        task = conn.root.get_task()
        if not task:
            break
        
        name, duration = task
        time.sleep(duration)
        conn.root.submit_result(f"{name} preparee")
        
    conn.close()

if __name__ == "__main__":
    main()

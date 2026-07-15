import time

fruits = [("Pomme", 2), ("Poire", 3), ("Banane", 1), ("Kiwi", 2), ("Mangue", 4)] * 2

def prepare_fruit(fruit):
    name, duration = fruit
    time.sleep(duration)
    return f"{name} preparee"

def main():
    start_time = time.time()
    results = []
    
    for fruit in fruits:
        results.append(prepare_fruit(fruit))
        
    end_time = time.time()
    print(f"Salade terminee en {end_time - start_time:.2f} secondes.")

if __name__ == "__main__":
    main()

import rpyc
from rpyc.utils.server import ThreadedServer

class MinimalService(rpyc.Service):
    def exposed_get_answer(self):
        return 42

if __name__ == "__main__":
    server = ThreadedServer(MinimalService, port=18812)
    print("Serveur demarre sur le port 18812...")
    server.start()

import socket, threading, os, platform
from server_services import *
from network_services import *

class Server(Server_Services_MixIn, Network_Services_MixIn):
    DIRECTORY  = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == 'Windows': DIRECTORY += '\\storage\\'
    elif platform.system() == 'Linux': DIRECTORY += '/storage'

    FUNCTION_DICTIONARY = {
        "/?": Server_Services_MixIn.command_list(),
        "/f": Server_Services_MixIn.files_on_the_server(),
        "/d": Server_Services_MixIn.send_file_to_client(),
        "/u": Server_Services_MixIn.receive_file_from_client(),
        "/m": Server_Services_MixIn.private_message(),
        "/b": Server_Services_MixIn.broadcast_message(),
        "/q": lambda Server: Server.remove_client_from_the_list(),
        "netcat": Network_Services_MixIn.netcat(),
        "dns": Network_Services_MixIn.dns(),
        "netscan": Network_Services_MixIn.netscan()
        }

    def __init__(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('localhost', 10000))
        self._server_socket.listen(4)
        print(f'\nTHE SERVER IS RUNNING: {self._server_socket.getsockname()}')
        self._clients_list = dict()
        self._lock         = threading.Lock()
        Server.create_directory(Server.DIRECTORY)

    def create_directory(directory):
        try:   os.mkdir(directory)
        except FileExistsError: print('The directory already exist')
        except Exception as error: print(f'{error}')
        else:  print(f'Directory created')

    def receive_client(self):
        while True:
            connection, client_address = self._server_socket.accept()
            print(f'New log in: {client_address}')
            threading.Thread(target=self.handle_client, args=(connection, client_address,)).start()

    def handle_client(self, connection, client_address):
        self.add_client_to_the_list(connection, client_address)
        while True:
            try:
                message = (connection.recv(1024)).decode()
                if message in Server.FUNCTION_DICTIONARY: 
                    result = Server.FUNCTION_DICTIONARY[message]
                else:
                    result = 'Command not found'
                Server.send_to_client(connection, result)
            except Exception as error:
                print('ERROR INSIDE THE LOOP')
                print(error)
                self.remove_client_from_the_list(self, connection, client_address)

    def add_client_to_the_list(self, connection, client_address):
        with self._lock:
            self._clients_list[client_address] = connection

    def remove_client_from_the_list(self, *args):
        connection     = args[0]
        client_address = args[1]
        with self._lock:
            connection.close()
            del self._clients_list[client_address]
    
    def send_to_client(connection, result):
        connection.sendall(result.encode())
    
if __name__ == '__main__':
    server = Server()
    server.receive_client()

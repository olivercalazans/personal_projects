import socket, threading, os, platform
from server_services import *
from network_services import *

class Server(Server_Services_MixIn, Network_Services_MixIn):
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == 'Windows':
        DIRECTORY += '\\storage\\'
    elif platform.system() == 'Linux':
        DIRECTORY += '/storage'

    FUNCTION_DICTIONARY = {
        "/?":        lambda self, args=None: self.command_list(),
        "/exit":     lambda self, args=None: self.remove_client_from_the_list(),
        "/files":    lambda self, args=None: self.files_on_the_server(),
        "/downl":    lambda self, args=None: self.send_file_to_client(),
        "/upl":      lambda self, args=None: self.receive_file_from_client(),
        "/msg":      lambda self, args=None: self.private_message(),
        "/bmsg":     lambda self, args=None: self.broadcast_message(),
        "/netcat":   lambda self, args=None: self.netcat(),
        "/dns":      lambda self, args=None: self.dns(),
        "/portscan": lambda self, args=None: self.portscan(args) if args else 'No host specified'
    }

    def __init__(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('localhost', 10000))
        self._server_socket.listen(4)
        print(f'\nTHE SERVER IS RUNNING: {self._server_socket.getsockname()}')
        self._clients_list = dict()
        self._lock = threading.Lock()
        Server.create_directory(Server.DIRECTORY)

    @staticmethod
    def create_directory(_directory):
        try:   os.mkdir(_directory)
        except FileExistsError: print('The directory already exists')
        except Exception as error: print(f'Error creating directory: {error}')
        else:  print('Directory created')

    @staticmethod
    def separating_function_from_arguments(_string):
        _function_key, _arguments = (_string.split(':', 1) + [None])[:2]
        return _function_key, _arguments

    @staticmethod
    def send_to_client(connection, result):
        connection.sendall(result.encode())

    def receive_client(self):
        while True:
            connection, client_address = self._server_socket.accept()
            print(f'New log in: {client_address}')
            threading.Thread(target=self.handle_client, args=(connection, client_address)).start()

    def handle_client(self, connection, client_address):
        self.add_client_to_the_list(connection, client_address)
        while True:
            try:
                _function, _args = Server.separating_function_from_arguments((connection.recv(1024)).decode())
                if _function in Server.FUNCTION_DICTIONARY:
                    _result = Server.FUNCTION_DICTIONARY[_function](self, _args)
                else:
                    _result = 'Command not found'
                Server.send_to_client(connection, _result)
            except Exception as error:
                print('ERROR INSIDE THE LOOP')
                print(error)
                self.remove_client_from_the_list(connection, client_address)

    def add_client_to_the_list(self, connection, client_address):
        with self._lock:
            self._clients_list[client_address] = connection

    def remove_client_from_the_list(self, connection, client_address):
        with self._lock:
            connection.close()
            del self._clients_list[client_address]

    def private_message(self):
        return "Command not available yet"
    
    def broadcast_message(self):
        return "Command not available yet"

    def command_list(self):
        commands = [
            '/files - Files on the server',
            '/downl - Download from the server',
            '/upl - Upload to the server',
            '/msg - Private message',
            '/bmsg - Broadcast message',
            '/exit - Log out',
            '/netcat',
            '/dns',
            '/portscan - Scan some ports of a server'
        ]
        return Server.convert_to_string(commands)

    @staticmethod
    def convert_to_string(_data):
        return '|'.join(_data)

if __name__ == '__main__':
    server = Server()
    server.receive_client()

import socket, threading, os, platform
from server_services import *
from network_services import *

class Server(Server_Services_MixIn, Network_Services_MixIn):
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == 'Windows': DIRECTORY += '\\server_folder\\'
    elif platform.system() == 'Linux': DIRECTORY += '/server_folder'

    FUNCTION_DICTIONARY = {
        "/?":        lambda self, arguments=None: self.command_list(),
        "/exit":     lambda self, arguments=None: self.remove_client_from_the_list(),
        "/files":    lambda self, arguments=None: self.files_on_the_server(),
        "/downl":    lambda self, arguments=None: self.send_file_to_client(),
        "/upl":      lambda self, arguments=None: self.receive_file_from_client(),
        "/msg":      lambda self, arguments=None: self.private_message(),
        "/bmsg":     lambda self, arguments=None: self.broadcast_message(),
        "/netcat":   lambda self, arguments=None: self.netcat(),
        "/dns":      lambda self, arguments=None: self.dns(),
        "/portscan": lambda self, arguments=None: self.portscan(arguments) if arguments else 'No host specified'
    }

    def __init__(self) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('localhost', 10000))
        self._server_socket.listen(4)
        print(f'\nTHE SERVER IS RUNNING: {self._server_socket.getsockname()}')
        self._clients_list = dict()
        self._lock = threading.Lock()
        Server.create_directory(Server.DIRECTORY)

    @staticmethod
    def create_directory(_directory) -> None:
        try:   os.mkdir(_directory)
        except FileExistsError: print('The directory already exists')
        except Exception as error: print(f'Error creating directory: {error}')
        else:  print('Directory created')

    @staticmethod
    def separating_function_from_arguments(_string) -> list:
        _function_key, _args = (_string.split(':', 1) + [None])[:2]
        return _function_key, _args

    @staticmethod
    def send_to_client(connection, result) -> None:
        connection.sendall(result.encode())

    def receive_client(self) -> None:
        while True:
            connection, client_address = self._server_socket.accept()
            print(f'New log in: {client_address}')
            threading.Thread(target=self.handle_client, args=(connection, client_address)).start()

    def handle_client(self, connection, client_address) -> None:
        self.add_client_to_the_list(connection, client_address)
        while True:
            try:
                _function, _arguments = Server.separating_function_from_arguments((connection.recv(1024)).decode())
                if _function in Server.FUNCTION_DICTIONARY:
                    _result = Server.FUNCTION_DICTIONARY[_function](self, _arguments)
                else:
                    _result = 'Command not found'
                Server.send_to_client(connection, _result)
            except Exception as error:
                print('ERROR INSIDE THE LOOP')
                print(error)
                self.remove_client_from_the_list(connection, client_address)

    def add_client_to_the_list(self, connection, client_address) -> None:
        with self._lock:
            self._clients_list[client_address] = connection

    def remove_client_from_the_list(self, connection, client_address) -> None:
        with self._lock:
            Server.send_to_client(connection, '<close>')
            connection.close()
            del self._clients_list[client_address]

    def private_message(self) -> None:
        return "Command not available yet"
    
    def broadcast_message(self) -> None:
        return "Command not available yet"

    def command_list(self) -> str:
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
    def convert_to_string(_data) -> str:
        return '|'.join(_data)

if __name__ == '__main__':
    server = Server()
    server.receive_client()

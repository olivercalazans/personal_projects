import socket, threading
from server_services import *
from network_services import *

class Server(Server_Services_MixIn, Network_Services_MixIn):
    FUNCTION_DICTIONARY = {
        "/?":        lambda self, arguments=None: self.command_list(),
        "/exit":     lambda self, arguments=None: self.remove_client_from_the_list(arguments) if arguments else None,
        "/files":    lambda self, arguments=None: self.file_list_on_the_server(),
        "/downl":    lambda self, arguments=None: self.send_file_to_client(),
        "/upl":      lambda self, arguments=None: self.receive_file_from_client(),
        "/msg":      lambda self, arguments=None: self.private_message(),
        "/bmsg":     lambda self, arguments=None: self.broadcast_message(),
        "/netcat":   lambda self, arguments=None: self.netcat(),
        "/dns":      lambda self, arguments=None: self.dns(),
        "/portscan": lambda self, arguments=None: self.portscan(arguments) if arguments else 'No host specified'
    }

    FORWARDING_DICTIONARY = {
        "svc": lambda self, *args: self.send_order(*args) if args else '',
        "pvt": lambda self, *args: self.send_private_message(*args) if args else '',
        "bdc": lambda self, *args: self.send_broadcast_message(*args) if args else ''
    }

    def __init__(self) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('localhost', 10000))
        self._server_socket.listen(4)
        print(f'\nTHE SERVER IS RUNNING: {self._server_socket.getsockname()}')
        self._clients_list = dict()
        self._lock = threading.Lock()
        self.create_directory(Server_Services_MixIn.DIRECTORY)

    def receive_client(self) -> None:
        while True:
            connection, client_address = self._server_socket.accept()
            print(f'New log in: {client_address}')
            threading.Thread(target=self.handle_client, args=(connection, client_address)).start()

    def add_client_to_the_list(self, connection, client_address) -> None:
        with self._lock:
            self._clients_list[client_address] = connection

    def remove_client_from_the_list(self, client_address) -> None:
        with self._lock:
            del self._clients_list[client_address]
    
    def close_connection(self, connection, client_address) -> None:
        self.send_order(connection, '<close>')
        self.remove_client_from_the_list(client_address)
        connection.close()

    def handle_client(self, connection, client_address) -> None:
        self.add_client_to_the_list(connection, client_address)
        while True:
            try:
                _function, _arguments = self.separating_function_from_arguments((connection.recv(1024)).decode())
                if _function == '/exit':
                    self.close_connection(connection, client_address)
                    continue
                elif _function in self.get_function_dictionary():
                    _forward_flag, _data = self.get_function_dictionary()[_function](self, _arguments)
                else:
                    _forward_flag, _data = self.add_server_flags('Command not found')
                print(f'{client_address}> {_function}')
                self.get_forward_dictionary()[_forward_flag](self, connection, _data)
            except ConnectionResetError:
                print('The client logout abruptly')
                self.remove_client_from_the_list(client_address)
            except Exception as error:
                print(error)
                self.remove_client_from_the_list(client_address)
    
    @staticmethod
    def separating_function_from_arguments(_string) -> list:
        _function_key, _args = (_string.split(':', 1) + [None])[:2]
        return _function_key, _args
    
    @staticmethod
    def add_server_flags(_data) -> str:
        return 'svc', f'<server>:{_data}'
    
    @staticmethod
    def add_private_message_flags(_data) -> str:
        return 'pvt', f'<users>:{_data}'
    
    @staticmethod
    def add_broadcast_message_flags(_data) -> str:
        return 'bdc', f'<users>:{_data}'
    
    @classmethod
    def get_function_dictionary(cls):
        return cls.FUNCTION_DICTIONARY

    @classmethod
    def get_forward_dictionary(cls):
        return cls.FORWARDING_DICTIONARY
    
    @staticmethod
    def convert_to_string(_data) -> str:
        string = '|'.join(map(str, _data))
        return Server.add_server_flags(string)

    @staticmethod
    def send_order(connection, _result) -> None:
        connection.sendall(_result.encode())
    
    @staticmethod
    def send_private_message(connection, _message) -> None:
        connection.sendall(_message.encode())

    @staticmethod
    def send_broadcast_message(connection, _message) -> None:
        connection.sendall(_message.encode())

    def private_message(self) -> None:
        return "Command not available yet"
    
    def broadcast_message(self) -> None:
        return "Command not available yet"

    def command_list(self) -> str:
        commands = (
            '/files - Files on the server',
            '/downl - Download from the server',
            '/upl - Upload to the server',
            '/msg - Private message',
            '/bmsg - Broadcast message',
            '/exit - Log out',
            '/netcat',
            '/dns',
            '/portscan - Scan some ports of a server'
        )
        return self.convert_to_string(commands)

if __name__ == '__main__':
    server = Server()
    server.receive_client()

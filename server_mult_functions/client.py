import socket, threading, os, platform

class Client:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == 'Windows': DIRECTORY += '\\client_folder\\'
    elif platform.system() == 'Linux': DIRECTORY += '/client_folder'

    FUNCTION_DICTIONARY = {
        "<close>":  lambda self, arguments=None: self.logout(),
        "<server>": lambda self, arguments=None: self.print_messages_from_server(arguments) if arguments else 'Nothing',
        "<client>": lambda self, arguments=None: self.print_messages_from_clients() if arguments else ' '
    }

    def __init__(self, ip='localhost', port=10000) -> None:
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((ip, port))
        self._stop_flag = False
        Client.create_directory(Client.DIRECTORY)
        threading.Thread(target=Client.receive_from_server, args=(self,)).start()

    @staticmethod
    def create_directory(_directory) -> None:
        try:   os.mkdir(_directory)
        except FileExistsError: print('The directory already exists')
        except Exception as error: print(f'Error creating directory: {error}')
        else:  print('Directory created')

    def send_messages(self) -> None:
        while not self._stop_flag:
            message = input('>')
            self._connection.sendall(message.encode())

    def receive_from_server(self) -> None:
        try:
            while not self._stop_flag:
                data_from_server = self._connection.recv(1024).decode()
        except:
            ...

    @property
    def logout(self) -> None:
        self._stop_flag = True

    def print_messages_from_server(_message):
        _message = _message.split('|')
        for line in _message:
            print(line)
    
    def print_messages_from_clients():
        ...

if __name__ == '__main__':
    client = Client()
    client.send_messages()

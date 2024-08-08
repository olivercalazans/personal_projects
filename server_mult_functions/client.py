import socket, threading, os, platform, time, sys

class Client:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == 'Windows': DIRECTORY += '\\client_folder\\'
    elif platform.system() == 'Linux': DIRECTORY += '/client_folder'

    FUNCTION_DICTIONARY = {
        "<close>":  lambda self, arguments=None: self.logout(),
        "<server>": lambda self, arguments=None: self.server_messages(arguments) if arguments else ' ',
        "<users>":  lambda self, arguments=None: self.users_messages(arguments) if arguments else ' '
    }

    def __init__(self, ip='localhost', port=10000) -> None:
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((ip, port))
        self._stop_flag = False
        self.create_directory(Client.DIRECTORY)
        threading.Thread(target=self.receive_from_server).start()

    @staticmethod
    def create_directory(_directory) -> None:
        try:   os.mkdir(_directory)
        except FileExistsError: print('The directory already exists')
        except Exception as error: print(f'Error creating directory: {error}')
        else:  print('Directory created')

    def send_messages(self) -> None:
        while not self._stop_flag:
            time.sleep(0.1)
            print('-' * 50)
            message = input('>')
            self._connection.sendall(message.encode())

    def stop_thread(self) -> None:
        self._stop_flag = True

    def receive_from_server(self) -> None:
        try:
            while not self._stop_flag:
                _function, _arguments = self.separating_function_from_arguments(self._connection.recv(1024).decode())
                _result = Client.FUNCTION_DICTIONARY[_function](self, _arguments)
                for line in _result:
                    print(line)
        except Exception as error:
            print(f'ERROR: {error}')

    @staticmethod
    def separating_function_from_arguments(_string) -> list:
        _function_key, _args = (_string.split(':', 1) + [None])[:2]
        return _function_key, _args

    @staticmethod
    def server_messages(_message) -> list:
        return _message.split('|')
    
    @staticmethod
    def users_messages(_message) -> list:
        return list(_message)
    
    def logout(self):
        self.stop_thread()
        sys.exit()
    
if __name__ == '__main__':
    client = Client()
    client.send_messages()

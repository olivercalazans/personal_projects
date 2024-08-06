import socket, threading, os, platform

class Client:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    if platform.system() == 'Windows': DIRECTORY += '\\client_folder\\'
    elif platform.system() == 'Linux': DIRECTORY += '/client_folder'

    FUNCTION_DICTIONARY = {
        "<close>": lambda self: self.logout()
    }

    def __init__(self, ip='localhost', port=10000) -> None:
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((ip, port))
        self._stop_flag = False
        threading.Thread(target=Client.receive_from_server, args=(self,)).start()

    @staticmethod
    def create_directory(_directory) -> None:
        try:   os.mkdir(_directory)
        except FileExistsError: print('The directory already exists')
        except Exception as error: print(f'Error creating directory: {error}')
        else:  print('Directory created')

    def sending_messages(self) -> None:
        while not self._stop_flag:
            message = input('>')
            self._connection.sendall(message.encode())

    @property
    def logout(self) -> None:
        self._stop_flag = True

    def receive_from_server(self) -> None:
        try:
            while not self._stop_flag:
                data_from_server = self._connection.recv(1024).decode()
                data_from_server = data_from_server.split('|')
                for line in data_from_server:
                    print(line)
        except:
            ...


if __name__ == '__main__':
    client = Client()
    client.sending_messages()

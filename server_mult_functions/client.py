import socket, threading, sys

class Client:
    def __init__(self, ip='localhost', port=10000):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((ip, port))
        threading.Thread(target=Client.receive_from_server, args=(self,)).start()

    def sending_messages(self):
        while True:
            message = input('>')
            self._connection.sendall(message.encode())
            if message == '/q':
                Client.closing_connection(self)
                break

    def closing_connection(self):
        self._connection.close()

    def receive_from_server(self):
        while True:
            data_from_server = self._connection.recv(1024).decode()
            data_from_server = data_from_server.split('|')
            for line in data_from_server:
                print(line)


if __name__ == '__main__':
    client = Client()
    client.sending_messages()

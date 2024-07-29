import socket, threading

class Client:
    def __init__(self, ip='localhost', port=10000):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.connect((ip, port))
        threading.Thread(target=Client.receive_from_server, args=(self,)).start()

    def sending_messages(self):
        while True:
            message = input('>')
            self._connection.sendall(message.encode())
            if message == 'EXIT':
                break

    def receive_from_server(self):
        while True:
            data_from_server = self._connection.recv(1024).decode()
            print(data_from_server)

    def closing_connection(self):
        self._connection.close()

if __name__ == '__main__':
    client = Client()
    client.sending_messages()
    client.closing_connection()

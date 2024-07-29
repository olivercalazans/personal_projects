import os

class Server_Services_MixIn:
    def create_directory(directory) -> None:
        try:   os.mkdir(directory)
        except FileExistsError: print('The directory already exist')
        except Exception as error: print(f'{error}')
        else:  print(f'Directory created')
    
    def command_list() -> list:
        return str(['/f - Files on the server',
                '/d - Download from the server',
                '/u - Upload to the server',
                '/m - Private message',
                '/b - Broadcast message',
                '/q - Log out'
               ])
    
    def files_on_the_server():
        ...
    
    def send_file_to_client():
        ...
    
    def receive_file_from_client():
        ...

    def private_message():
        ...
    
    def broadcast_message():
        ...
    
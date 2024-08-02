class Server_Services_MixIn:
    def convert_to_string(data):
        return '|'.join(data)

    def command_list():
        commands = ['/f - Files on the server',
                    '/d - Download from the server',
                    '/u - Upload to the server',
                    '/m - Private message',
                    '/b - Broadcast message',
                    '/q - Log out',
                    '/netcat'
                    'dns',
                    'netscan'
                    ]
        return Server_Services_MixIn.convert_to_string(commands)
    
    def files_on_the_server():
        return "Command not avaliable yet"
    
    def send_file_to_client():
        return "Command not avaliable yet"
    
    def receive_file_from_client():
        return "Command not avaliable yet"

    def private_message():
        return "Command not avaliable yet"
    
    def broadcast_message():
        return "Command not avaliable yet"
    

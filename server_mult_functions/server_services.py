import platform, os

class Server_Services_MixIn:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == 'Windows': DIRECTORY += '\\server_folder\\'
    elif platform.system() == 'Linux': DIRECTORY += '/server_folder/'
    
    @classmethod
    def get_directory(cls) -> str:
        return cls.DIRECTORY

    @staticmethod
    def create_directory(_directory) -> None:
        try:   os.mkdir(_directory)
        except FileExistsError: print('The directory already exists')
        except Exception as error: print(f'Error creating directory: {error}')
        else:  print('Directory created')

    @staticmethod
    def file_list_on_the_server() -> list:
        _file_list = os.listdir(Server_Services_MixIn.get_directory())
        _files_and_sizes = Server_Services_MixIn.process_large_file_list(_file_list)
        return _files_and_sizes

    @staticmethod
    def process_large_file_list(_file_names, _block_size=10) -> list:
        _file_and_size = list()
        for index in range(0, len(_file_names), _block_size):
            _block = _file_names[index:index + _block_size]
            _file_and_size.extend(Server_Services_MixIn.process_file_block(_block))
        return _file_and_size
    
    @staticmethod
    def process_file_block(_file_names) -> list:
        _file_info = list()
        for file in _file_names:
            try: _file_info.append(f'{os.path.getsize(Server_Services_MixIn.get_directory() + file)} - {file}')
            except: continue
        return _file_info

    def send_file_to_client():
        return "Command not avaliable yet"
    
    def receive_file_from_client():
        return "Command not avaliable yet"
    
    def delete_file():
        return "Command not avaliable yet"

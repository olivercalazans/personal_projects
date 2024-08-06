import socket

class Network_Services_MixIn:
    def netcat():
        ...
    
    def dns():
        ...
    
    def portscan(_host) -> list:
        _ip = socket.gethostbyname(_host)
        _ports = { 21  : 'FTP - File Transfer Protocol',  
                   22  : 'SSH - Secure Shell',  
                   23  : 'Telnet',  
                   25  : 'SMTP - Simple Mail Transfer Protocol',   
                   53  : 'DNS - Domain Name System', 
                   80  : 'HTTP - HyperText Transfer Protocol', 
                   110 : 'POP3 - Post Office Protocol version 3', 
                   443 : 'HTTPS - HTTP Protocol over TLS/SSL', 
                   5432: 'PostgreSQL database system', 
                   8080: 'Jakarta Tomcat'
                  }
        try:
            _data = list()
            for port in _ports.keys():
                _portscan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                _portscan_socket.settimeout(3) 
                _result = _portscan_socket.connect_ex((_ip, port))
                _status = 'Closed'
                if _result == 0: _status = 'Opened'
                _data.append(f' Port {port:>4} : {_ports[port]} (STATUS -> {_status})')
                _portscan_socket.close()
            return _data
        except socket.gaierror:
            return 'ERROR: problems with DNS'
        except socket.error:
            return 'ERROR: It was not possible to connect to the server'
    

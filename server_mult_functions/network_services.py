import socket, sys

class Network_Services_MixIn:
    def netcat():
        ...
    
    def dns():
        ...
    
    def netscan():
        strHost = input('\nInforme o nome do HOST ou URL do site: ')
        ipHost  = socket.gethostbyname(strHost)

        lista_de_portas = {   
                  21  : 'FTP - File Transfer Protocol',  
                  22  : 'SSH - Secure Shell',  
                  23  : 'Telnet',  
                  25  : 'SMTP - Simple Mail Transfer Protocol',   
                  53  : 'DNS - Domain Name System', 
                  80  : 'HTTP - HyperText Transfer Protocol', 
                  110 : 'POP3 - Post Office Protocol version 3)', 
                  443 : 'HTTPS - HTTP Protocol over TLS/SSL', 
                  5432: 'PostgreSQL database system', 
                  8080: 'Jakarta Tomcat'
                  }  

        print('-'*100)
        print(f'Escaneando o IP {ipHost}')
        try:
            for porta in lista_de_portas.keys():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3) #.......................................TEMPO, EM SEGUNDOS, PARA O TIMEOUT
                resultados = sock.connect_ex((ipHost, porta)) #............socket.connect() X socket.connect_ex()
                status = 'Fechada'
                if resultados == 0: status = 'Aberta'
                print(f' Porta {porta:>4} : {lista_de_portas[porta]} (STATUS -> {status})')
                sock.close()
        except KeyboardInterrupt:
           print('AVISO: Escaneamento Interrompido (<Ctrl>+<C> Pressionado ...)')
           sys.exit()
        except socket.gaierror:
           print('ERRO: O HOSTNAME não pode ser resolvido...')
           sys.exit()
        except socket.error:
           print('ERRO: Não foi possível conectar no servidor...')
           sys.exit()
        print('-'*100)
    

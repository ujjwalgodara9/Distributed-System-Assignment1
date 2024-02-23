import socket
import random

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            hostname=socket.gethostname()
            ip=socket.gethostbyname(hostname)
            
            s.bind((ip, port))
           
        except OSError:
            return True
        else:
            s.close()
            return False
        
def get_new_port():
    port = 0
    while True:
        port  = random.randint(5000, 6000)
        if not is_port_in_use(port):
            break
    print(port)
    return port



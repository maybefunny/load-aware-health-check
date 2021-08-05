from mylib.constants import *

class Client:
    def __init__(self, addr) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))
        
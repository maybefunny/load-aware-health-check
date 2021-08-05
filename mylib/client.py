from mylib.constants import *

class Client:
    def __init__(self, addr) -> None:
        print("client: trying to connect to " + addr, flush=True)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((addr, port))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))
        
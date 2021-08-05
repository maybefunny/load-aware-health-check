import socket
import sys
import time
import threading

class Client:
    lsock = None
    sock = None
    stat = None
    load = None
    addr = None
    port = None
    def __init__(self, addr, port) -> None:
        self.addr = addr
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_thread = threading.Thread(target=self.client, daemon=True)        
        client_thread.start()
        client_thread.join()

    def client(self) -> None:
        self.sock.settimeout(3)
        self.sock.connect((self.addr, self.port))
        while(True):
            self.sock.sendall(b'5')
            data = self.sock.recv(1024)

            self.stat = data.decode()
            # f = open('index.html', 'w')
            # f.writelines(self.stat)
            # f.close()
            time.sleep(1)

def main():
    # get server address from user
    addr = input("server address (None): ")
    port = 5054
    newport = input("server address (5054): ")
    if(addr == ''):
        print('server address is needed!')
        sys.exit(0)
    if(newport != ''):
        port = int(newport)
    client = Client(addr, port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
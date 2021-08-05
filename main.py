from mylib.constants import *
from mylib.client import Client
from mylib.server import Server

def main():
    # get superior peer address from user
    addr = input("superior peer address (None): ")
    if(addr != ''):
        myp2p.peers.append(addr)
    addr = input("listening address (0.0.0.0): ")
    if(addr == ''):
        addr = '0.0.0.0'
    host = addr
    
    # start server routine
    Server(host, port)

    # connect to superior peer and start client routine
    retrieve()

def retrieve():
    while True:
        try:
            for peer in myp2p.peers:
                if(peer != host):
                    client = Client(peer)
            time.sleep(3)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
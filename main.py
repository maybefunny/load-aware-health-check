from mylib.constants import *
from mylib.client import Client
from mylib.server import Server

peers = ['127.0.0.1']
data = []

def main():
    # get superior peer address from user
    addr = input("superior peer address: ")
    peers.append(addr)
    # connect to superior peer and start client routine
    while True:
        for peer in peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass

    # start server routine

if __name__ == "__main__":
    main()
import selectors
import types
import socket
import threading
import requests
import json
import time
import sys

class Server:
    data = {}
    def __init__(self, host, port) -> None:
        self.sel = selectors.DefaultSelector()
        # ...
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind((host, port))
        self.lsock.listen()
        print('listening on', (host, port))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        serve_thread = threading.Thread(target=self.serve, daemon=True)
        serve_thread.start()
        serve_thread.join()

    def serve(self):
        while True:
            try:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
            except:
                pass
    
    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                if ( sock.getpeername()[0] in self.data ):
                    data.outb += b"true"
                else:
                    data.outb += b"false"
            else:
                print('closing connection to', data.addr)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('echoing', repr(data.outb), 'to', data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def data_handler(self):
        url = 'http://10.199.2.120:9090/api/v1/query?query=topk(1,%20avg%20by%20(instance)%20(100%20-%20rate(node_cpu_seconds_total{mode=%22idle%22}[30s])%20*%20100))'
        while(True):
            r = requests.get(url)
            try:
                if(r.status_code == 200):
                    res = json.loads(r.text)
                    newdata = []
                    for data in res["data"]["result"]:
                        newdata.append(data["metric"]["instance"][:-5])
                    self.data = newdata
            except:
                pass
            time.sleep(10)

def main():
    server = Server('0.0.0.0', 5054)

if __name__ == "__main__":
    main()
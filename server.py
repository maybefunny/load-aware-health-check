import selectors
import types
import socket
import threading
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
                self.data[sock.getpeername()[0]] = int(recv_data.decode())
                if ( sock.getpeername()[0] == min(self.data, key=self.data.get) ):
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

def main():
    server = Server('0.0.0.0', 5054)

if __name__ == "__main__":
    main()
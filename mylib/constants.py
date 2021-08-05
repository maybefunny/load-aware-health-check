import socket 
import threading 
import sys
import time

class p2p:
    peers = []
    data = []
    my_load = 10

    def update_peers(self, new_peers):
        for new_peer in new_peers:
            self.add_peer(new_peer)
    
    def add_peer(self, peer):
        if(peer not in self.peers):
            self.peers.append(peer)

    def remove_peer(self, peer):
        if(peer in self.peers):
            self.peers.remove(peer)

myp2p = p2p()
host = '0.0.0.0'
port = 5054
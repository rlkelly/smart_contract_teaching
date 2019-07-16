from multiprocessing import Process
import json

from flask import Flask, Response
import requests

from blockchain import Blockchain


class Miner(object):
    def __init__(self, blockchain: Blockchain):
        self.peers = []
        self.blockchain = blockchain
        self.paused = False

    def toggle(self):
        self.toggle = not self.toggle

    def add_peer(self, peer):
        self.peers.append(peer)
        self.peers = list(set(self.peers))
        self.validate_peers()
        print('added peer')

    def validate_peer(self, peer):
        r = requests.get(peer + '/ping')
        if r.status_code == 200:
            return True
        return False

    def validate_peers(self):
        self.peers = list(filter(lambda x: self.validate_peer(x), self.peers))

    def send_block_to_peers(self):
        for peer in self.peers:
            block = self.blockchain.prev_blocks[-1]
            print(len(block.dumps()))
            r = requests.put(peer + '/block', json={'block': block.dumps()})
        self.validate_peers()

    def share_peers(self):
        for i in range(len(self.peers)):
            others = [elt for num, elt in enumerate(self.peers) if not num == k]
            for o in others:
                requests.put(self.peers[i] + '/peer', json={'peer': o})

    def update(self, block_data):
        print('Received New Block!')
        block = Block.loads(block_data)
        if block.verify():
            self.blockchain.update(block)

    def mine(self):
        while True:
            print('peers:', self.peers)
            if self.toggle:
                print('TOGGLED!!!')
                # This can be used to periodically trigger things
                self.toggle()

            x: bool = self.blockchain.mine_block()
            if x:
                print('FOUND BLOCK!!!!')
                self.validate_peers()
                self.send_block_to_peers()

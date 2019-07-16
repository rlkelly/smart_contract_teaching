from multiprocessing import Process
import json

from flask import Flask, Response
import requests

from blockchain import Blockchain


app = Flask(__name__)

@app.route('/ping')
def home():
    return 'I am awake still'

@app.route('/add_peer', methods=['PUT'])
def add_peer():
    data = json.dumps(request.json)
    peer = data['peer']

if __name__ == "__main__":
    app.run(debug=True)


class Miner(object):
    def __init__(self, blockchain: Blockchain):
        self.peers = []
        self.blockchain = blockchain
        self.paused = False

    def toggle(self):
        self.toggle = not self.toggle

    def add_peer(self, peer):
        self.peers.append(peer)

    def validate_peer(self, peer):
        r = requests.get(peer + '/ping')
        if r.status_code == 200:
            return True
        return False

    def validate_peers(self):
        self.peers = list(filter(lambda x: self.validate_peer(x), self.peers))

    def send_block_to_peers(self):
        for peer in self.peers:
            r = requests.put(peer + '/block', json=self.blockchain.prev_blocks[-1])

    def mine(self):
        while True:
            print('iter')
            if self.toggle:
                print('TEST!!!')
                # This can be used to periodically trigger things
                self.toggle()

            x = self.blockchain.mine_block()
            if x == True:
                print('FOUND BLOCK!!!!')
                self.validate_peers()
                self.send_block_to_peers(self, self.blockchain.prev_blocks[-1])



if __name__ == '__main__':
    m = Miner(Blockchain())

import json
from multiprocessing import Process
import sys

from flask import Flask, Response, request
import requests

from blockchain import Blockchain
from miner import Miner


app = Flask(__name__)
m = Miner(Blockchain('3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134'))
p = Process(target=m.mine)
p.daemon = True


def reset_process():
    global p
    # This is a kludge.  Why do you think it's a bad idea?
    p.terminate(); p.join()
    p = Process(target=m.mine)
    p.start()


@app.route('/ping')
def home():
    return 'I am awake still'


@app.route('/add_peer', methods=['PUT'])
def add_peer():
    peer = request.json['peer']
    if peer == f'http://127.0.0.1:{sys.argv[1]}':
        return 'Same'
    m.add_peer(peer)
    reset_process()
    return 'Success'


@app.route('/block', methods=['PUT'])
def block():
    block = bytes.fromhex(request.json['block'])
    m.update(block)
    reset_process()


@app.route('/toggle')
def toggle():
    m.toggle()
    reset_process()


if __name__ == "__main__":
    # requests.get('http://127.0.0.1:8000/ping')

    p.start()
    app.run(port=int(sys.argv[1]))

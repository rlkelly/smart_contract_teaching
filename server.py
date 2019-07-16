from multiprocessing import Process
import json

from flask import Flask, Response
import requests

from blockchain import Blockchain
from miner import Miner


app = Flask(__name__)
m = Miner(Blockchain('3a1bcfa12a29a7ed68b1c70743a104cc37e6ae8e2c94653fcc1093707a62c448f98ac599df92d392a9f56c2a46bca5a375b9996f321c490b2e92c7c71cf1e134'))
p = Process(target=m.mine)

@app.route('/ping')
def home():
    return 'I am awake still'

@app.route('/add_peer', methods=['PUT'])
def add_peer():
    data = json.dumps(request.json)
    peer = data['peer']
    m.add_peer(peer)

@app.route('/toggle')
def toggle():
    m.toggle()


if __name__ == "__main__":
    p.start()
    app.run(debug=True)

import install
from uwledclient import WLEDNode
from time import sleep


n = WLEDNode('http://wled.local')

while True:
    n.update().fx('r').pal('r').next().done()
    sleep(10)

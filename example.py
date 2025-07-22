from time import sleep

from uwledclient import WLEDNode

n = WLEDNode('http://wled.local')

while True:
    n.update().fx('r').pal('r').next().done()
    sleep(10)

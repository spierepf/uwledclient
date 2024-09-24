import os
import sys

libpath = 'lib'
sys.path.insert(0, libpath)
if 'lib' not in os.listdir():
    os.mkdir(libpath)

if 'urllib' not in os.listdir(libpath):
    import mip
    mip.install('urllib.urequest', target=libpath)

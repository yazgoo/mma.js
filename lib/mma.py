class Main:
    def __init__(self):
        self.MMAdir="/tmp"
        self.platform="Linux"
        self.ffi = self.lib = []
print("test")
import os
def list_dir(d):
    for f in os.listdir(d):
        full_path = d + "/" + f
        if(f != '.' and f != '..' and os.path.isdir(full_path)):
            list_dir(full_path)
        else:
            print(full_path)
#list_dir(".")
print("===== song ======")
if os.path.exists("in.mid"): os.unlink("in.mid")
print(song)
f = open('in.mma','w')
f.write(str(song))
f.close()
import sys
sys.argv = ["", "in.mma"]
main = Main()
sys.modules['__main__'] = main
sys.modules['_pwdgrp_cffi'] = main
print("test2")
import MMA.main
reload(MMA)
MMA.main.mma_run()
#list_dir(".")
f = open("in.mid", 'r')
import base64
midi = base64.b64encode(f.read())
f.close()

import json
import os.path as os_path

from importlib import import_module
from sys       import path as sys_path

sys_path.append("bin")

from bin import Engine


def getControllers(cfgPath):
    module = import_module(os_path.splitext(os_path.basename(cfgPath))[0])
    ctrl   = {}
    
    for name in dir(module):
        prop = module.__getattribute__(name)

        if callable(prop) and name != "Controller": ctrl[name] = prop

    return ctrl

def __main__():
    with open('GUI.json', 'r') as file: 
        cfg = json.load(file)
    
    sys_path.append(os_path.dirname(os_path.abspath(cfg["controllers_path"]))) 

    ROOT = Engine(cfg, getControllers(cfg["controllers_path"]))

    ROOT.mainloop()


if __name__ == "__main__":
    __main__()

   

    
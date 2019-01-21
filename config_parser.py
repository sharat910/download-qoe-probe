from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config = None 

def get_config():
    global config
    if config is None:
        with open("config.yaml") as f:
            config = load(f,Loader=Loader)
    return config
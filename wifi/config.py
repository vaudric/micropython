import ujson

dcfg = {}

def cfg(action=0):
    global dcfg
    if action == 0:
        with open('config.json', 'r') as f:
            dcfg = ujson.load(f)
    elif action == 1:
        with open('config.json', 'w') as f:
            ujson.dump(dcfg, f)
            
# Read config file
cfg(0)

import json

def Save_picks(picks, filepath):
    with open(filepath, 'w') as f:
        json.dump(picks, f)

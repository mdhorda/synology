import json

def jsonprint(data):
    """
    Prettify JSON dump to stdout
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

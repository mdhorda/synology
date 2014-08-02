import json

def jsonprint(data):
    """
    Prettify JSON dump to stdout
    """
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

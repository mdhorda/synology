import config
import urllib3
import json
from clint.textui import colored

class Syno():
    def __init__(self, host, port='5000'):
        self.host = host
        self.port = port
        self.http = urllib3.PoolManager()
        print(colored.yellow(self.host + ':' + self.port))

    def req(self, api, version='1', method='query', query='all'):
        url = 'http://' + self.host + ':' + self.port +\
              '/webapi/query.cgi?api=' + api + '&version=' + version +\
              '&method=' + method + '&query=' + query
        print(colored.green(url))
        r = self.http.request('GET', url)
        print(colored.blue('status: ') + r.status)
        with open('test.json', 'w') as f:
            f.write(r.data.strip().decode('utf-8'))
        response = json.loads(r.data.strip().decode('utf-8'))

        if response['success'] == True:
            print(colored.green('success'))
            self.jsonprint(response['data'])
        else:
            print(colored.red('failure - ' + response['error']['code']))
            self.jsonprint(response['error'])

    def jsonprint(self, data):
        print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))




if __name__ == '__main__':
    syno = Syno(config.host)
    syno.req('SYNO.API.Info')

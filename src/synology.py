import urllib3
import json
from clint.textui import colored

import config
import errors


class Syno():
    def __init__(self, host, user, passwd, port='5000'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.http = urllib3.PoolManager()
        print(colored.yellow(self.host + ':' + self.port))

    def login(self):
        data = self.req(self.endpoint('SYNO.API.Info', query='SYNO.API.Auth,SYNO.FileStation.'))
        login_endpoint = self.endpoint(
            'SYNO.API.Auth',
            version=str(data['SYNO.API.Auth']['maxVersion']),
            cgi=data['SYNO.API.Auth']['path'][:-4],
            method='login',
            extra={
                'account' : self.user,
                'passwd' : self.passwd,
                'session' : 'FileStation',
                'format' : 'cookie'
            }
        )
        print(colored.magenta(login_endpoint))

    def endpoint(self, api, query='', cgi='query', version='1', method='query', extra={}):
        ret = 'http://' + self.host + ':' + self.port + '/webapi/' + cgi + '.cgi?api='\
              + api + '&version=' +version + '&method=' + method
        if query:
            ret += '&query=' + query

        for key, value in extra.items():
            ret += '&' + key + '=' + value

        return ret

    def req(self, endpoint):
        print()
        print(colored.magenta(endpoint))
        r = self.http.request('GET', endpoint)
        print(colored.blue('http status: ') + r.status)

        if r.status == 404:
            return

        with open('test.json', 'w') as f:
            f.write(r.data.strip().decode('utf-8'))
        response = json.loads(r.data.strip().decode('utf-8'))

        if response['success'] == True:
            print(colored.green('success'))
            return response['data']

        print(colored.red('failure - ' + str(response['error']['code']) +\
	      ' - ' + errors.errors[response['error']['code']]))
        self.jsonprint(response['error'])

    def jsonprint(self, data):
        print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    syno = Syno(config.host, config.user, config.passwd)
    syno.login()
    #syno.req('SYNO.API.Info', query='all')
    #syno.req('SYNO.FileStation.Info', end='info', extra='FileStation/', method='getinfo')

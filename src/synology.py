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
        self.sid = ''
        self.session_name = 'FileStation'
        self.http = urllib3.PoolManager()
        self.login()

    def __del__(self):
        self.logout()

    def login(self):
        data = self.req(self.endpoint('SYNO.API.Info', query='SYNO.API.Auth,SYNO.FileStation.'))
        login_endpoint = self.endpoint(
            'SYNO.API.Auth',
            version=str(data['SYNO.API.Auth']['maxVersion']),
            cgi=data['SYNO.API.Auth']['path'],
            method='login',
            extra={
                'account' : self.user,
                'passwd' : self.passwd,
                'session' : self.session_name,
                'format' : 'sid'
            }
        )
        data2 = self.req(login_endpoint)
        self.sid = data2['sid']

    def logout(self):
        logout_endpoint = self.endpoint(
            'SYNO.API.Auth',
            cgi='auth.cgi',
            method='logout',
            extra={
                'account' : self.user,
                'passwd' : self.passwd,
                'session' : self.session_name
            }
        )
        data = self.req(logout_endpoint)

    def endpoint(self, api, query='', cgi='query.cgi', version='1', method='query', extra={}):
        ret = 'http://' + self.host + ':' + self.port + '/webapi/' + cgi + '?api='\
              + api + '&version=' +version + '&method=' + method
        if query:
            ret += '&query=' + query

        for key, value in extra.items():
            ret += '&' + key + '=' + value

        if self.sid:
            ret += '&_sid=' + self.sid

        return ret

    def req(self, endpoint):
        print()
        print(colored.magenta(endpoint))
        r = self.http.request('GET', endpoint)

        if r.status != 200:
            print('http status: ' + str(r.status))

        if r.status == 404:
            raise NameError('http error' + str(r.status))

        with open('test.json', 'w') as f:
            f.write(r.data.strip().decode('utf-8'))
        response = json.loads(r.data.strip().decode('utf-8'))

        if response['success'] == True:
            print(colored.green('success'))
            if 'data' in response.keys():
                return response['data']
            return ''

        print(colored.red('failure - ' + str(response['error']['code']) +\
	      ' - ' + errors.errors[response['error']['code']]))
        self.jsonprint(response['error'])

    def jsonprint(self, data):
        print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    syno = Syno(config.host, config.user, config.passwd)
    #syno.req('SYNO.API.Info', query='all')
    #syno.req('SYNO.FileStation.Info', end='info', extra='FileStation/', method='getinfo')
    syno.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.List', cgi='FileStation/file_share.cgi', method='list_share')))
    print('hello')

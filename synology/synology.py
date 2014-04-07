import urllib3
import json
import logging

from synology.errors import errors
from synology.utils import jsonprint


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
            extra={ 'session' : self.session_name }
        )
        data = self.req(logout_endpoint)

    def endpoint(self, api, query='', cgi='query.cgi', version='1', method='query', extra={}):
        ret = 'http://' + self.host + ':' + self.port + '/webapi/' + cgi + '?api='\
              + api + '&version=' +version + '&method=' + method
        if query:
            ret += '&query=' + query

        for key, value in extra.items():
            ret += '&' + key + '=' + str(value)

        if self.sid:
            ret += '&_sid=' + self.sid

        return ret

    def req(self, endpoint):
        logging.info('url: ' + endpoint)
        r = self.http.request('GET', endpoint)

        if r.status != 200:
            print('http status: ' + str(r.status))

        if r.status == 404:
            logging.error('404 http error')
            raise NameError('http error' + str(r.status))

        with open('test.json', 'w') as f:
            f.write(r.data.strip().decode('utf-8'))
        response = json.loads(r.data.strip().decode('utf-8'))

        if response['success'] == True:
            logging.info('successfull http request')
            if 'data' in response.keys():
                return response['data']
            return ''

        print('failure - ' + str(response['error']['code']) +\
	      ' - ' + errors[response['error']['code']])
        jsonprint(response['error'])

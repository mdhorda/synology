import json
import logging
import requests

from errors import errors
from utils import jsondump

class Syno():
    def __init__(self, host, user, passwd, port='5000'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.sid = ''
        self.logged_in = False
        self.session_name = 'FileStation'
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
        if not 'code' in data2:
            self.sid = data2['sid']
            self.logged_in = True

    def logout(self):
        logout_endpoint = self.endpoint(
            'SYNO.API.Auth',
            cgi='auth.cgi',
            method='logout',
            extra={ 'session' : self.session_name }
        )
        self.req(logout_endpoint)

    def base_endpoint(self, cgi):
        ret = 'http://' + self.host + ':' + self.port + '/webapi/' + cgi
        return ret

    def endpoint(self, api, query='', cgi='query.cgi', version='1', method='query', extra={}):
        ret = self.base_endpoint(cgi) + '?api=' + api + '&version=' +version + '&method=' + method
        if query:
            ret += '&query=' + query

        for key, value in extra.items():
            ret += '&' + key + '=' + str(value)

        if self.sid:
            ret += '&_sid=' + self.sid

        return ret

    def req(self, endpoint):
        logging.info('GET: ' + endpoint)
        r = requests.get(endpoint)
        return self.get_response_data(r)

    def req_binary(self, endpoint):
        logging.info('GET: ' + endpoint)
        r = requests.get(endpoint)
        if self.is_response_binary(r):
            return r.content
        self.get_response_data(r)
        return None

    def req_post(self, endpoint, data, files):
        logging.info('url: ' + endpoint)
        try:
            r = requests.post(endpoint, data=data, files=files)
        except:
            return None
        return self.get_response_data(r)

    def get_response_data(self, response):
        if response.status_code != 200:
            logging.error('http status: ' + str(response.status_code))

        try:
            response_json = json.loads(response.text.strip().decode('utf-8'))
        except:
            return response.content

        if response_json['success'] == True:
            if 'data' in response_json.keys():
                return response_json['data']
            return ''

        logging.error('failure - ' + str(response_json['error']['code']) +\
	      ' - ' + errors[response_json['error']['code']])
        return jsondump(response_json['error'])

    def is_response_binary(self, response):
        return 'text/plain' not in response.headers['content-type']

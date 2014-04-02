import config
import urllib3
import json
from clint.textui import colored

errors = {
    100: 'Unknown error',
    101: 'No parameter of API, method or version',
    102: 'The requested API does not exist',
    103: 'The requested method does not exist', 
    104: 'The requested version does not support the functionality',
    105: 'The logged in session does not have permission',
    106: 'Session timeout',
    107: 'Session interrupted by duplicate login' 
#400 Invalid parameter of file operation 
#401 Unknown error of file operation 
#402 System is too busy 
#403 Invalid user does this file operation 
#404 Invalid group does this file operation 
#405 Invalid user and group does this file operation 
#406 Can’t get user/group information from the account server 
#407 Operation not permitted 
#408 No such file or directory 
#409 Non-supported file system 
#410 Failed to connect internet-based file system (ex: CIFS) 
#411 Read-only file system 
#412 Filename too long in the non-encrypted file system 
#413 Filename too long in the encrypted file system 
#414 File already exists 
#415 Disk quota exceeded 
#416 No space left on device 
#417 Input/output error 
#418 Illegal name or path 
#419 Illegal file name 
#420 Illegal file name on FAT file system 
#421 Device or resource busy 
#599 No such task of the file operation 
}

class Syno():
    def __init__(self, host, port='5000'):
        self.host = host
        self.port = port
        self.http = urllib3.PoolManager()
        print(colored.yellow(self.host + ':' + self.port))

    def req(self, api, end='query', extra='', version='1', method='query', query=''):
        url = 'http://' + self.host + ':' + self.port +\
              '/webapi/' + extra + end + '.cgi?api=' + api + '&version=' + version +\
              '&method=' + method
        if query:
            url += '&query=' + query
        print(colored.green(url))
        r = self.http.request('GET', url)
        print(colored.blue('http status: ') + r.status)

        if r.status == 404:
            return

        with open('test.json', 'w') as f:
            f.write(r.data.strip().decode('utf-8'))
        response = json.loads(r.data.strip().decode('utf-8'))

        if response['success'] == True:
            print(colored.green('success'))
            self.jsonprint(response['data'])
        else:
            print(colored.red('failure - ' + str(response['error']['code']) +\
		  ' - ' + errors[response['error']['code']]))
            self.jsonprint(response['error'])

    def jsonprint(self, data):
        print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    syno = Syno(config.host)
    #syno.req('SYNO.API.Info', query='all')
    syno.req('SYNO.FileStation.Info', end='info', extra='FileStation/', method='getinfo')

#!/usr/bin/env python

import logging
from clint.textui import colored
from hurry.filesize import size

import config
from synology.filestation import FileStation
from synology.utils import jsonprint


logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

#syno = Syno(config.host, config.user, config.passwd)
#syno.req('SYNO.API.Info', query='all')
#syno.req('SYNO.FileStation.Info', end='info', extra='FileStation/', method='getinfo')
#utils.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.List', cgi='FileStation/file_share.cgi', method='list_share')))
#utils.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.Info', cgi='FileStation/info.cgi', method='getinfo')))

filestation = FileStation(config.host, config.user, config.passwd)

#print(colored.yellow('Get info'))
#jsonprint(filestation.get_info())

#print(colored.yellow('Get shares'))
#jsonprint(filestation.get_shares())

print(colored.yellow('Get list'))
jsonprint(filestation.get_list('/Backups'))

print(colored.yellow('Get dirsize of /Backups/magnau_f'))
print('Size: ' + size(filestation.dir_size('/Backups/magnau_f')))

#print(colored.yellow('Search'))
#filestation.search()

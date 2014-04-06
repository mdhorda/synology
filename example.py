#!/usr/bin/env python

import logging
from clint.textui import colored

import config
from synology.filestation import FileStation
from synology.utils import jsonprint

logging.basicConfig(level=logging.INFO)

#syno = Syno(config.host, config.user, config.passwd)
#syno.req('SYNO.API.Info', query='all')
#syno.req('SYNO.FileStation.Info', end='info', extra='FileStation/', method='getinfo')
#utils.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.List', cgi='FileStation/file_share.cgi', method='list_share')))
#utils.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.Info', cgi='FileStation/info.cgi', method='getinfo')))

filestation = FileStation(config.host, config.user, config.passwd)
print(colored.yellow('Get info'))
jsonprint(filestation.get_info())
print(colored.yellow('Get shares'))
jsonprint(filestation.get_shares())
print(colored.yellow('Get list'))
jsonprint(filestation.get_list('/Backups'))
#print(colored.yellow('Search'))
#filestation.search()

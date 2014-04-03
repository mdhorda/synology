synology
========

Python binding to Synology DSM API.
I refer to the following document to add functions 1 by 1:

- [Synology_File_Station_API_Guide.pdf](http://ukdl.synology.com/download/Document/DeveloperGuide/Synology_File_Station_API_Guide.pdf)

Any help is welcome, please fork this repo and contact me.

Install
-------

```bash
git clone https://github.com/satreix/synology.git
cd synology
virtualenv -p python3 .
source bin/activate

cp src/example_config.py src/config.py
# edit src/config.py

python src/synology.py
```

Usage
-----

```python
logging.basicConfig(level=logging.INFO)

# Instanciate directly a Syno
syno = Syno(config.host, config.user, config.passwd)
syno.req('SYNO.API.Info', query='all')
syno.req('SYNO.FileStation.Info', end='info', extra='FileStation/', method='getinfo')
syno.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.List', cgi='FileStation/file_share.cgi', method='list_share')))
syno.jsonprint(syno.req(syno.endpoint('SYNO.FileStation.Info', cgi='FileStation/info.cgi', method='getinfo')))

# Instanciate a FileStation
filestation = FileStation(config.host, config.user, config.passwd)
filestation.jsonprint(filestation.get_info())
filestation.jsonprint(filestation.get_shares())
```

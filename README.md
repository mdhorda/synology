synology
########

Python binding to Synology DSM API.
I refer to the following document to add functions 1 by 1:

- [Synology_File_Station_API_Guide.pdf](http://ukdl.synology.com/download/Document/DeveloperGuide/Synology_File_Station_API_Guide.pdf)

Any help is welcome, please fork this repo and contact me.

API coverage
============

Implemented
-----------

| Endpoint                         | Description                                                                                                                                                                                          |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SYNO.FileStation.Info            | Provide File Station info                                                                                                                                                                            |
| SYNO.FileStation.List            | List all shared folders, enumerate files in a shared folder,and get detailed file information                                                                                                        |
| SYNO.FileStation.DirSize         | Get the total size of files/folders within folder(s)                                                                                                                                                 |
| SYNO.FileStation.MD5             | Get MD5 of a file                                                                                                                                                                                    |
| SYNO.FileStation.CreateFolder    | Create folder(s)                                                                                                                                                                                     |
| SYNO.FileStation.Rename          | Rename a file/folder                                                                                                                                                                                 |
| SYNO.FileStation.Delete          | Delete files/folders                                                                                                                                                                                 |
| SYNO.FileStation.Search          | Search files on given criteria                                                                                                                                                                       |
| SYNO.FileStation.Thumb           | Get a thumbnail of a file                                                                                                                                                                            |
| SYNO.FileStation.CheckPermission | Check if the file/folder has a permission of a file/folder or not                                                                                                                                    |
| SYNO.FileStation.Upload          | Upload a file                                                                                                                                                                                        |
| SYNO.FileStation.Download        | Download files/folders                                                                                                                                                                               |

TODO
----

| Endpoint                         | Description                                                                                                                                                                                          |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SYNO.FileStation.VirtualFolder   | List all mount point folders of virtual file system, ex: CIFS or ISO                                                                                                                                 |
| SYNO.FileStation.Favorite        | Add a folder to user’s favorites or do operations on user’s favorites                                                                                                                                |
| SYNO.FileStation.Sharing         | Generate a sharing link to share files/folders with other people and perform operations on sharing links                                                                                             |
| SYNO.FileStation.CopyMove        | Copy/Move files/folders                                                                                                                                                                              |
| SYNO.FileStation.Extract         | Extract an archive and do operations on an archive                                                                                                                                                   |
| SYNO.FileStation.Compress        | Compress files/folders                                                                                                                                                                               |
| SYNO.FileStation.BackgroundTask  | Get information regarding tasks of file operations which are run as the background process including copy, move, delete, compress and extract tasks or perform operations on these background tasks. |

Install
=======

```bash
git clone https://github.com/satreix/synology.git
cd synology
virtualenv -p python3 .
source bin/activate

cp example_config.py config.py
# edit config.py

python example.py
```

Usage
=====

```python
import config
from synology.synology import Syno
from synology.filestation import FileStation
from synology.utils import jsonprint

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

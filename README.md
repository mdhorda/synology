synology
========

Python binding to Synology DSM API.
I refer to the following document to add functions 1 by 1:

- [Synology_File_Station_API_Guide.pdf](http://ukdl.synology.com/download/Document/DeveloperGuide/Synology_File_Station_API_Guide.pdf)

Any help is welcome, please fork this repo and contact me.

API coverage
------------

| Endpoint                         | Description                                                                                                                                                                                          | Status |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| SYNO.FileStation.Info            | Provide File Station info                                                                                                                                                                            | ok     |
| SYNO.FileStation.List            | List all shared folders, enumerate files in a shared folder,and get detailed file information                                                                                                        | ok     |
| SYNO.FileStation.Search          | Search files on given criteria                                                                                                                                                                       | todo   |
| SYNO.FileStation.VirtualFolder   | List all mount point folders of virtual file system, ex: CIFS or ISO                                                                                                                                 | todo   |
| SYNO.FileStation.Favorite        | Add a folder to user’s favorites or do operations on user’s favorites                                                                                                                                | todo   |
| SYNO.FileStation.Thumb           | Get a thumbnail of a file                                                                                                                                                                            | todo   |
| SYNO.FileStation.DirSize         | Get the total size of files/folders within folder(s)                                                                                                                                                 | ok     |
| SYNO.FileStation.MD5             | Get MD5 of a file                                                                                                                                                                                    | ok     |
| SYNO.FileStation.CheckPermission | Check if the file/folder has a permission of a file/folder or not                                                                                                                                    | todo   |
| SYNO.FileStation.Upload          | Upload a file                                                                                                                                                                                        | todo   |
| SYNO.FileStation.Download        | Download files/folders                                                                                                                                                                               | todo   |
| SYNO.FileStation.Sharing         | Generate a sharing link to share files/folders with other people and perform operations on sharing links                                                                                             | todo   |
| SYNO.FileStation.CreateFolder    | Create folder(s)                                                                                                                                                                                     | ok     |
| SYNO.FileStation.Rename          | Rename a file/folder                                                                                                                                                                                 | ok     |
| SYNO.FileStation.CopyMove        | Copy/Move files/folders                                                                                                                                                                              | todo   |
| SYNO.FileStation.Delete          | Delete files/folders                                                                                                                                                                                 | ok     |
| SYNO.FileStation.Extract         | Extract an archive and do operations on an archive                                                                                                                                                   | todo   |
| SYNO.FileStation.Compress        | Compress files/folders                                                                                                                                                                               | todo   |
| SYNO.FileStation.BackgroundTask  | Get information regarding tasks of file operations which are run as the background process including copy, move, delete, compress and extract tasks or perform operations on these background tasks. | wip    |

Install
-------

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
-----

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

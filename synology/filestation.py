import os
import time

from synology import Syno

class FileStation(Syno):
    """
    Access synology FileStation informations
    """
    add = 'real_path,size,owner,time,perm'

    def get_info(self):
        """
        Provide File Station information
        """
        return self.req(self.endpoint('SYNO.FileStation.Info',
                        cgi='FileStation/info.cgi', method='getinfo'))

    def list_share(self, writable_only=False, limit=25, offset=0,
                   sort_by='name', sort_direction='asc', additional=False):
        """
        List all shared folders
        """
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='list_share',
            extra={
                'onlywritable': writable_only,
                'limit': limit,
                'offset': offset,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
                'additional': self.add if additional else ''
            }
        ))

    def list(self, path, limit=25, offset=0, sort_by='name',
             sort_direction='asc', pattern='', filetype='all',
             additional=False):
        """
        Enumerate files in a given folder
        """
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='list',
            extra={
                'folder_path': path,
                'limit': limit,
                'offset': offset,
                'sort_by': sort_by,
                'sort_direction': sort_direction,
                'pattern': pattern,
                'filetype': filetype,
                'additional': self.add if additional else ''
            }
        ))

    def get_file_info(self, path, additional=False):
        """
        Get information of file(s)
        """
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='getinfo',
            extra={
                'path': path,
                'additional': self.add if additional else ''
            }
        ))

    def search(self, path, pattern):
        """
        Search for files/folders.
        """
        start = self.req(self.endpoint(
            'SYNO.FileStation.Search',
            cgi='FileStation/file_find.cgi',
            method='start',
            extra={
                'folder_path': path,
                'pattern': pattern
            }
        ))
        if not 'taskid' in start.keys():
            raise NameError('taskid not in response')

        while True:
            time.sleep(0.5)
            file_list = self.req(self.endpoint(
                'SYNO.FileStation.Search',
                cgi='FileStation/file_find.cgi',
                method='list',
                extra={
                    'taskid': start['taskid'],
                    'limit': -1
                }
            ))
            if file_list['finished']:
                result_list = []
                for item in file_list['files']:
                    result_list.append(item['path'])
                return result_list

    def dir_size(self, path):
        """
        Get the accumulated size of files/folders within folder(s).

        Returns:
            size in octets
        """
        start = self.req(self.endpoint(
            'SYNO.FileStation.DirSize',
            cgi='FileStation/file_dirSize.cgi',
            method='start',
            extra={'path': path}
        ))
        if not 'taskid' in start.keys():
            raise NameError('taskid not in response')

        while True:
            time.sleep(10)
            status = self.req(self.endpoint(
                'SYNO.FileStation.DirSize',
                cgi='FileStation/file_dirSize.cgi',
                method='status',
                extra={'taskid': start['taskid']}
            ))
            if status['finished']:
                return int(status['total_size'])

    def md5(self, path):
        """
        Get MD5 of a file.
        """
        start = self.req(self.endpoint(
            'SYNO.FileStation.MD5',
            cgi='FileStation/file_md5.cgi',
            method='start',
            extra={'file_path': path}
        ))
        if not 'taskid' in start.keys():
            raise NameError('taskid not in response')

        while True:
            time.sleep(10)
            status = self.req(self.endpoint(
                'SYNO.FileStation.MD5',
                cgi='FileStation/file_md5.cgi',
                method='status',
                extra={'taskid': start['taskid']}
            ))
            if status['finished']:
                return status['md5']

    def permission(self, path):
        """
        Check if user has permission to write to a path.
        """
        return self.req(self.endpoint(
            'SYNO.FileStation.CheckPermission',
            cgi='FileStation/file_permission.cgi',
            method='write',
            extra={
                'path': path,
                'create_only': 'false'
            }
        ))

    def delete(self, path):
        """
        Delete file(s)/folder(s)
        I'm using ths blocking method for now.
        """
        self.req(self.endpoint(
            'SYNO.FileStation.Delete',
            cgi='FileStation/file_delete.cgi',
            method='delete',
            extra={'path': path}
        ))

    def create(self, path, name, force_parent=True, additional=False):
        """
        Create folders
        This does not support several path/name tupple as the API does
        """
        return self.req(self.endpoint(
            'SYNO.FileStation.CreateFolder',
            cgi='FileStation/file_crtfdr.cgi',
            method='create',
            extra={
                'name': name,
                'folder_path': path,
                'force_parent': force_parent,
                'additional': self.add if additional else ''
            }
        ))

    def rename(self, path, name, additional=False):
        """
        Rename a file/folder
        """
        return self.req(self.endpoint(
            'SYNO.FileStation.Rename',
            cgi='FileStation/file_rename.cgi',
            method='rename',
            extra={
                'name': name,
                'path': path,
                'additional': self.add if additional else ''
            }
        ))

    def thumb(self, path, size='small', rotate='0'):
        """
        Get thumbnail of file.
        """
        return self.req_binary(self.endpoint(
            'SYNO.FileStation.Thumb',
            cgi='FileStation/file_thumb.cgi',
            method='get',
            extra={
                'path': path,
                'size': size,
                'rotate': rotate
            }
        ))

    def download(self, path, mode='open'):
        """
        Download files/folders.
        """
        return self.req_binary(self.endpoint(
            'SYNO.FileStation.Download',
            cgi='FileStation/file_download.cgi',
            method='download',
            extra={
                'path': path,
                'mode': mode
            }
        ))

    def upload(self, path, data, overwrite=True):
        """
        Upload file.
        """
        dir = os.path.dirname(path)
        file = os.path.basename(path)
        return self.req_post(self.base_endpoint('FileStation/api_upload.cgi'),
            data={
                'api': 'SYNO.FileStation.Upload',
                'version': '1',
                'method': 'upload',
                'create_parents': True,
                'overwrite': True if overwrite else None,   # None tells API to throw an error if file exists
                'dest_folder_path': dir,
                '_sid': self.sid
            },
            files={
                'file': (
                    file,
                    data,
                    'application/octet-stream'
                )
            }
        )
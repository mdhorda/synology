import time
import sys
import logging

from synology.synology import Syno


class FileStation(Syno):
    """
    Access synology FileStation informations
    """
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
        extra = {
            'onlywritable': writable_only,
            'limit': limit,
            'offset': offset,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
            'additional': 'real_path,size,owner,time,perm' if additional else ''
        }
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='list_share',
            extra=extra
        ))

    def list(self, path, limit=25, offset=0, sort_by='name',
             sort_direction='asc', pattern='', filetype='all',
             additional=False):
        """
        Enumerate files in a given folder
        """
        extra = {
            'folder_path': path,
            'limit': limit,
            'offset': offset,
            'sort_by': sort_by,
            'sort_direction': sort_direction,
            'pattern': pattern,
            'filetype': filetype,
            'additional': 'real_path,size,owner,time,perm' if additional else ''
        }
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='list',
            extra=extra
        ))

    def get_file_info(self, path, additional=False):
        """
        Get information of file(s)
        """
        extra = {
            'path': path,
            'additional': 'real_path,size,owner,time,perm' if additional else ''
        }
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='getinfo',
            extra=extra
        ))

    # TODO
    def search(self):
        raise NotImplementedError()

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
            print('.', end='')
            sys.stdout.flush()
            if status['finished']:
                print()
                return int(status['total_size'])

    def md5(self, path):
        """
        Get MD5 of a file. 

        Return:
            file MD5
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
            print('.', end='')
            sys.stdout.flush()
            if status['finished']:
                print()
                return status['md5']

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
        extra = {
            'name': name,
            'folder_path': path,
            'force_parent': force_parent,
            'additional': 'real_path,size,owner,time,perm' if additional else ''
        }
        return self.req(self.endpoint(
            'SYNO.FileStation.CreateFolder',
            cgi='FileStation/file_crtfdr.cgi',
            method='create',
            extra=extra
        ))

    def rename(self, path, name, additional=False):
        """
        Rename a file/folder
        """
        extra = {
            'name': name,
            'path': path,
            'additional': 'real_path,size,owner,time,perm' if additional else ''
        }
        return self.req(self.endpoint(
            'SYNO.FileStation.Rename',
            cgi='FileStation/file_rename.cgi',
            method='rename',
            extra=extra
        ))

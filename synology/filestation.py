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
        Provide File Station information.

        Availability: Since DSM 4.3
        Version: 1
        """
        return self.req(self.endpoint('SYNO.FileStation.Info',
                        cgi='FileStation/info.cgi',
                        method='getinfo'))

    def get_shares(self, writable_only=False, limit=25, offset=0,
                   sort_by='name', sort_direction='asc', additional=False):
        """
        List all shared folders.
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

    # TODO
    def get_object_info(self):
        raise NotImplementedError()

    # TODO
    def get_list(self, path, limit=25, offset=0, sort_by='name',
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

    def dir_size(self, path):
        """
        Get the accumulated size of files/folders within folder(s).
        This is a non-blocking API. You need to start it with the start method.
        Then, you should poll requests with the status method to get progress
        status or make a request with stop method to cancel the operation.

        Availability: Since DSM 4.3
        Version: 1

        Return: size in octets
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

    # TODO
    def search(self):
        raise NotImplementedError()

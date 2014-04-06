from synology.synology import Syno


class FileStation(Syno):
    def get_info(self):
        return self.req(self.endpoint('SYNO.FileStation.Info',
                        cgi='FileStation/info.cgi',
                        method='getinfo'))

    def get_shares(self, writable_only=False, limit=25, offset=0,
                   sort_by='name', sort_direction='asc', additional=False):
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

    # TODO
    def search(self):
        raise NotImplementedError()

from synology import Syno


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
            # FIXME 'real_path,owner,time,perm,volume_status'
            'additional': additional
        }
        return self.req(self.endpoint(
            'SYNO.FileStation.List',
            cgi='FileStation/file_share.cgi',
            method='list_share',
            extra=extra
        ))

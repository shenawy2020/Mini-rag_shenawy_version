from helpers.config import get_settings,Settings
class BaseDataModesl:
    def __init__(self,dbclient:object):
        self.dbclient=dbclient
        self.app_settings=get_settings()

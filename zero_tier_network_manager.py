
import network_manager

class NetworkManager(network_manager.NetworkManager):
    def __init__(self):
        self.process = {
            'dir': 'C:\\ProgramData\\ZeroTier\\One',
            'exe': 'zerotier-one_x64.exe',
        }

    def init(self):
        return False
    
    def getUrl(self) -> str:
        return '172.128.123.2:8211'

import network_manager

from process import ProcessBuilder

class NetworkManager(network_manager.NetworkManager):
    def __init__(self):
        self.main_process = (ProcessBuilder()
                        .with_name('zerotier')
                        .with_dir('C:\\ProgramData\\ZeroTier\\One')
                        .with_exe('zerotier-one_x64.exe')
                        .build())
        
        self.ip_address = None

    def init(self) -> bool:
        memory_usage = self.main_process.get_memory_usage()
        return memory_usage > 0
    
    def stop(self) -> bool:
        return True
    
    def getUrl(self) -> str:
        if self.ip_address is None:
            with open('.tunnel.info', '+r') as file:
                ip_address = file.read().strip().split('\n')[0].strip()
                [address, port] = ip_address.split(':')
                self.ip_address = address + ':' + (port if port is not None else '8211')
        
        return self.ip_address
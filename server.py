import subprocess
import time
import os

import config

from process import Process, ProcessBuilder
from zero_tier_network_manager import NetworkManager

class Server:
    def __init__(self, processes):
        self.network_manager = NetworkManager()
        self.root_dir = os.getcwd()

        self.processes = []
        for process_name in config.process_names:
            process_data = config.server_processes[process_name]
            process_builder = (ProcessBuilder()
                .with_name(process_name)
                .with_exe(process_data['exe'])
                .with_dir(process_data.get('dir'))
                .with_to_kill(process_data.get('toKill')))
            
            if process_data.get('backup'):
                process_builder = (process_builder
                    .with_target_path(process_data['backup']['targetPath'])
                    .with_destination_path(process_data['backup']['destinationPath']))  

            self.processes.append(process_builder.build())

    def is_running(self):
        return self.get_status() == "UP"

    def _get_process_usage(self, process: Process):
        return [process.name, process.get_memory_usage()]
    
    def get_status(self, include_details: bool = False) -> str:
        running_processes = []
        down_processes = []

        for process in self.processes:
            [process_name, memory_usage] = self._get_process_usage(process)

            if memory_usage == 0:
                down_processes.append(process_name)
                continue

            running_processes.append([process_name, memory_usage])

        if len(down_processes) == 0:
            return 'UP' if not include_details else 'UP ' + ' and '.join(
                [i[0] for i in running_processes]) + ' using ' + \
                                                    str(round(sum([i[1] for i in running_processes]), 2)) + ' MiB'
        
        return 'Down' if not include_details else 'Down ' + ' and '.join(down_processes) + \
                                                  (' are ' if len(down_processes) > 1 else ' is ') + 'not running'

    def get_server_url(self) -> str:
        return self.network_manager.getUrl()
    
    def stop_server(self, should_use_force: bool=False) -> bool:
        if not self.is_running() and not should_use_force:
            return True
        
        for process in self.processes:
            process.stop(should_use_force)
        
        self.network_manager.stop()
        time.sleep(1)
        self.run_backup()

        return not self.is_running()

    def set_address(self, address: str):
        self.network_manager.set_address(address)

    def start_server(self) -> str:
        if not self.is_running():
            if not self.network_manager.init():
                return 'Network Manager not running'
            
            up_processes = []
            for process in self.processes:
                process.start()
                up_processes.append(process.name)
            time.sleep(1)

            return 'Started ' + ' and '.join(up_processes)+' please wait a while for connecting to it: ' + self.get_server_url()
        
        return 'Server is already UP'

    def run_backup(self) -> str:
        if self.is_running():
            return 'Server is running, please stop it before running a backup to avoid data cooorruption'
        
        success_counter = 0
        failed_backups = []
        for process in self.processes:
            result = process.do_backup()
            
            if not result:
                failed_backups.append(process.name)

        if len(failed_backups):
            return 'Some processes backup failed: ' + ', '.join(failed_backups)
        
        return 'Success! All backups resulted on a sucess'

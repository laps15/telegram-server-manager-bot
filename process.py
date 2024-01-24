import subprocess
import os

import config
import security

from shutil import copyfile, make_archive
from datetime import datetime

class Process:
    mode = 'regular'    
    dir = None
    to_kill = None

    backup_configured = False
    target_path = None
    destination_path = None

    def get_memory_usage(self):
        process_name = (self.to_kill or self.exe).split('.')[0]
        cmd = 'powershell "gps -name ' + process_name + ' -ErrorAction SilentlyContinue | select PM"'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        mem_in_use = 0
        for line in proc.stdout:
            if not line.decode()[0].isspace():
                mem_in_use = int(line.decode().rstrip()) / 1024 / 1024

        return mem_in_use

    def get_cmd(self):
        return self.exe

    def start(self):
        cmd = self.get_cmd()
        dir = self.dir or '.'

        prev_dir = os.getcwd()
        os.chdir(dir)
        self._proc_data = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        os.chdir(prev_dir)

        return self._proc_data
    
    def get_stop_cmd(self, should_use_force: bool):
        process_name = self.to_kill or self.exe
        kill_cmd = 'taskkill ' + ('/F ' if should_use_force else ' ') + '/IM  ' + process_name
        return kill_cmd

    def stop(self, should_use_force: bool = False) -> bool:
        cmd = self.get_stop_cmd(should_use_force)
        cmd_result = subprocess.call(cmd)

        return cmd_result == 0

    def get_backup_filename(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def do_backup(self) -> bool:
        if not self.backup_configured:
            return True
        
        destination = os.path.join(self.destination_path, self.get_backup_filename())
        target = os.path.join(self.target_path)

        if os.path.exists(destination + '.zip') or not os.path.exists(self.target_path):
            return False
        
        print ('Will backup path:', target, 'into', destination+'.zip')
        make_archive(destination, 'zip', target)
        
        return True

class ProcessBuilder:
    def __init__(self):
        self.instance = Process()

    def with_name(self, name):
        self.instance.name = name
        return self
    
    def with_dir(self, dir):
        self.instance.dir = dir
        return self
    
    def with_exe(self, exe):
        self.instance.exe = exe
        return self
    
    def with_to_kill(self, to_kill):
        self.instance.to_kill = to_kill
        return self
    
    def as_admin(self):
        self.instance.mode = 'admin'
        return self

    def with_target_path(self, target_path: str):
        self.instance.backup_configured = True
        self.instance.target_path = target_path
        return self

    def with_destination_path(self, destination_path: str):
        self.instance.backup_configured = True
        self.instance.destination_path = destination_path
        return self
    
    def build(self) -> Process:
        return self.instance
        
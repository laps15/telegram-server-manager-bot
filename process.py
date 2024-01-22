import subprocess
import os

class Process:        
    def get_memory_usage(self):
        process_name = (self.to_kill or self.exe).split('.')[0]
        cmd = 'powershell "gps -name ' + process_name + ' -ErrorAction SilentlyContinue | select PM"'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        mem_in_use = 0
        for line in proc.stdout:
            if not line.decode()[0].isspace():
                mem_in_use = int(line.decode().rstrip()) / 1024 / 1024

        return mem_in_use

    def start(self):
        cmd = self.exe
        dir = self.dir or '.'

        prev_dir = os.getcwd()
        os.chdir(dir)
        self.proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        os.chdir(prev_dir)

        return self.proc
    
    def stop(self, should_use_force: bool) -> bool:
        process_name = self.to_kill or self.exe
        cmd = 'taskkill ' + ('/F ' if should_use_force else ' ') + '/IM  ' + process_name
        cmd_result = os.system(cmd)

        return cmd_result == 0


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
    
    def build(self):
        return self.instance
        
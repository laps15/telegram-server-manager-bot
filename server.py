import subprocess
import json
import time
import os

import config


class Server:
    def __init__(self, processes):
        self.running_processes = {}
        self.root_dir = os.getcwd()
        self.processes = processes
        self.active_processes = {}
        self.init_tunnel_data_file()

    def is_running(self):
        return self.get_status() == "UP"

    def get_status(self, include_details: bool = False) -> str:
        running_processes = []
        down_processes = []

        for process in self.processes:
            memory_usage = self.get_application_memory_usage(process)
            if memory_usage == 0:
                down_processes.append(process)
                continue
            running_processes.append([process, memory_usage])

        if len(down_processes) == 0:
            return 'UP' if not include_details else 'UP ' + ' and '.join(
                [i[0] for i in running_processes]) + ' using ' + \
                                                    str(round(sum([i[1] for i in running_processes]), 2)) + ' MiB'
        return 'Down' if not include_details else 'Down ' + ' and '.join(down_processes) + \
                                                  (' are ' if len(down_processes) > 1 else ' is ') + 'not running'

    @staticmethod
    def get_application_memory_usage(process_name: str):
        cmd = 'powershell "gps -name ' + process_name + ' -ErrorAction SilentlyContinue | select PM"'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        mem_in_use = 0
        for line in proc.stdout:
            if not line.decode()[0].isspace():
                mem_in_use = int(line.decode().rstrip()) / 1024 / 1024
        return mem_in_use

    def init_tunnel_data_file(self):
        os.system("curl --silent --output .tunnel.info http://localhost:4040/api/tunnels")
        with open('.tunnel.info', 'r') as file:
            try:
                data = json.load(file)
            except:
                file.close()
                return
            url = data['tunnels'][0]['public_url'].split('//')[1]
            file.close()

        with open('.tunnel.info', 'w') as file:
            file.write(url)
            file.close()

    def get_server_url(self) -> str:
        if self.is_running():
            with open('.tunnel.info') as f:
                return f.read()
        return 'Server is not running.'

    def stop_server(self, should_use_force: bool=False) -> bool:
        for process in self.processes:
            cmd = 'taskkill ' + ('/F ' if should_use_force else ' ') + '/IM  ' + process + '.exe'
            os.system(cmd)
        return self.is_running()

    def start_server(self) -> str:
        if not self.is_running():
            for process in self.processes:
                process_cmd = config.server_processes[process]
                self.running_processes[process] = self.start_process(process_cmd)
            time.sleep(1)
            self.init_tunnel_data_file()
            return 'Started ' + ' and '.join(self.processes)+' please wait a while for connecting to it: ' + self.get_server_url()
        return 'Server is already UP'

    def start_process(self, process_cmd):
        cmd = process_cmd['exe']
        dir = process_cmd['dir'] or '.'
        os.chdir(dir)
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        os.chdir(self.root_dir)
        return proc

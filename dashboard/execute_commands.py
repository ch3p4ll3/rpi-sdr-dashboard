import subprocess
from json import load
from typing import List
from systemd_service import Service


class ExecuteCommands:
    def __manage_service(self, service_name: str, to_start: bool):
        daemon = Service(service_name)

        if to_start:
            daemon.start()
        else:
            daemon.stop()
        
    def __run_command(self, command):
        process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        stdout, stderr = process.communicate()
        print(stdout)
    
    def __get_commands(self, command_name: str):
        configs = []
        
        with open("./configurations.json", "r") as f:
            configs = load(f).get('system', [])

        for config in configs:
            if config.get("name", "") == command_name:
                return config.get('commands', [])
        
        return []
    
    def run_commands(self, command_name: str):
        commands = self.__get_commands(command_name)

        for i in commands:
            self.__run_command(i)

    def __run_sequence(self, command_sequence: List[str], is_start: bool):
        for command in command_sequence:
            self.__manage_service(command, is_start)

    def __get_service_sequence(self, service_name: str, is_for_start: bool = True):
        configs = []
        
        with open("./configurations.json", "r") as f:
            configs = load(f).get('services', [])

        for config in configs:
            if config.get("name", "") == service_name:
                if is_for_start:
                    return config.get('start_commands', [])
                return config.get('stop_commands', [])
        
        return []

    def stop_service(self, service_name: str):
        sequence = self.__get_service_sequence(service_name, False)
        self.__run_sequence(sequence, False)

    def start_service(self, service_name: str):
        sequence = self.__get_service_sequence(service_name, True)
        self.__run_sequence(sequence, True)
    
    def check_hostapd_is_active(self):
        try:
            process = subprocess.Popen(['sudo', 'systemctl', 'status', 'hostapd'], stdout=subprocess.PIPE)
            output, err = process.communicate()
            return 'Active: active (running)' in str(output)
        except Exception as e:
            print(e)
            return False

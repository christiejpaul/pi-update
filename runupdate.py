import paramiko
import os
from textfsm import TextFSM

private_key_path = os.path.expanduser("~/.ssh/id_rsa")
HOSTFILE = 'HOSTNAMES.txt' #Update later
username = 'pi'

with open ('match-text.textfsm') as f:
    template = TextFSM(f)

def check_updates(hostname, username, private_key_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client.connect(hostname, username=username, pkey=private_key)
        commands = [
            'pihole -up',
            'sudo apt update'
            #'sudo apt list --upgradable'
        ]

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            print (f'command : {command}')
            result = stdout.read().decode('utf-8')
            f_result = template.ParseText(result)
            print (f'Parsing = {f_result}')
            if ('up to date' in f_result):
                print ('Packages up to date')
            error  = stderr.read().decode('utf-8')
            #print (f'Result > {result}\nError > {error}')
    except Exception as e:
        print (f'Error occured at {e}')
    finally:
        client.close()

def install_updates():
    pass

def get_hostnames():
    pass

def main():
    with open(HOSTFILE, 'r') as file: [check_updates(host.strip(),username, private_key_path) for host in file]

if __name__ == "__main__":
    main()

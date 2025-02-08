import paramiko
import os

private_key_path = os.path.expanduser("~/.ssh/id_rsa")
# HOSTFILE = 'HOSTNAMES.txt' #Update later

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
            error  = stderr.read().decode('utf-8')
            print (f'Result > {result}\nError > {error}')
            #print (stderr.read().decode('utf-8'))
    except Exception as e:
        print (f'Error occured at {e}')
    finally:
        client.close()

def install_updates():
    pass

def get_hostnames():
    pass

def main():
    hostnames = ['pihole01', 'pihole02']
    username  = 'pi'
    for host in hostnames:
        check_updates(host, username, private_key_path) 

if __name__ == "__main__":
    main()

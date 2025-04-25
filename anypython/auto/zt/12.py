import paramiko
import os

# VMware connection details
vmware_host = '172.30.1.39'
username = 'test'
password = '1234'
remote_folder = '/home/test/python'
local_folder = 'D:\짬통\172.30.1.39'

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(vmware_host, username=username, password=password)

# Use SFTP to transfer files
sftp = ssh.open_sftp()
for filename in sftp.listdir(remote_folder):
    remote_file = os.path.join(remote_folder, filename)
    local_file = os.path.join(local_folder, filename)
    sftp.get(remote_file, local_file)  # This will overwrite existing files

sftp.close()
ssh.close()
import paramiko

hostname = '192.168.0.21'
username = 'jetson'
password = 'jetson'
remote_file_path = '/home/jetson/Documents/People-Counter-V1/Personas'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, username=username, password=password)

# Lee el valor actual de Personas desde el archivo remoto
_, stdout, _ = client.exec_command(f'cat {remote_file_path}')
current_value = int(stdout.read().decode().strip())

print(f'Valor actual de Personas: {current_value}')

new_value = current_value + 1

# Modifica el valor en el archivo remoto
_, stdout, _ = client.exec_command(f'echo "{new_value}" > {remote_file_path}')

print(f'Nuevo valor de Personas: {new_value}')

client.close()



"""
En este codigo
_, stdout, _ = client.exec_command(f'cat {remote_file_path}')
current_value = int(stdout.read().decode().strip())

Que es lo que hace esta dos parte
"""





from pycomm3 import LogixDriver
import time

# Dirección IP del controlador
ip_controlador = '10.0.0.20'

# Número de salida que deseas controlar
salida = 1 

# Tiempo en segundos que la salida estará encendida
tiempo_encendido = 3  

# Establecer conexión con el controlador
with LogixDriver(ip_controlador) as plc:
    # Encender salida
    plc.write(f'output:{salida}', True)  
    print(f'Salida {salida} encendida.')
   
    # Esperar el tiempo especificado
    time.sleep(tiempo_encendido)

    # Apagar salida
    plc.write(f'output:{salida}', False)  
    print(f'Salida {salida} apagada.')
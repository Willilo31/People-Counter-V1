import schedule
import time
import subprocess
import psutil
from datetime import datetime
import os 

def reiniciar_programa():
    subprocess.Popen(['pkill', '-f', 'python3 People_Counter_VS_Jetson_1.py'])
    print("Programa cerrado")
    time.sleep(5)

def verificar_proceso():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python3' and proc.info['cmdline'] is not None and len(proc.info['cmdline']) > 1:
            # print(f"PID: {proc.info['pid']}, Nombre: {proc.info['name']}, Comando: {' '.join(proc.info['cmdline'])}")
            if proc.info['cmdline'][1] == 'People_Counter_VS_Jetson_1.py':
                return True
    return False

def Registro():
    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('Registro_de_parada.txt', 'a') as archivo:
        archivo.write(f"Fecha de detenida: {hora}\n")


if __name__ == "__main__":
    schedule.every().day.at("09:42").do(reiniciar_programa)
    tiempo_de_verificacion = 0
    while True:        
        if tiempo_de_verificacion == 10:
            # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            schedule.run_pending()

            if not verificar_proceso():
                print("No estaba encendido")
                subprocess.Popen(['python3', 'People_Counter_VS_Jetson_1.py'])
                Registro()
            else:
                print("--------")
            tiempo_de_verificacion = 0
        
        print(tiempo_de_verificacion)
        tiempo_de_verificacion +=1
        time.sleep(1)

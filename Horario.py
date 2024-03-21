import schedule
import time
import subprocess
import psutil
from datetime import datetime

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

if __name__ == "__main__":
    schedule.every().day.at("14:34").do(reiniciar_programa)
    tiempo_de_verificacion = 0
    while True:        
        if tiempo_de_verificacion == 10:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            schedule.run_pending()

            if not verificar_proceso():
                print("No estaba encendido")
                subprocess.Popen(['python3', 'People_Counter_VS_Jetson_1.py'])
            else:
                print("NOOOOOOOOOOO")
            tiempo_de_verificacion = 0
        
        print(tiempo_de_verificacion)
        tiempo_de_verificacion +=1
        time.sleep(1)


"""
import pandas as pd
from openpyxl import Workbook

# Leer el archivo Excel
df = pd.read_excel('Prueba.xlsx', sheet_name='03.18.24')

# Buscar la fila y columna donde se encuentra "FGs"
fila, columna = None, None
for index, row in df.iterrows():
    for col_index, value in enumerate(row):
        if value == 'Sub Assy':
            fila, columna = index + 2, col_index + 1

if fila is not None and columna is not None:
    nuevo_excel = Workbook()
    nuevo_sheet = nuevo_excel.active

    nuevo_sheet.append(['Line', 'Pack', 'Code'])
   
    # Iterar sobre las filas debajo de FGs y guardar la información hasta encontrar filas vacías
    for i in range(fila, len(df)):
        line_value = df.iloc[i, columna -1]
        pack_value = df.iloc[i, columna]
        code_value = df.iloc[i, columna + 1]

        # Reemplazar valores vacíos o '00:00:00' por 'N/A'
        line_value = 'N/A' if pd.isna(line_value) else line_value
        pack_value = 'N/A' if pd.isna(pack_value) else pack_value
        code_value = 'N/A' if pd.isna(code_value) else code_value

        # Verificar si se encuentran las tres casillas en blanco (Line, Pack, Code)
        if line_value == 'N/A' and pack_value == 'N/A' and code_value == 'N/A':
            break

        nuevo_sheet.append([line_value, pack_value, code_value])

    nuevo_excel.save('Intento_01.xlsx')
    print('Se ha creado y guardado el nuevo archivo Excel.')
else:
    print('No se encontró el valor "FGs" en el archivo.')



    Quisiera que ahora este archivo en la misma fila que esta ubicado FGs siga  hacia delante hasta otra columna donde aparecen las fechas, en total son 6 fechas



"""
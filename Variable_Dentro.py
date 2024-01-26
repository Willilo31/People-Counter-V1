
with open('Personas', 'r') as archivo:
    numero = int(archivo.read().strip())

numero += 1

with open('Personas', 'w') as archivo:
    archivo.write(numero)

print("Número actualizado:", numero)


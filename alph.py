import os 

mi_ruta = os.getcwd()
archivos = os.listdir(mi_ruta)

cont = 0

for i in range(len(archivos)):
    if (archivos[i][-2:] == 'py') or (archivos[i][-3:] == 'csv'):
        print(i,archivos[i])
        cont = cont + 1 

n = -1
while n >= len(archivos) or n < 0:
    print("Ingrese un valor entre",0,"y" , cont-1 )
    try:
        n = int(input("Digite el número del archivo que quiere abrir: "))
    except:
        print("Ingrese valor numerico")   

print("El archivo selecionado es: ",archivos[n])
file = open(archivos[n], "r")
print(file.read())
file.close()
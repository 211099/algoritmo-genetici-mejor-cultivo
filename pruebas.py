import pandas as pd
import random 
from decimal import Decimal

data_diccionario = {}
poblacion_puntuacion = {}

def leer_dataset():
    
    # Cargar el archivo CSV
    df = pd.read_csv('dataset.csv')

    # Recortar el DataFrame para que comience desde la segunda fila (índice 1)
    df = df.iloc[0:]

    # Crear una lista que almacena cada fila como una lista de listas
    data = []
    for index, row in df.iterrows():
        # Convierte cada fila en una lista y divide las cadenas en subcadenas basándose en las comas
        converted_row = []
        for item in row:
            if isinstance(item, int):
                converted_row.append([item])
            elif isinstance(item, str) and ',' in item:
                converted_row.append(item.split(','))
            else:
                converted_row.append([item])
        data.append(converted_row)
    auxiliar_id = 1
    for row in data:
        data_diccionario[auxiliar_id] = row
        auxiliar_id += 1

leer_dataset()

#datos ingresados por el usuario
cultivo_requerido = ""
#       O
tipo_cultivo = "" ## se puede cambiar a un arreglo por si gusta agregar mas de un tipo de cultivo

tipo_suelo = "Limoso" 
ph_suelo = "6"
nutrientes_suelo = ["Nitrógeno", "Fósforo"]
clima = "Templado"
riesgo_conocido = ["Insectos","sequia"] 
fecha_siembra = "abril"

poblacion = [[11, 1, 9, 5, 10, 4, 7, 2, 15, 3, 13, 9, 16, 17, 8, 12, 14],[16, 12, 3, 5, 10, 4, 7, 2, 15, 3, 13, 9, 16, 17, 8, 12, 14],[2, 1, 3, 5, 10, 4, 7, 2, 15, 3, 13, 9, 16, 17, 8, 12, 14]]
print (data_diccionario)
def valorar_elemetos():
    global poblacion
    index = 0
    for individuo in poblacion:
        obtener_puntuacion(individuo,index)
        index += 1

def obtener_puntuacion(individuo, index):
    global data_diccionario
    cantidad_cultivos = 3 #esta variable se usara en la interface grafica 
    puntuacion = Decimal(0)
    for elemento in individuo[:cantidad_cultivos]:    
        #verifica si el cultivo es igual al que el usuario desea o si es algun tipo de cultivo que desea 
        if cultivo_requerido == data_diccionario[elemento][0][0].replace(" ", "") or any(tipo in tipo_cultivo for tipo in data_diccionario[elemento][2]) : ### complete
            puntuacion += Decimal('1')
        else:
            puntuacion -= Decimal('0.1')

        #verificar que el tipo de suelo sea el correcto
        if tipo_suelo in data_diccionario[elemento][1]: ### complete
            puntuacion += Decimal('1')
        else:
            puntuacion -= Decimal('0.2')
        
        #si los cultivos son compatibles
        for identificador in individuo[:cantidad_cultivos]: ### complete
            if identificador == elemento:
                pass
            else:
                if any(compatible.replace(" ","") in data_diccionario[elemento][0][0].replace(" ", "") for compatible in data_diccionario[identificador][6]):
                    puntuacion += Decimal('0.5')
                else:
                    puntuacion -= Decimal('0.15')

                #aprovechando el for y que la situcion es similar se hace aqui la comprobacion de los efectos que generan las plantas y si afectan positivamente a las otras
                for efectos_generado in data_diccionario[elemento][8]:#efectos generados fila 9 del dataset
                    # print(str(efectos_generado),":", data_diccionario[identificador][9]) solo es para ver so coincide despues lo borro 
                    # print(str(efectos_generado) in data_diccionario[identificador][9])
                    if str(efectos_generado) in data_diccionario[identificador][9]:##afecta
                        puntuacion += Decimal('0.2')

        #verificar que el ph este dentro del rango
        ph_rango = [float(num) for num in data_diccionario[elemento][7][0].replace(" ", "").split("-")]    
        if ph_rango[0] <= float(ph_suelo) <= ph_rango[1]:###completo
            puntuacion += Decimal('2')
        else:
            puntuacion -= Decimal('0.6')
                
        #verificar que los nutrientes sean los necesario
        for nutriente in data_diccionario[elemento][5]:
            if nutriente.replace(" ","") in  nutrientes_suelo:
                puntuacion += Decimal('0.3')
            else:
                puntuacion -= Decimal('0.1')
        
        #verificar si el clima es compatible con los cultivos
        if clima in data_diccionario[elemento][3]:
            puntuacion += Decimal('0.8')
        else:
            puntuacion -= Decimal('0.5')
        
        #  #verifica si hay relacion entre los riesgos que puede sifrir las plantas 
        for riesgo in data_diccionario[elemento][4]:
            riesgo = riesgo.replace(" ","")
            if riesgo in riesgo_conocido:
                puntuacion -= Decimal('0.18')
            else:
                puntuacion += Decimal('0.2')
        
         #verificar que la temporada sea la correcta
        if fecha_siembra.replace(" ","") in data_diccionario[elemento][10]:
            puntuacion += Decimal('1.0')
        else:
            puntuacion -= Decimal('0.8')

    print(Decimal(puntuacion))
    poblacion_puntuacion[index] = puntuacion
    

    


valorar_elemetos()
print(poblacion_puntuacion)
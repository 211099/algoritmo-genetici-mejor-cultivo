import pandas as pd
import random 
from decimal import Decimal

data = [] #datos
data_diccionario = {} #datos con identificador (en in diccionario)
poblacion = [] #la poblacion 
arreglo_claves = [] #arreglo que contiene las claves de data diccionario
poblacion_puntuacion = {}
mejor_individuo = []
promedio_individuo = []
peor_individuo = []

#configuracion del algoritmo
cantidad_poblacion_inicial = 6 ###valor que despues sera sustituido / se ingresara desde la interface
poblacion_maxima = 100
posibilidad_cruza = 1 ###valor que despues sera sustituido / se ingresara desde la interface
posibilidad_mut_individuo = 35 ###valor que despues sera sustituido / se ingresara desde la interface
posibilidad_mut_gen = 30
cantidad_iteraciones = 1000

  ###valor que despues sera sustituido / se ingresara desde la interface
cantidad_cultivos = 6 ###esta variable se usara en la interface grafica 

#datos ingresados por el usuario
cultivo_requerido = "Maiz"
tipo_suelo = "" 
ph_suelo = ""
nutrientes_suelo = ""
clima = ""
riesgo_conocido = "" 

def leer_dataset():
    # Cargar el archivo CSV
    df = pd.read_csv('dataset.csv')

    # Recortar el DataFrame para que comience desde la segunda fila (índice 1)
    df = df.iloc[1:]

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

def generar_n_individuos():
    global arreglo_claves 
    poblacion_inicial = []
    auxiliar_claves = []

    for clave in data_diccionario:
        arreglo_claves.append(clave)
    auxiliar_claves = arreglo_claves

    for i in range(cantidad_poblacion_inicial):
        auxiliar_claves_copia = auxiliar_claves[:] # crea una copia de la lista
        random.shuffle(auxiliar_claves_copia) # baraja la copia
        poblacion_inicial.append(auxiliar_claves_copia) # agrega la copia barajada a la población inicial

    return poblacion_inicial

def seleccion_parejas():   
    numero_de_parejas = (len(poblacion) / 2) + 0.5 
    parejas_aleatorias = [random.sample(poblacion, 2) for _ in range(int(numero_de_parejas))]

    return parejas_aleatorias

def cruza(parejas_aleatorias):
    hijos = []
    punto_de_cruce = 2 ###
    for pareja in parejas_aleatorias:
        if random.randrange(0,100) <= posibilidad_cruza:
            tupla1 = pareja[0]
            tupla2 = pareja[1]
            # Realizar el cruce por punto fijo
            hijo1 = tupla1[:punto_de_cruce] + tupla2[punto_de_cruce:]
            hijo2 = tupla2[:punto_de_cruce] + tupla1[punto_de_cruce:]
            # Agregar las tuplas cruzadas a la lista de parejas cruzadas
            hijos.append(hijo1)
            hijos.append(hijo2)

    print('hijos')
    for hijo in hijos:
        print(hijo)
    print('\n')
    
    return hijos

def reparar_hijos(hijos_sin_reparar):
    global arreglo_claves
    hijos_reparados = []
    for hijo in hijos_sin_reparar:
       
        auxiliar_elementos_usados = []

        for elemento in hijo:
            print(elemento)
            if elemento in auxiliar_elementos_usados:
                for claves in arreglo_claves: 
                    if claves not in auxiliar_elementos_usados:
                        auxiliar_elementos_usados.append(claves)
                        break
            else:       
                auxiliar_elementos_usados.append(elemento)
        hijos_reparados.append(auxiliar_elementos_usados)

    print('\n hijos reparados')
    for hijo in hijos_reparados:
        print(hijo)
    return hijos_reparados    

def mutacion(hijos_reparados):
    
    for hijo in hijos_reparados:
        arreglo_posiciones_que_mutan=[]

        if random.randint(0,100) <= posibilidad_mut_individuo :

            for posicion in range(len(hijo)):

                if random.randint(0,100) <= posibilidad_mut_gen :
                    arreglo_posiciones_que_mutan.append(posicion)

            Intercambio_de_valor(arreglo_posiciones_que_mutan, hijo)

        else:
            poblacion.append(hijo)

def Intercambio_de_valor(arreglo_posiciones_que_mutan,hijo):
    global poblacion
    
    for elemento in arreglo_posiciones_que_mutan:
        posicion_random = random.randint(0,len(hijo) - 1)
        print(posicion_random)
        print(len(hijo))
     
        #hace referencia al valor que va cambiar
        elemento_1 = hijo[elemento]#2
        #hace referencia al valor por el que se cambiara
        elemento_2 = hijo[posicion_random]#3

        hijo[elemento] = elemento_2

        hijo[posicion_random] = elemento_1

    poblacion.append(hijo)

def valorar_elemetos():
    global poblacion
    print(poblacion)
    index = 0
    for individuo in poblacion:
        obtener_puntuacion(individuo,index)
        index += 1
    print

def obtener_puntuacion(individuo, index):
    global data_diccionario
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

def ordenar_poblacion():
    global poblacion
    print(len(poblacion_puntuacion))
    print(len(poblacion))
    diccionario_ordenado = {k: v for k, v in sorted(poblacion_puntuacion.items(), key=lambda item: item[1], reverse=True)}
    print(diccionario_ordenado)
    print(poblacion,'\n')
    print(len(diccionario_ordenado))
    print(len(poblacion))
    
    poblacion = [poblacion[key] for key in diccionario_ordenado.keys()]
    #eliminar por poblacion exedente, elimina los peores solo toma los mejores
    primer_elemento = next(iter(diccionario_ordenado.items()))
    ultimo_elemento = diccionario_ordenado.popitem()
    suma_valores = sum(diccionario_ordenado.values())
    promedio = suma_valores / len(diccionario_ordenado)
    
    mejor_individuo.append(primer_elemento[1])
    peor_individuo.append(ultimo_elemento[1])
    promedio_individuo.append(promedio)
    

    print(promedio_individuo)
    poblacion = poblacion[:poblacion_maxima]###
   


def main():
    global poblacion
    leer_dataset()
    poblacion = generar_n_individuos()

    #inicia el el bucle
    for i in range(0,cantidad_iteraciones):
        parejas_aleatorias = seleccion_parejas()
        print('parejas_aleatorias: ', parejas_aleatorias)
        hijos_sin_reparar = cruza(parejas_aleatorias)
        hijos_reparados = reparar_hijos(hijos_sin_reparar)
        mutacion(hijos_reparados)
        valorar_elemetos()
        ordenar_poblacion()
        print(poblacion)
        poblacion_puntuacion.clear()
        #termina el bucle

main()


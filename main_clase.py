import pandas as pd
import random 
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import mplcursors


class AlgoritmoGenetico():
    def __init__(self, arreglo_data_algoritmo,cultivo_requerido, tipo_cultivo,tipo_suelo,nutrientes_suelo,arreglo_data_main,riesgo_conocido):
        self.data = []
        self.data_diccionario = {}
        self.poblacion = []
        self.arreglo_claves = []
        self.poblacion_puntuacion = {}
        self.mejor_individuo = []
        self.promedio_individuo = []
        self.peor_individuo = []
        ###valores algoritmo
        self.cantidad_poblacion_inicial = int(arreglo_data_algoritmo[0])
        self.poblacion_maxima =  int(arreglo_data_algoritmo[1])
        self.posibilidad_cruza = int(arreglo_data_algoritmo[2])
        self.posibilidad_mut_individuo = int(arreglo_data_algoritmo[3])
        self.posibilidad_mut_gen = int(arreglo_data_algoritmo[4])
        self.cantidad_iteraciones =  int(arreglo_data_algoritmo[5])
        ###valores de usuario
        self.cantidad_cultivos = int(arreglo_data_main[7])###peso de la mochila
        self.cultivo_requerido = cultivo_requerido
        self.tipo_cultivo =  tipo_cultivo
        self.tipo_suelo = tipo_suelo
        self.ph_suelo = arreglo_data_main[8]
        self.nutrientes_suelo = nutrientes_suelo
        self.clima = arreglo_data_main[4]
        self.riesgo_conocido = riesgo_conocido
        self.fecha_siembra = arreglo_data_main[6]
        self.lo_mejor = []

  



    def leer_dataset(self):
        df = pd.read_csv('dataset.csv')
        df = df.iloc[0:]
        self.data = []
        for index, row in df.iterrows():
            converted_row = []
            for item in row:
                if isinstance(item, int):
                    converted_row.append([item])
                elif isinstance(item, str) and ',' in item:
                    converted_row.append(item.split(','))
                else:
                    converted_row.append([item])
            self.data.append(converted_row)
        auxiliar_id = 1
        for row in self.data:
            self.data_diccionario[auxiliar_id] = row
            auxiliar_id += 1

    def generar_n_individuos(self):
        poblacion_inicial = []
        auxiliar_claves = []

        for clave in self.data_diccionario:
            self.arreglo_claves.append(clave)
        auxiliar_claves = self.arreglo_claves

        for i in range(self.cantidad_poblacion_inicial):
            auxiliar_claves_copia = auxiliar_claves[:]
            random.shuffle(auxiliar_claves_copia)
            poblacion_inicial.append(auxiliar_claves_copia)

        return poblacion_inicial

    def seleccion_parejas(self):
        numero_de_parejas = (len(self.poblacion) / 2) + 0.5
        parejas_aleatorias = [random.sample(self.poblacion, 2) for _ in range(int(numero_de_parejas))]

        return parejas_aleatorias

    def cruza(self, parejas_aleatorias):
        hijos = []
        punto_de_cruce = 2 ##punto de cruce 
        for pareja in parejas_aleatorias:
            if random.randrange(0, 100) <= self.posibilidad_cruza:
                tupla1 = pareja[0]
                tupla2 = pareja[1]
                hijo1 = tupla1[:punto_de_cruce] + tupla2[punto_de_cruce:]
                hijo2 = tupla2[:punto_de_cruce] + tupla1[punto_de_cruce:]
                hijos.append(hijo1)
                hijos.append(hijo2)
        return hijos

    def reparar_hijos(self, hijos_sin_reparar):##elimina los elementos repetido que hay dentro del individuo
        hijos_reparados = []
        for hijo in hijos_sin_reparar:
            auxiliar_elementos_usados = []
            for elemento in hijo:
                if elemento in auxiliar_elementos_usados:
                    for claves in self.arreglo_claves:
                        if claves not in auxiliar_elementos_usados:
                            auxiliar_elementos_usados.append(claves)
                            break
                else:
                    auxiliar_elementos_usados.append(elemento)
            hijos_reparados.append(auxiliar_elementos_usados)

       
        return hijos_reparados

    def mutacion(self, hijos_reparados):
        for hijo in hijos_reparados:
            arreglo_posiciones_que_mutan = []

            if random.randint(0, 100) <= self.posibilidad_mut_individuo:
                for posicion in range(len(hijo)):
                    if random.randint(0, 100) <= self.posibilidad_mut_gen:
                        arreglo_posiciones_que_mutan.append(posicion)

                self.intercambio_de_valor(arreglo_posiciones_que_mutan, hijo)
            else:
                self.poblacion.append(hijo)

    def intercambio_de_valor(self, arreglo_posiciones_que_mutan, hijo):
        for elemento in arreglo_posiciones_que_mutan:
            posicion_random = random.randint(0, len(hijo) - 1)
            elemento_1 = hijo[elemento]
            elemento_2 = hijo[posicion_random]

            hijo[elemento] = elemento_2
            hijo[posicion_random] = elemento_1

        self.poblacion.append(hijo)

    def valorar_elementos(self):
        index = 0
        for individuo in self.poblacion:
            self.obtener_puntuacion(individuo, index)
            index += 1

    def obtener_puntuacion(self, individuo, index):
        puntuacion = Decimal(0)
      
        for elemento in individuo[:self.cantidad_cultivos]:
           
            for cultivo in self.cultivo_requerido:
                
                if cultivo == self.data_diccionario[elemento][0][0].replace(" ", "") or any(
                        tipo.replace(" ","") in self.tipo_cultivo for tipo in self.data_diccionario[elemento][2]):
                    puntuacion += Decimal('1')
                else:
                    puntuacion -= Decimal('0.1')

            if self.tipo_suelo in self.data_diccionario[elemento][1]:
                puntuacion += Decimal('1')
            else:
                puntuacion -= Decimal('0.2')

            for identificador in individuo[:self.cantidad_cultivos]:
                if identificador == elemento:
                    pass
                else:
                    if any(
                            compatible.replace(" ", "") in self.data_diccionario[elemento][0][0].replace(" ", "")
                            for compatible in self.data_diccionario[identificador][6]):
                        puntuacion += Decimal('0.5')
                    else:
                        puntuacion -= Decimal('0.15')

                    for efectos_generado in self.data_diccionario[elemento][8]:
                        if str(efectos_generado) in self.data_diccionario[identificador][9]:
                            puntuacion += Decimal('0.2')

            ph_rango = [float(num) for num in
                        self.data_diccionario[elemento][7][0].replace(" ", "").split("-")]
            if ph_rango[0] <= float(self.ph_suelo) <= ph_rango[1]:
                puntuacion += Decimal('2')
            else:
                puntuacion -= Decimal('0.6')

            for nutriente in self.data_diccionario[elemento][5]:
                if nutriente.replace(" ", "") in self.nutrientes_suelo:
                    puntuacion += Decimal('0.3')
                else:
                    puntuacion -= Decimal('0.1')

            if self.clima in self.data_diccionario[elemento][3]:
                puntuacion += Decimal('0.8')
            else:
                puntuacion -= Decimal('0.5')

            for riesgo in self.data_diccionario[elemento][4]:
                riesgo = riesgo.replace(" ", "")
                if riesgo in self.riesgo_conocido:
                    puntuacion -= Decimal('0.18')
                else:
                    puntuacion += Decimal('0.2')

            if self.fecha_siembra.replace(" ", "") in self.data_diccionario[elemento][10]:
                puntuacion += Decimal('1.0')
            else:
                puntuacion -= Decimal('0.8')

        print(Decimal(puntuacion))
        self.poblacion_puntuacion[index] = puntuacion

    def ordenar_poblacion(self):
        diccionario_ordenado = {k: v for k, v in sorted(self.poblacion_puntuacion.items(),
                                                       key=lambda item: item[1], reverse=True)}
        print(diccionario_ordenado)
        print(self.poblacion, '\n')
        self.poblacion = [self.poblacion[key] for key in diccionario_ordenado.keys()]

        primer_elemento = next(iter(diccionario_ordenado.items()))
        ultimo_elemento = diccionario_ordenado.popitem()
        suma_valores = sum(diccionario_ordenado.values())
        promedio = suma_valores / len(diccionario_ordenado)
        self.lo_mejor = self.poblacion[0]
        self.mejor_individuo.append(primer_elemento[1])
        self.peor_individuo.append(ultimo_elemento[1])
        self.promedio_individuo.append(promedio)


        self.poblacion = self.poblacion[:self.poblacion_maxima]

    def main(self):
        
        self.leer_dataset()
        self.poblacion = self.generar_n_individuos()

        for i in range(self.cantidad_iteraciones):
            parejas_aleatorias = self.seleccion_parejas()
            print('parejas_aleatorias: ', parejas_aleatorias)
            hijos_sin_reparar = self.cruza(parejas_aleatorias)
            hijos_reparados = self.reparar_hijos(hijos_sin_reparar)
            self.mutacion(hijos_reparados)
            self.valorar_elementos()
            self.ordenar_poblacion()
            print(self.poblacion)
            self.poblacion_puntuacion.clear()
        iteraciones = range(1, len(self.mejor_individuo) + 1)
        plt.figure(figsize=(10, 6))

        plt.plot(iteraciones, self.mejor_individuo, color='g', marker='o', linestyle='-', label='Mejor individuo')
        plt.plot(iteraciones, self.promedio_individuo, color='b', marker='o', linestyle='-', label='Promedio individuo')
        plt.plot(iteraciones, self.peor_individuo, color='r', marker='o', linestyle='-', label='Peor individuo')
        titulo ='Comparación de individuos a lo largo de las iteraciones\n La mejor combinacion es: ' + ', '.join(self.data_diccionario[elemento][0][0] for elemento in self.lo_mejor[:self.cantidad_cultivos])
        plt.title(titulo)
        plt.xlabel('Iteraciones')
        plt.ylabel('Valor del individuo')
        plt.legend()

        mplcursors.cursor(hover=True)

        plt.show()
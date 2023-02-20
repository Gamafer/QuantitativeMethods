import os
import csv
import numpy
import pandas as pd
import time
import math
import decimal
from scipy.stats import chi2
import matplotlib.pyplot as plt
from numpy import random

errorPercentages = numpy.array([0.995, 0.99, 0.975, 0.95, 0.90, 0.75, 0.5, 0.25, 0.10, 0.05, 0.025, 0.01, 0.005]) #99.5%, 99%, 97.5%, 95%, 90%, 75%, 50%, 25%, 10%, 5%, 2.5%, 1%, 0.5% 
tablaChiCuadrada = numpy.array(range(1,100)).reshape(-1,1)
tablaChiCuadrada = chi2.isf(errorPercentages, tablaChiCuadrada)
indiceErrores = 2

def centrosCuadrados(semillaInicio, numerosAGenerar):
    semilla = int(semillaInicio)
    if len(str(semillaInicio)) == 4 and semilla >= 100 and semilla <= 9999 and type(numerosAGenerar) == int and numerosAGenerar >= 1:
        numerosAleatorios = []
        Ris = []
        semillas = []
        generadores = []
        numerosGenerados = 0

        while numerosGenerados < numerosAGenerar:
            complemento = ""
            semillas.append(semilla)
            semillaCuadrado = semilla * semilla
            if len(str(semillaCuadrado)) < 8: 
                for relleno in range((8 - len(str(semillaCuadrado)))):
                    complemento += "0"
                semillaCuadrado = complemento + str(semillaCuadrado)
            
            numeroAleatorio = str(semillaCuadrado)[2:6]
            numerosAleatorios.append(numeroAleatorio)
            semilla = int(numeroAleatorio)
            Ri = int(numeroAleatorio) / 10000
            Ris.append(Ri)
            generador = str(semillaCuadrado)[0:2] + "|" + numeroAleatorio + "|" + str(semillaCuadrado)[6:]
            generadores.append(generador)
            
            numerosGenerados += 1

        creacionCarpeta("Centros_Cuadrados")
        datos = [semillas, generadores, numerosAleatorios, Ris]
        columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
        carpetaArchivo = "Centros_Cuadrados"
        escrituraCsv(datos, columnas, carpetaArchivo)

    else:
        print("La semilla otorgada no es un numero enetero de 4 digitos decimales o la cantidad de numeros a generar es invalida" + "\n")

def congruencial(semilla, multiplicador, incremento, modulo, numerosAGenerar, linealOMixto, chiCuadrada, kolmogorovSmirnov):
    if modulo > 0 and modulo > multiplicador and multiplicador > 0 and modulo > incremento and (incremento > 0 or incremento == 0) and modulo > semilla and (semilla > 0 or semilla == 0) and numerosAGenerar >= 1 and type(semilla) == int and type(multiplicador) == int and type(incremento) == int and type(modulo) == int and type(numerosAGenerar) == int:
        numerosAleatorios = []
        Ris = []
        semillas = []
        generadores = []
        numerosGenerados = 0

        while numerosGenerados < numerosAGenerar:
            semillas.append(semilla)
            generador = "(" + str(multiplicador) + "(" + str(semilla) + ")" + "+ " + str(incremento) + ")" + "mod" + "(" + str(modulo) + ")"
            generadores.append(generador)
            numeroAleatorio = (multiplicador * semilla + incremento) % modulo
            numerosAleatorios.append(numeroAleatorio)
            Ri = numeroAleatorio / modulo
            Ris.append(Ri)
            semilla = numeroAleatorio

            numerosGenerados += 1

        if linealOMixto == 0:
            creacionCarpeta("Congruencial")
            datos = [semillas, generadores, numerosAleatorios, Ris]
            columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
            carpetaArchivo = "Congruencial"
            escrituraCsv(datos, columnas, carpetaArchivo)
        else:
            creacionCarpeta("Congruencial_Mixto")
            datos = [semillas, generadores, numerosAleatorios, Ris]
            columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
            carpetaArchivo = "Congruencial_Mixto"
            escrituraCsv(datos, columnas, carpetaArchivo)

        if chiCuadrada == 1:
            validacionChiCuadrada(Ris, indiceErrores)
        if kolmogorovSmirnov == 1: 
            kolgomorovSmirnov(Ris)

    else:
        print("El modulo tiene que ser mayor a los demas valores; el multiplicador, incremento y semilla deben ser mayores a Cero; los valores presentados no son validos")

def congruencialMixto(semilla, multiplicador, incremento, modulo, numerosAGenerar, chiCuadrada, kolmogorovSmirnov):
    if hullDobell(multiplicador, incremento, modulo):
        congruencial(semilla, multiplicador, incremento, modulo, numerosAGenerar, 1, chiCuadrada, kolmogorovSmirnov)
    else:
        print("Los parametros no logran cumplir la evaluacion de Hull-Dobell")

def hullDobell(multiplicador, incremento, modulo): # a es el multiplicador, c es el incremento
    verificadorDivisor = 2
    while verificadorDivisor <= modulo:
        if incremento % verificadorDivisor != 0 or modulo % verificadorDivisor != 0:
            verificadorDivisor += 1
        else:
            return False
            
    numerosPrimosDivisores = []
    for numero in range(2, modulo):
        if modulo % numero == 0 and numeroPrimo(numero) == True:
            numerosPrimosDivisores.append(numero)
    for primo in numerosPrimosDivisores:
        if multiplicador % primo == 1:
            continue
        else:
            return False
    
    if modulo % 4 == 0: 
        if (multiplicador - 1) % 4 != 0: return False
        else: return True

    return True

def numeroPrimo(numero):
    if numero == 2: return True
    for num in range(2, numero):
        if numero % num == 0: 
            return False
    return True

def generadorMultiplicativo(semilla, multiplicador, modulo, numerosAGenerar, chiCuadrada, kolmogorovSmirnov):
    if (semilla == 0 or semilla > 0) and (multiplicador == 0 or multiplicador > 0) and (modulo == 0 or modulo > 0) and modulo > multiplicador and modulo > semilla and float(semilla).is_integer() and float(multiplicador).is_integer() and float(modulo).is_integer() and numerosAGenerar >= 1 and type(numerosAGenerar) == int:
        numerosAleatorios = []
        Ris = []
        semillas = []
        generadores = []
        numerosGenerados = 0

        while numerosGenerados < numerosAGenerar:
            semillas.append(semilla)
            generador = "(" + str(multiplicador) + "*" + str(semilla) + ")" + "mod" + "(" + str(modulo) + ")"
            generadores.append(generador)
            numeroAleatorio = (multiplicador * semilla) % modulo
            numerosAleatorios.append(numeroAleatorio)
            Ri = numeroAleatorio / modulo
            Ris.append(Ri)
            semilla = numeroAleatorio
            
            numerosGenerados += 1

        creacionCarpeta("Generador_Multiplicativo")
        datos = [semillas, generadores, numerosAleatorios, Ris]
        columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
        carpetaArchivo = "Generador_Multiplicativo"
        escrituraCsv(datos, columnas, carpetaArchivo)

        if chiCuadrada == 1:
            validacionChiCuadrada(Ris, indiceErrores)
        if kolmogorovSmirnov == 1: 
            kolgomorovSmirnov(Ris)

    else:
        print("Los parametros introducidos por el usuario no cumplen las espeficaciones para este generador")     

def congruencialLinealCombinado(semillasOriginales, multiplicadores, modulos, numerosAGenerar):
    if(separacionValores(semillasOriginales) != False and separacionValores(multiplicadores) != False and separacionValores(modulos) != False and numerosAGenerar >= 1 and type(numerosAGenerar) == int): 
        semillas = separacionValores(semillasOriginales)
        multiplicadores = separacionValores(multiplicadores)
        modulos = separacionValores(modulos)

        Ris = []
        numerosAleatorios = []
        semillasHistoricas = []
        for semilla in range(0, len(modulos)):
            semillasHistoricas.append([])
        numerosGenerados = 0

        while numerosGenerados < numerosAGenerar:
            numerosTemporales = []
            for indice in range(0, len(semillas)):
                numTemp = (multiplicadores[indice] * semillas[indice]) % modulos[indice]
                numerosTemporales.append(numTemp)
            numeroAleatorio = numerosTemporales[0]
            for numero in numerosTemporales[1:]:
                numeroAleatorio -= numero
            numeroAleatorio = numeroAleatorio % (modulos[0] - 1) #Misma cuestion de modulos
            numerosAleatorios.append(numeroAleatorio)
            Ris.append(numeroAleatorio / modulos[0]) #Ris se saca con modulos[0] o modulos[0] - 1
            for semilla in range(0, len(modulos)):
                semillasHistoricas[semilla].append(semillas[semilla])
            semillas = numerosTemporales
            numerosTemporales = []
            numerosGenerados += 1

        creacionCarpeta("Lineal_Combinado")
        datos = []
        for semilla in range(0, len(modulos)):
            datos.append(semillasHistoricas[semilla])
        datos.append(numerosAleatorios)
        datos.append(Ris)
        indice = 1
        columnas = []
        for semilla in range(0, len(modulos)):
            columnas.append("Semilla" + str(indice))
            indice += 1
        columnas.append("Aleatorio")
        columnas.append("Ri")
        carpetaArchivo = "Lineal_Combinado"
        escrituraCsv(datos, columnas, carpetaArchivo)

    else:
        print("No se puede llevar acabo el el metodo ya que los parametros no cumplen con las especificaciones")

def separacionValores(listaValores):
    arregloValores = []
    valorenCurso = ""
    indice = 0
    for caracter in listaValores:
        if caracter.isdigit():
            valorenCurso += caracter
            if indice == len(listaValores) - 1:
                (arregloValores).append(int(valorenCurso))
                valorenCurso = ""
        elif caracter == ",":
            arregloValores.append(int(valorenCurso))
            valorenCurso = ""
        elif caracter.isspace():
            indice += 1
            continue
        else:
            return False
        indice += 1
    return arregloValores 

def validacionChiCuadrada(numeros, porcentajeError):
    numeros.sort()
    numeroMenor = numeros[0]
    numeroMayor = numeros[len(numeros) - 1]
    rango = numeroMayor - numeroMenor
    k = math.floor(1 + (3.322 * math.log10(len(numeros))))
    sizeClase = round(1 / k, 5)
    print(sizeClase)
    
    limitesClases = []
    bandera = 0
    while bandera <= numeroMayor:
        limitesClases.append([round(bandera, 5), round(bandera + sizeClase, 5)])
        bandera += sizeClase
    frecuenciasAbsolutas = []
    for intervalo in limitesClases:
        frecuenciasAbsolutas.append(sum(map(lambda x: x >= intervalo[0] and x < intervalo[1], numeros)))

    #print(limitesClases)
    #print(frecuenciasAbsolutas)
    
    limitesClases = reasignacionClases(limitesClases, frecuenciasAbsolutas)[0]
    frecuenciasAbsolutas = reasignacionClases(limitesClases, frecuenciasAbsolutas)[1]

    probabilidades = []
    frecuenciasEsperadas = []
    elementosEstadisticoPrueba = []
    for indice in range(0, len(frecuenciasAbsolutas)):
        if indice != len(frecuenciasAbsolutas) - 1:
            probabilidades.append(1*(limitesClases[indice][1] - limitesClases[indice][0]))
            frecuenciasEsperadas.append(round(len(numeros) * probabilidades[indice], 3))
        else:
            probabilidades.append(1 - sum(probabilidades))
            frecuenciasEsperadas.append(round(len(numeros) - sum(frecuenciasEsperadas), 3))
        elementosEstadisticoPrueba.append(round(math.pow((frecuenciasAbsolutas[indice] - frecuenciasEsperadas[indice]),2) / frecuenciasEsperadas[indice], 5)) 
    
    print(k)
    print(limitesClases)
    print(frecuenciasAbsolutas)
    print(probabilidades)
    print(frecuenciasEsperadas)
    print(elementosEstadisticoPrueba)
    estadisticoPrueba = round(sum(elementosEstadisticoPrueba), 5)
    print(estadisticoPrueba)
    gradosLibertad = (len(limitesClases) - 1) 
    estadisticoChiCuadrada = round(tablaChiCuadrada[(gradosLibertad-1),porcentajeError], 5)
    print(estadisticoChiCuadrada)

    etiquetasGrafica = limitesClases
    ubicacionesBarras = numpy.arange(len(frecuenciasAbsolutas))
    ancho = 0.35
    figura, aux = plt.subplots()
    encontradas = aux.bar(ubicacionesBarras - ancho / 2, frecuenciasAbsolutas, ancho, label="Encontradas")
    esperadas = aux.bar(ubicacionesBarras + ancho / 2, frecuenciasEsperadas, ancho, label="Esperadas")
    aux.set_xlabel("Rangos de las clases")
    aux.set_ylabel("Numeros")
    aux.set_title("Frecuencias Encontradas VS Esperadas")
    aux.set_xticks(ubicacionesBarras)
    aux.set_xticklabels(etiquetasGrafica)
    aux.legend()
    aux.bar_label(encontradas, padding=2)
    aux.bar_label(esperadas, padding=2)
    figura.tight_layout()
    plt.show()

def reasignacionClases(limitesClases, frecuenciasAbsolutas):
    for indice in range(0, len(frecuenciasAbsolutas)):
        if frecuenciasAbsolutas[indice] < 5 and indice < len(frecuenciasAbsolutas) - 1:
            while frecuenciasAbsolutas[indice] < 5 and indice < len(frecuenciasAbsolutas) - 1:
                frecuenciasAbsolutas[indice] += frecuenciasAbsolutas[indice + 1]
                limitesClases[indice][1] = limitesClases[indice + 1][1]
                frecuenciasAbsolutas.pop(indice + 1)
                limitesClases.pop(indice + 1)
        if indice >= len(frecuenciasAbsolutas) - 1:
            break
    return [limitesClases, frecuenciasAbsolutas]    

def kolgomorovSmirnov(numeros,nivelSignificancia):
    numeros.sort()
    Ri = numeros 
    N = len(numeros)

    #Caculate 
    i_n = []
    i_n1 = []

    for i in range(1, N + 1): #Calcular i / N
        i_n.append(i/N) 
        
    for i in range(0, N): #Calcular i / N - Ri
        i_n1.append(abs(i_n[i] - Ri[i] ))
    
    ar = [Ri[0]]
    for i in range (1, N): #Calcular Ri - ((i-1)/N)
        ar.append(abs(Ri[i] - i_n[i-1]))

    Dplus = max(i_n1)
    Dminus = max(ar)
    Dtotal = max(Dplus, Dminus)

    #Link de la tabla https://simulacionutp2016.wordpress.com/2016/10/01/prueba-kolmogorov-smirnov/
    tabla = [[0.9,0.95,0.975,0.99,0.995,0.9975,0.999,0.995],
    [0.68337,0.77639,0.84189,0.9,0.92929,0.95,0.96838,0.97764],
    [0.56481,0.6304,0.70760,0.78456,0.829,0.86428,0.9,0.92065],
    [0.49265,0.56522,0.62394,0.68887,0.73424,0.77639,0.82217,0.85047],
    [0.44698,0.50945,0.56328,0.62718,0.66853,0.70543,0.75,0.78137],
    [0.41037,0.46799,0.51926,0.57741,0.61661,0.65287,0.69571,0.72479],
    [0.38148,0.43607,0.48342,0.53844,0.57581,0.60975,0.65071,0.67930],
    [0.35831,0.40962,0.45427,0.50654,0.54179,0.57429,0.61368,0.64098],
    [0.33910,0.38746,0.43001,0.47960,0.51332,0.54443,0.58210,0.60846],
    [0.32260,0.36866,0.40925,0.45562,0.48893,0.51872,0.555,0.58042],
    [0.30829,0.35242,0.39122,0.43670,0.46770,0.49539,0.53135,0.55588],
    [0.29577,0.33815,0.37543,0.41918,0.44905,0.47672,0.51047,0.53422],
    [0.28470,0.32549,0.36143,0.40362,0.43247,0.45921,0.49189,0.51490],
    [0.27481,0.31417,0.34890,0.38970,0.41762,0.44352,0.4725,0.49753],
    [0.26589,0.30397,0.33750,0.37713,0.40420,0.42934,0.45611,0.48182],
    [0.25778,0.29472,0.32733,0.36571,0.39201,0.41644,0.44637,0.4675],
    [0.25039,0.28627,0.31796,0.35528,0.38086,0.40464,0.43380,0.45540],
    [0.2436,0.27851,0.30936,0.34569,0.37062,0.39380,0.42224,0.44234],
    [0.23735,0.27136,0.30143,0.33685,0.36117,0.38379,0.41156,0.43119],
    [0.23156,0.26473,0.29408,0.32866,0.35241,0.37451,0.40165,0.42085],
    [0.22517,0.25858,0.28724,0.32104,0.34426,0.36588,0.39243,0.41122],
    [0.221,0.25283,0.28087,0.31394,0.33666,0.35782,0.38382,0.40223],
    [0.21646,0.24746,0.2749,0.30728,0.32954,0.35027,0.37575,0.39380],
    [0.21205,0.24242,0.26931,0.30104,0.32286,0.34318,0.36787,0.38588],
    [0.20790,0.23768,0.26404,0.29518,0.31657,0.33651,0.36104,0.37743],
    [0.20399,0.23320,0.25908,0.28962,0.30963,0.33022,0.35431,0.37139],
    [0.20030,0.22898,0.25438,0.28438,0.30502,0.32425,0.34794,0.36473],
    [0.19680,0.22497,0.24993,0.27942,0.29971,0.31862,0.34190,0.35842],
    [0.19348,0.22117,0.24571,0.27471,0.29466,0.31327,0.33617,0.35242],
    [0.19032,0.21756,0.2417,0.27023,0.28986,0.30818,0.33072,0.34672],
    [0.18732,0.21412,0.23788,0.26596,0.28529,0.30333,0.32553,0.34129],
    [0.18445,0.21085,0.23424,0.26189,0.28094,0.29870,0.32058,0.33611],
    [0.18171,0.20771,0.23076,0.25801,0.27577,0.29428,0.31584,0.33115],
    [0.17909,0.21472,0.22743,0.25429,0.27271,0.29005,0.31131,0.32641],
    [0.17659,0.20158,0.22425,0.25073,0.26897,0.286,0.30597,0.32187],
    [0.17418,0.1991,0.22119,0.24732,0.26532,0.28211,0.30281,0.31751],
    [0.17188,0.19646,0.21826,0.24404,0.2618,0.27838,0.29882,0.31333],
    [0.16966,0.19392,0.21544,0.24089,0.25843,0.27483,0.29498,0.30931],
    [0.16753,0.19148,0.21273,0.23785,0.25518,0.27135,0.29125,0.30544],
    [0.16547,0.18913,0.21012,0.23494,0.25205,0.26803,0.28772,0.30171]]
            
    datos = numpy.array(tabla)

    dataframe = pd.DataFrame(datos,index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,
                                            22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40], columns = [0.20,0.10,0.05,0.02,0.01,0.005,0.002,0.001]) # Los columns son los porcentajes para KolgomorovSmirnov (20%, 10%, 5%, 2%, 1%)

    if(nivelSignificancia >= 0.001 and nivelSignificancia <= 0.20 ):
      if(N<41):
        valorCritico = dataframe[nivelSignificancia][N]
        print("El valor critico es:", valorCritico)

      elif(nivelSignificancia >= 0.2 or nivelSignificancia < 0.1):
        valorCritico = 1.07 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.10 or nivelSignificancia < 0.05):
        valorCritico = 1.22 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.05 or nivelSignificancia < 0.02):
        valorCritico = 1.36 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.02 or nivelSignificancia < 0.01):
        valorCritico = 1.52 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.01 or nivelSignificancia < 0.005):
        valorCritico = 1.63 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.005 or nivelSignificancia < 0.002):
        valorCritico = 1.73 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.002 or nivelSignificancia < 0.001):
        valorCritico = 1.85 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia >= 0.002 or nivelSignificancia < 0.001):
        valorCritico = 1.85 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      elif(nivelSignificancia == 0.001):
        valorCritico = 1.95 / math.sqrt(N)
        print("El valor critico es:", valorCritico)
      else:
        print("No se puede realizar la operacion")  

    else:
      print("Nivel de Significancia Inválido")

    graficarSmirnov(Ri,i_n)

    ##Para el Quiroz 
    #Tabla de la ppt del prof
    ''' print("Numero de randoms", N) 
    print("Numeros ordenados",Ri)
    print("1er calculo",i_n) #Calcular i / N
    print("2ndo calculo",i_n1) #Calcular i / N - Ri
    print("3er calculo",ar) #Calcular Ri - ((i-1)/N)
    print("D+ ",Dplus)
    print("D- ",Dminus)
    print("Dtotal ",Dtotal)
    print(dataframe)  '''

def graficarSmirnov(Ri,i_n):
  print(Ri)
  print(i_n)
  horizontales = []
  verticales = []
  verticales.append(0)

  for i__n in range(len(i_n)):
      for i in range(0,2):
        verticales.append(i_n[i__n])
  for i__n in range(len(Ri)):
      for i in range(0,2):
        horizontales.append(Ri[i__n])
  horizontales.append(1)
  plt.plot(horizontales,verticales)

  Ri.insert(0,0)
  Ri.append(1)
  print(Ri)
  plt.plot(Ri,Ri)

  plt.legend(['Sn(x)','F(x)'])
  plt.ylabel('Probabilidad Acumulada')
  plt.xlabel('R(i)')
  plt.title("Comparacion de F(x) y Sn(x)")
  plt.show()

def creacionCarpeta(nombreCarpeta):
    pathActual = os.getcwd()
    pathActual = pathActual.replace("\\", "/")
    pathCarpeta = pathActual + "/" + nombreCarpeta + "/"
    if os.path.exists(pathCarpeta):
        pass
    else:
        os.mkdir(pathCarpeta)

def escrituraCsv(datos, columnas, carpetaArchivo):
    pathActual = os.getcwd()
    pathActual = pathActual.replace("\\", "/")
    pathActual = pathActual + "/" + carpetaArchivo + "/"

    columnas = numpy.array([columnas])
    t = time.localtime()
    nombreArchivo = time.strftime("%H:%M:%S", t)
    nombreArchivo = nombreArchivo.replace(":", "_") 
    nombreArchivo += carpetaArchivo + ".csv"
    nombreArchivo = pathActual + nombreArchivo

    with open(nombreArchivo, "w", newline = "") as file:
        escritor = csv.writer(file, delimiter = ",")
        escritor.writerows(columnas)
        for indices in range(0, len(datos[0])):
            renglon = []
            for indice in range(0, len(datos)):
                renglon.append(datos[indice][indices])
            renglon = numpy.array([renglon])
            escritor.writerows(renglon)


#centrosCuadrados("3547", 200)
#congruencial(4,5,7,8,8,0)
#congruencialMixto(4,8121,28411,134456,8)
#generadorMultiplicativo(15,35,64,25)
congruencialLinealCombinado("15985,33652,4545", "40014,40692,6678", "2147493563,2147483399,4557632", 20)

#print(hullDobell(5,7,8))
#print(hullDobell(75,74,65537))
#print(hullDobell(8121,28411,134456))
#print(separacionValores("45678,3939, 20920, 292029282, 212,21292"))
#creacionCarpeta("Centros_Cuadrados")
#escrituraCsv([[4,5,6,7], [4,5,6,7],[4,5,6,7], [4,5,6,7]], ["Semilla", "Generador", "Aletorio", "Ri"], "Centros_Cuadrados")
#prueba = [8.223, 0.836, 2.634, 4.778, 0.406, 0.517, 2.33, 2.563, 0.511, 6.426, 2.23, 3.81, 1.624, 1.507, 2.343, 1.458, 0.774, 0.023, 0.225, 3.214, 2.92, 0.968, 0.333, 4.025, 0.538, 0.234, 3.323, 3.334, 2.325, 7.514, 0.761, 4.49, 1.594, 1.064, 5.088, 1.401, 0.294, 3.491, 2.921, 0.334, 1.064, 0.186, 2.782, 3.246, 5.587, 0.685, 1.725, 1.267, 1.702, 1.849]
#for indice in range(0, len(prueba)):
    #prueba[indice] = prueba[indice] / 10
#numeros = [.018,.037,.156,.191,.213,.233,.281,.383,.392,.408,0.411, 0.434, 0.469, 0.541, 0.553, 0.575, 0.598, 0.668, 0.671, 0.711,0.719, 0.73, 0.77, 0.791, 0.819, 0.826, 0.894, 0.914, 0.994, 0.995]
#validacionChiCuadrada(numeros, 9)
#numeros = [0.44,0.81,0.14,0.05,0.93]
#nivelSignificancia = 0.05
#numero = random.rand(1000000)
#numero= numero.tolist()
#kolgomorovSmirnov(numero, nivelSignificancia)
#numeroPrimo((2**31 - 1))
#congruencialMixto(123457, 7**5, 0, (2**31 - 1), 10, 0, 0)
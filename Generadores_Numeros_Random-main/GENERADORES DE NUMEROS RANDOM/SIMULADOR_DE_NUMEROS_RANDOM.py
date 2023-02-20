import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
import os
import csv
import numpy
import pandas as pd
import time
import math
from scipy.stats import chi2
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure

class App(tk.Tk):
    
    def __init__(self):
        #Declaracion de la ventana principal y el tamaño de esta
        super().__init__()
        self.geometry("1000x450")
        self.title('Generador de Números Aleatorios')

        # Inicialización del menu principal
        self.menu = ("Método de los Centros Cuadrados",
      "Método Congruencial",
      "Método Congruencial Mixto",
      "Generador Multiplicativo",
      "Método Congruencial Lineal Combinado")
        
        #Porcentajes declarados para el display de las comprobaciones
        self.porcentajes=(
            "99.5%", "99%", "97.5%", "95%", "90%", "75%", "50%", "25%", "20%","10%", "5%", "2%", "1%", "0.5%", "0.2%", "0.1%"
            )
        self.porcentajes2=(
            "20%", "10%", "5%", "2%", "1%", "0.5%", "0.2%", "0.1%"
            )
        

        # Variables para manjear las opciones del menu en caso de comprobaciones
        self.option = tk.StringVar(self)
        
        self.option.set(self.menu[0])
        
        self.option2 = tk.StringVar(self)
        self.option3 = tk.StringVar(self)
        
        self.errorPercentages = numpy.array([0.995, 0.99, 0.975, 0.95, 0.90, 0.75, 0.5, 0.25,0.2 ,0.10, 0.05, 0.02, 0.01, 0.005,0.002,0.001])
        self.significancia = numpy.array([0.20,0.10,0.05,0.02,0.01,0.005,0.002,0.001])
        
        self.option2.set(self.porcentajes[0])
        self.option3.set(self.porcentajes2[0])
        
        self.tablaChiCuadrada = numpy.array(range(1,100)).reshape(-1,1)
        self.tablaChiCuadrada = chi2.isf(self.errorPercentages, self.tablaChiCuadrada)
        
        self.chi=tk.IntVar()
        self.kov=tk.IntVar()
        
        # create widget
        self.create_wigets()

    def create_wigets(self):
        # Paddings genéricos
        paddings = {'padx': 5, 'pady': 5}

        # Titulo de la ventana principal
        label = ttk.Label(self,  text='SIMULADOR DE NUMEROS RANDOM',font = ("Castellar",15))
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # Marco donde delimitamos los inputs de los diferentes métodos y declaración del mensaje de error
        self.frame = tk.LabelFrame(self,text="Método de los Centros Cuadrados", borderwidth=8,  labelanchor = "nw", font = ("Castellar",12))
        self.frame.grid(column=0, row=1,pady=20,padx=10)
        self.errorText= tk.StringVar()
        self.errorText.set(" ")
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")

        # option menu
        option_menu = tk.OptionMenu(
            self,
            self.option,
            *self.menu,
            command=self.option_changed)
        
        helv36 = tkFont.Font(family='Castellar', size=8)
        option_menu.config(font=helv36)
        
        option_menu.place(x=585, y=10)

    #Metodo encargado de crear carpeta, en caso de 
    #inexsistencia para guardar csv's historicos para
    #cada uno de los metoods de generacion de aleatorios
    def creacionCarpeta(self,nombreCarpeta):
        #Se obtiene el path/ruta donde se ejecuta el programa
        pathActual = os.getcwd()
        pathActual = pathActual.replace("\\", "/")
        pathCarpeta = pathActual + "/" + nombreCarpeta + "/"
        
        #En caso de que la carpeta no exista, se crea
        if os.path.exists(pathCarpeta):
            pass
        else:
            os.mkdir(pathCarpeta)
    
    #Metodo encargado de escribir generadores, numeros
    #aleatorios y Ris generados para cada metodo, en archivos
    #csv para posterior consulta del usuario
    def escrituraCsv(self,datos, columnas, carpetaArchivo):
        pathActual = os.getcwd()
        pathActual = pathActual.replace("\\", "/")
        pathActual = pathActual + "/" + carpetaArchivo + "/"
    
        #Se asigna el nombre ar archivo teninedo en cuenta el método
        #y la hora de ejecucion del mismo
        columnas = numpy.array([columnas])
        t = time.localtime()
        nombreArchivo = time.strftime("%H:%M:%S", t)
        nombreArchivo = nombreArchivo.replace(":", "_") 
        nombreArchivo += carpetaArchivo + ".csv"
        nombreArchivo = pathActual + nombreArchivo

        #Escritura en csv de la informacion previamente explicada
        with open(nombreArchivo, "w", newline = "") as file:
            escritor = csv.writer(file, delimiter = ",")
            escritor.writerows(columnas)
            for indices in range(0, len(datos[0])):
                renglon = []
                for indice in range(0, len(datos)):
                    renglon.append(datos[indice][indices])
                renglon = numpy.array([renglon])
                escritor.writerows(renglon)

    #Metodo invocado por la comprobracion de Chi-Cuadrada
    #para balancear clases con presencia menor a 5 numeros
    def reasignacionClases(self,limitesClases, frecuenciasAbsolutas):
            for indice in range(0, len(frecuenciasAbsolutas)):
                if frecuenciasAbsolutas[indice] < 5 and indice < len(frecuenciasAbsolutas) - 1: #Se realiza en caso de que hay presencia menor a 5 numeros
                    while frecuenciasAbsolutas[indice] < 5 and indice < len(frecuenciasAbsolutas) - 1:
                        frecuenciasAbsolutas[indice] += frecuenciasAbsolutas[indice + 1]
                        limitesClases[indice][1] = limitesClases[indice + 1][1]
                        frecuenciasAbsolutas.pop(indice + 1)
                        limitesClases.pop(indice + 1)
                if indice >= len(frecuenciasAbsolutas) - 1:
                    break
            return [limitesClases, frecuenciasAbsolutas]    
    
    def chi_frame(self,menor,mayor,claseLongitud,clases,fo,fe,prob,grados,aprob,formula,fig,com):
        
        # Creación de una nueva ventana para el display de los datos más relevantes del metodo de chi cuadrada
        chiFrame = tk.Toplevel()
        chiFrame.title("Chi-Cuadrada")
        
        # Labels para desplegar datos del algoritmo
        label = tk.Label(chiFrame, text="Rango:", font=("Arial",17,'bold'))
        label.grid(row=0,column=0)
        labelRango = tk.Label(chiFrame, text=(menor+" - "+mayor), font=("Arial",14))
        labelRango.grid(row=0,column=1)
        
        label2 = tk.Label(chiFrame, text="Clase (Longuitud): ", font=("Arial",17,'bold'))
        label2.grid(row=0,column=2)
        labelClase = tk.Label(chiFrame, text=str(claseLongitud), font=("Arial",14))
        labelClase.grid(row=0,column=3)
        
        label3 = tk.Label(chiFrame, text="K: ", font=("Arial",17,'bold'))
        label3.grid(row=0,column=4)
        labelK = tk.Label(chiFrame, text=str(len(clases)), font=("Arial",14))
        labelK.grid(row=0,column=5)

        # Declaración de la tabla para diplay de las clases y frecuencias
        cols = ('K','Clase', 'FOi observado', 'Probabilidad', 'FEi esperado', '(FO - FE)^2/FE')
        clasesStr=[] 

        if(aprob==1):
            color="green"
        else:
            color="red"
        
        for x in range(len(clases)):
            aux=""
            aux=str(clases[x][0])+" - " + str(clases[x][1]) 
            clasesStr.append(aux)

        table = ttk.Treeview(chiFrame, columns=cols, show='headings',selectmode='browse')
       
        for col in cols:
            table.heading(col, text=col,anchor="center") 
            table.column(col, stretch=0, anchor="center")
           
        for x in range(len(clases)):
            table.insert("", "end", values=(x,clasesStr[x],fo[x],prob[x],fe[x],formula[x]))

        
        headerTable=tk.Label(chiFrame, text="Distribuciones de Frecuencias ", font=("Arial",17,'bold'), pady=15)
        headerTable.grid(row=4,column=0, pady=10,columnspan=6)
        
        # Gráfica de las frecuencias por clases y  el toolbar para observar de manera más limpia, en caso de que se amonten las barras
        canvas=FigureCanvasTkAgg(fig,master=chiFrame)  
        canvas.get_tk_widget().grid(row=5,column=0,columnspan=6)
        toolbarFrame = tk.Frame(master=chiFrame)
        toolbarFrame.grid(row=7,column=0)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

        # Scrollbar para la tabla en caso que el el no. de datos sobrepase el tamaño
        table.grid(row=2, column=0, columnspan=6)
        vsb=ttk.Scrollbar(chiFrame, orient="vertical", command=table.yview)
        vsb.place(relx=0.98, rely=0.04, relheight=0.247, relwidth=0.020)
        table.configure(yscrollcommand=vsb.set)
        
        # La comprobación coloraeda indicando si se acepta o no la valiidación
        label5 = tk.Label(chiFrame, text="Estadístico Prueba: ", font=("Arial",17,'bold'), pady=15)
        label5.grid(row=7,column=0,columnspan=3)
        labelEst = tk.Label(chiFrame, text=(com), font=("Arial",15), pady=15,fg=color)
        labelEst.grid(row=7,column=2,columnspan=3)
        
    def kov_frame(self,ris,n_1,n_1_r,ar,fig,com,text,a,b,c,d):
        
        # Creación de una nueva ventana para el display de los datos más relevantes del metodo de chi cuadrada
        kovFrame = tk.Toplevel()
        kovFrame.title("Kolgomorov-Smirnov")
        
        # Labels para desplegar datos del algoritmo
        a=round(a,4)
        b=round(b,4)
        c=round(c,4)
        d=round(d,4)        
        label = tk.Label(kovFrame, text="Numero de elementos:", font=("Arial",17,'bold'))
        label.grid(row=0,column=0,pady=10)
        labelRango = tk.Label(kovFrame, text=a, font=("Arial",14))
        labelRango.grid(row=0,column=1,pady=10)
        
        label2 = tk.Label(kovFrame, text="D+: ", font=("Arial",17,'bold'))
        label2.grid(row=0,column=2,pady=10)
        labelClase = tk.Label(kovFrame, text=b, font=("Arial",14))
        labelClase.grid(row=0,column=3,pady=10)
        
        label3 = tk.Label(kovFrame, text="D-: ", font=("Arial",17,'bold'))
        label3.grid(row=0,column=4,pady=10)
        labelK = tk.Label(kovFrame, text=c, font=("Arial",14))
        labelK.grid(row=0,column=5,pady=10)
        
        label4 = tk.Label(kovFrame, text="Dmax: ", font=("Arial",17,'bold'))
        label4.grid(row=0,column=6,pady=10)
        labelN = tk.Label(kovFrame, text=d, font=("Arial",14))
        labelN.grid(row=0,column=7,pady=10)
        
        
        # Declaración de la tabla para diplay de las iteracions de Kolmogorov
        cols = ('Ri','1/N', '(1/N)-Ri', 'Ri-(i-1)/N')
        table = ttk.Treeview(kovFrame, columns=cols, show='headings',selectmode='browse')
        ris.pop(0)

       
        for col in cols:
            table.heading(col, text=col,anchor="center") 
            table.column(col, stretch=0, anchor="center")
            

        for x in range(len(n_1)):
            table.insert("", "end", values=(ris[x],n_1[x],n_1_r[x],ar[x]))

            
        headerTable=tk.Label(kovFrame, text="Comparación entre F(X) y Sn(X)", font=("Arial",17,'bold'))
        headerTable.grid(row=2,column=0, pady=10,padx=20,columnspan=8)
        table.grid(row=1, column=0, columnspan=8, rowspan=1)
        
        #Scrollbar para la tabla
        vsb=ttk.Scrollbar(kovFrame, orient="vertical", command=table.yview)
        vsb.place(relx=0.98, rely=0.06, relheight=0.245, relwidth=0.020)
        table.configure(yscrollcommand=vsb.set)
                
        
        # Gráfica de los datos de smirnov y el toolbar para observar de manera más limpia, en caso de que se amonten los datos
        canvas=FigureCanvasTkAgg(fig,master=kovFrame)  
        canvas.get_tk_widget().grid(row=3,column=0,columnspan=8)
        toolbarFrame = tk.Frame(master=kovFrame)
        toolbarFrame.grid(row=4,column=0,columnspan=8)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        
        if(com==1):
            color="green"
        else:
            color="red"
        
        # La comprobación coloraeda indicando si se acepta o no la valiidación
        labelC = tk.Label(kovFrame, text="Comprobación: ", font=("Arial",17,'bold'))
        labelC.grid(row=5, column=0,columnspan=4, pady=20)
        label5 = tk.Label(kovFrame, text=text, font=("Arial",15),fg=color)
        label5.grid(row=5, column=2,columnspan=4, pady=20)
        
    #Metodo encargado de realizar todos los pasos de la
    #comprobracion de Chi-cuadrada
    def validacionChiCuadrada(self,numeros,resultados):
        #Ordenamiento de numeros, obtencion de tamano clase
        numeros.sort()
        numeroMenor = numeros[0]
        numeroMayor = numeros[len(numeros) - 1]
        rango = numeroMayor - numeroMenor
        k = math.floor(1 + (3.322 * math.log10(len(numeros))))
        sizeClase = round(1 / k, 5)
        print(sizeClase)
        
        #Generacion de clases
        limitesClases = []
        bandera = 0
        while bandera <= numeroMayor:
            limitesClases.append([round(bandera, 5), round(bandera + sizeClase, 5)])
            bandera += sizeClase
        frecuenciasAbsolutas = []
        for intervalo in limitesClases:
            frecuenciasAbsolutas.append(sum(map(lambda x: x >= intervalo[0] and x < intervalo[1], numeros)))

        #Se verifica si se deben realizar reasignaciones de clases
        limitesClases = self.reasignacionClases(limitesClases, frecuenciasAbsolutas)[0]
        frecuenciasAbsolutas = self.reasignacionClases(limitesClases, frecuenciasAbsolutas)[1]
    
        #Se calculan las probabilidades reales y os elementos del Estadistico de Prueba
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
        
        #Se obtiene el estadistico de Prueba, al igual que el estadistico de ChiCuadrada
        indice=self.porcentajes.index(self.option2.get())
        estadisticoPrueba = round(sum(elementosEstadisticoPrueba), 5)
        gradosLibertad = (len(limitesClases) - 1) 
        estadisticoChiCuadrada = round(self.tablaChiCuadrada[(gradosLibertad-1),indice], 5)
        
        # Configuración para el display de la gráfica
        fig = Figure(figsize=(12,3.5),dpi=100)
        etiquetasGrafica = limitesClases
        ubicacionesBarras = numpy.arange(len(frecuenciasAbsolutas))
        ancho = 0.35
        
        # Creación de la gráfica con la libreria matplotlib y tkinter
        aux = fig.add_subplot(111)
        encontradas = aux.bar(ubicacionesBarras - ancho / 2, frecuenciasAbsolutas, ancho, label="Encontradas")
        esperadas = aux.bar(ubicacionesBarras + ancho / 2, frecuenciasEsperadas, ancho, label="Esperadas")
        aux.set_xlabel("Rangos de las clases")
        aux.set_ylabel("Numeros")
        aux.set_xticks(ubicacionesBarras)
        aux.set_xticklabels(etiquetasGrafica)
        aux.legend()
        aux.bar_label(encontradas, padding=2)
        aux.bar_label(esperadas, padding=2)

        # Variable para diplay de la validación
        numeroMenorStr=str(numeroMenor)
        numeroMayorStr=str(numeroMayor)
        comprobacion=(str(estadisticoPrueba)+" < "+str(estadisticoChiCuadrada))
        if estadisticoPrueba < estadisticoChiCuadrada:
            condicion=1
            color="green"
        else:
            condicion=0
            color="red"
        
        # Deplega los resultado de la validación y crea un hipervínculo a los detalles del método
        label = tk.Label(resultados, text="Chi-Cuadrada", font=("Arial",17)).grid(row=2, column=0)

        label2 = tk.Label(resultados, text=comprobacion, font=("Arial",17), fg=color)
        label2.grid(row=2, column=1)
        label2.bind("<Button-1>", lambda event, a=numeroMenorStr, b=numeroMayorStr, c=sizeClase, d=limitesClases, 
                    e=frecuenciasAbsolutas, f=frecuenciasEsperadas, g=probabilidades, h=gradosLibertad, i=condicion, j=elementosEstadisticoPrueba, 
                    fig=fig,com=comprobacion: 
                    self.chi_frame(a,b,c,d,e,f,g,h,i,j,fig,com) )
 
    #Metodo encargado de realizar todos los pasos de la
    #comprobacion de Kolmogorov Smirnov
    def kolgomorovSmirnov(self,numeros,nivelSignificancia,resultados):
        #Ordenamiento de numeros
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
    
        #Obtencion de D+, D- y Dmax{D+, D-}
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

        #Calculo del valor critico con base en tabla de kolmogorov y  nivel de significancia
        if(nivelSignificancia >= 0.001 and nivelSignificancia <= 0.20):
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
              
        horizontales = []
        verticales = []
        verticales.append(0)
        save_ri=Ri
        
        #Generacion de puntos para ser graficados -S(n) y F(x)- en comprobacion
        for i__n in range(len(i_n)):
            for i in range(0,2):
              verticales.append(i_n[i__n])
        for i__n in range(len(Ri)):
            for i in range(0,2):
              horizontales.append(Ri[i__n])
        horizontales.append(1)
        
        # Configuración para el display de la gráfica
        fig = Figure(figsize=(5,3),dpi=100)
        aux=fig.add_subplot(111)
        aux.plot(horizontales,verticales)
        Ri.insert(0,0)
        Ri.append(1)
        aux.plot(Ri,Ri)      
        aux.legend(['Sn(x)','F(x)'])
        aux.set_ylabel('Probabilidad Acumulada')
        aux.set_xlabel('R(i)')
        aux.set_title("Comparacion de F(x) y Sn(x)")
        
        # Variable para diplay de la validación
        auxDtotal=round(Dtotal,10)
        auxCritico=round(valorCritico,10)
        comprobacion=(str(auxDtotal)+" < "+str(auxCritico))
        
        if  Dtotal < valorCritico:
            condicion=1
            color="green"
        else:
            condicion=0
            color="red"
        
        # Deplega los resultado de la validación y crea un hipervínculo a los detalles del método
        label = tk.Label(resultados, text="Kolgomorov-Smirnov", font=("Arial",17)).grid(row=3, column=0)

        label2 = tk.Label(resultados, text=comprobacion, font=("Arial",17),fg=color)
        label2.grid(row=3, column=1)
        label2.bind("<Button-1>", lambda event, a=save_ri, b=i_n, c=i_n1, d=ar, f=fig, com=condicion,text=comprobacion,g=N,h=Dplus,i=Dminus,j=Dtotal: 
                    self.kov_frame(a,b,c,d,f,com,text,g,h,i,j) )

    #Funcion encaragada de realizar el metodo de Centros Cuadrados
    def centrosCuadrados(self, semillaInicio, numerosAGenerar):
       #Manejo de errores al presentarse parametros no aceptodos por el metodo
       try:
           semilla = int(semillaInicio)
       except:
           self.errorText.set('La semilla debe ser un numero entero')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=2)
           return
           
       if type(numerosAGenerar) != int:
           self.errorText.set('Numeros a Generar debe ser un entero')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=2)
           return
       if numerosAGenerar < 1:
           self.errorText.set('Numeros a Generar debe ser mayor a 0')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=2)
           return
       
       #Esta parte del codigo simboliza la generacion de n. aleatorios, al igual que de Ri
       if len(str(semillaInicio)) == 4 and semilla >= 100 and semilla <= 9999:
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
                   #Completa semilla al cuadrado en caso de no tener 8 digitos
                   for relleno in range((8 - len(str(semillaCuadrado)))):
                       complemento += "0"
               semillaCuadrado = complemento + str(semillaCuadrado)
                
               numeroAleatorio = str(semillaCuadrado)[2:6] #Se obtiene numero aleatorio
               numerosAleatorios.append(numeroAleatorio)
               semilla = int(numeroAleatorio)
               Ri = int(numeroAleatorio) / 10000 #Se obtiene Ri
               Ris.append(Ri)
               generador = str(semillaCuadrado)[0:2] + "|" + numeroAleatorio + "|" + str(semillaCuadrado)[6:] #Se obtiene generador
               generadores.append(generador)
                
               numerosGenerados += 1
        
        #Tablas para desplegar los números random generados 
           self.creacionCarpeta("Centros_Cuadrados")
           datos = [semillas, generadores, numerosAleatorios, Ris]
           columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
           carpetaArchivo = "Centros_Cuadrados"
           self.escrituraCsv(datos, columnas, carpetaArchivo)
           
           results = tk.Toplevel()
           results.title("Resultados")
           cols = ('Xn','Semilla', 'Generador', 'No. Aleatorio', 'Ri')
           label = tk.Label(results, text="Centros Cuadrados", font=("Arial",30)).grid(row=0, columnspan=3)
           table = ttk.Treeview(results, columns=cols, show='headings',selectmode='browse')
           
           for col in cols:
               table.heading(col, text=col)  
               
           for x in range(len(semillas)):
               table.insert("", "end", values=(x,semillas[x], generadores[x], numerosAleatorios[x], Ris[x]))
               
           table.grid(row=1, column=0, columnspan=2)
           vsb=ttk.Scrollbar(results, orient="vertical", command=table.yview)
           vsb.place(relx=0.978, rely=0.2, relheight=0., relwidth=0.020)
           table.configure(yscrollcommand=vsb.set)

       else:
           self.errorText.set('La semilla otorgada no es un numero enetero de 4 digitos decimales')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=2) 

    #Funcion encaragada de realizar el metodo de Metodo Congruencial 
    #(se invoca desde aqui al Congruencial y/o al Congruencial Mixto)       
    def congruencial(self,semilla, multiplicador, incremento, modulo, numerosAGenerar,titulo):
        #Manejo de errores con los parametros obtenidos del usuario
        if numerosAGenerar < 1:
           self.errorText.set('Numeros a Generar debe ser mayor a 0')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=4)
           return
        
        #Manejo de errores con los parametros obtenidos del usuario
        if modulo > 0 and modulo > multiplicador and multiplicador > 0 and modulo > incremento and (incremento > 0 or incremento == 0) and modulo > semilla and (semilla > 0 or semilla == 0):
            numerosAleatorios = []
            Ris = []
            semillas = []
            generadores = []
            numerosGenerados = 0
    
            #Se realiza la formula para la obtencion los numeros aleatorios y los Ri's
            while numerosGenerados < numerosAGenerar:
                semillas.append(semilla)
                generador = "(" + str(multiplicador) + "(" + str(semilla) + ")" + "+ " + str(incremento) + ")" + "mod" + "(" + str(modulo) + ")" #Obtencion generador
                generadores.append(generador)
                numeroAleatorio = (multiplicador * semilla + incremento) % modulo #Obtencio del numero aleatorio
                numerosAleatorios.append(numeroAleatorio)
                Ri = numeroAleatorio / modulo #Obtencion del Ri
                Ris.append(Ri)
                semilla = numeroAleatorio
    
                numerosGenerados += 1
    
            #Dependiendo del usuario, se invoca a la escritura de los resultados en las carpetas de Congruencial Lineal o Mixto
            if titulo == "Congurencial Lineal":
                self.creacionCarpeta("Congruencial")
                datos = [semillas, generadores, numerosAleatorios, Ris]
                columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
                carpetaArchivo = "Congruencial"
                self.escrituraCsv(datos, columnas, carpetaArchivo)
            else:
                self.creacionCarpeta("Congruencial_Mixto")
                datos = [semillas, generadores, numerosAleatorios, Ris]
                columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
                carpetaArchivo = "Congruencial_Mixto"
                self.escrituraCsv(datos, columnas, carpetaArchivo)
            
            #Tablas para desplegar los números random generados 
            results = tk.Toplevel()
            results.title("Resultados")
            cols = ('Xn','Semilla', 'Generador', 'No. Aleatorio', 'Ri')
            label = tk.Label(results, text=titulo, font=("Arial",30)).grid(row=0, columnspan=3)
            table = ttk.Treeview(results, columns=cols, show='headings',selectmode='browse')
           
            for col in cols:
                table.heading(col, text=col)  
               
            for x in range(len(semillas)):
                table.insert("", "end", values=(x,semillas[x], generadores[x], numerosAleatorios[x], Ris[x]))
               
            table.grid(row=1, column=0, columnspan=2)
            vsb=ttk.Scrollbar(results, orient="vertical", command=table.yview)
            vsb.place(relx=0.978, rely=0.2, relheight=0.8, relwidth=0.020)
            table.configure(yscrollcommand=vsb.set)
            
            indice=self.porcentajes2.index(self.option3.get())
            sig=self.significancia[indice]
            
            # Verificar si el usuario quiere realizar una validación con los diversos métodos
            if self.chi.get() == 1:
                self.validacionChiCuadrada(Ris,results)
            if self.kov.get() == 1:
                self.kolgomorovSmirnov(Ris,sig,results)

        else:
            self.errorText.set('El modulo tiene que ser mayor a los demas valores; el multiplicador, incremento y semilla deben ser mayores a Cero')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 

    #Metodo auxiliar para manejo de errores de parametros de usuario al realizar Congruencial Mixto        
    def congruencialMixto(self,semilla, multiplicador, incremento, modulo, numerosAGenerar):
         #Manejo de errores con los parametros obtenidos del usuario
        if self.hullDobell(multiplicador, incremento, modulo):
            titulo="Congruencial Mixto"
            self.congruencial(semilla, multiplicador, incremento, modulo, numerosAGenerar,titulo)
        else:
            self.errorText.set('Los parametros no logran cumplir la evaluacion de Hull-Dobell')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
            print("Los parametros no logran cumplir la evaluacion de Hull-Dobell")

    #Metodo auxiliar para realizar comprobacion de Hull-Dobell
    #durante el metodo de generacion Congruencial Mixto
    def hullDobell(self,multiplicador, incremento, modulo): # a es el multiplicador, c es el incremento
        verificadorDivisor = 2
        #Verifica que el MCD entre incremento y modulo sea 1
        while verificadorDivisor <= modulo:
            if incremento % verificadorDivisor != 0 or modulo % verificadorDivisor != 0:
                verificadorDivisor += 1
            else:
                return False
                
        numerosPrimosDivisores = []
        #Verifica segundo estatuto de la prueba Hull-Dobell
        for numero in range(2, modulo):
            if modulo % numero == 0 and self.numeroPrimo(numero) == True:
                numerosPrimosDivisores.append(numero)
        for primo in numerosPrimosDivisores:
            if multiplicador % primo == 1:
                continue
            else:
                return False

        #Verifica tercer estatuto de la prueba Hull-Dobell
        if modulo % 4 == 0: 
            if (multiplicador - 1) % 4 != 0: return False
            else: return True
    
        return True
    
    #Metodo auxiliar para determinar si un numero es primo
    def numeroPrimo(self,numero):
        if numero == 2: return True
        for num in range(2, numero):
            if numero % num == 0: 
                return False
        return True
    
    #Funcion encargada de realizar todos los pasos
    #contemplados en el generador Multiplicativo
    def generadorMultiplicativo(self,semilla, multiplicador, modulo, numerosAGenerar):
        #Comprobacion y manejo de rrores por elementos introducidos por usuario
        if numerosAGenerar < 1:
           self.errorText.set('Numeros a Generar debe ser mayor a 0')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=4)
           return
       
        #Comprobacion y manejo de rrores por elementos introducidos por usuario
        if (semilla == 0 or semilla > 0) and (multiplicador == 0 or multiplicador > 0) and (modulo == 0 or modulo > 0) and modulo > multiplicador and modulo > semilla and float(semilla).is_integer() and float(multiplicador).is_integer() and float(modulo).is_integer():
            numerosAleatorios = []
            Ris = []
            semillas = []
            generadores = []
            numerosGenerados = 0
    
            while numerosGenerados < numerosAGenerar:
                semillas.append(semilla)
                generador = "(" + str(multiplicador) + "*" + str(semilla) + ")" + "mod" + "(" + str(modulo) + ")" #Obtencion del generador
                generadores.append(generador)
                numeroAleatorio = (multiplicador * semilla) % modulo #Obtencion del numero aleatorio con formula del generador Multiplicativo
                numerosAleatorios.append(numeroAleatorio)
                Ri = numeroAleatorio / modulo #Obtencion de Ri
                Ris.append(Ri)
                semilla = numeroAleatorio
                
                numerosGenerados += 1
            
            self.creacionCarpeta("Generador_Multiplicativo")
            datos = [semillas, generadores, numerosAleatorios, Ris]
            columnas = ["Semilla", "Generador", "Aletorio", "Ri"]
            carpetaArchivo = "Generador_Multiplicativo"
            self.escrituraCsv(datos, columnas, carpetaArchivo)
            
            #Tablas para desplegar los números random generados 
            results = tk.Toplevel()
            results.title("Resultados")
            cols = ('Xn','Semilla', 'Generador', 'No. Aleatorio', 'Ri')
            label = tk.Label(results, text="Generador Multiplicativo", font=("Arial",30)).grid(row=0, columnspan=3)
            table = ttk.Treeview(results, columns=cols, show='headings',selectmode='browse')
            
            for col in cols:
                table.heading(col, text=col)  
               
            for x in range(len(semillas)):
                table.insert("", "end", values=(x,semillas[x], generadores[x], numerosAleatorios[x], Ris[x]))
               
            table.grid(row=1, column=0, columnspan=2)
            vsb=ttk.Scrollbar(results, orient="vertical", command=table.yview)
            vsb.place(relx=0.978, rely=0.2, relheight=0.8, relwidth=0.020)
            table.configure(yscrollcommand=vsb.set)
                        
            indice=self.porcentajes2.index(self.option3.get())
            sig=self.significancia[indice]
            
            # Verificar si el usuario quiere realizar una validación con los diversos métodos
            if self.chi.get() == 1:
                self.validacionChiCuadrada(Ris,results)
            if self.kov.get() == 1:
                self.kolgomorovSmirnov(Ris,sig,results)
        else:
            self.errorText.set('El modulo tiene que ser mayor a los demas valores; el multiplicador y semilla deben ser mayores o iguales a Cero')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
    
    #Metodo auxiliar para separacion de valores a ser usados
    #como semillas, modulos, y multplicadores con L'Ecuyer
    def separacionValores(self,listaValores):
        arregloValores = []
        valorenCurso = ""
        indice = 0
        for caracter in listaValores:
            if caracter.isdigit():
                valorenCurso += caracter
                if indice == len(listaValores) - 1:
                    if int(valorenCurso) == 0: #No se aceptan valores de 0
                        return False
                    (arregloValores).append(int(valorenCurso))
                    valorenCurso = ""
            elif caracter == ",":
                if int(valorenCurso) == 0:
                    return False
                arregloValores.append(int(valorenCurso))
                valorenCurso = ""
            elif caracter.isspace():
                indice += 1
                continue
            else: #Solo se aceptan digitos, comas y espacios; lo demas generara excepcion y manejo de errores
                return False
            indice += 1
        return arregloValores 
    
    #Metodo encargado de realizar todos los pasos necesarios
    #para implementar el metodo de L'Ecuyer
    def congruencialLinealCombinado(self,semillasOriginales, multiplicadores, modulos, numerosAGenerar):
        #Comprobacion y manejo de errores de parametros de usuarios
        if numerosAGenerar < 1:
           self.errorText.set('Numeros a Generar debe ser mayor a 0')
           self.errorMessage.grid_configure(column=0,row=0,columnspan=2)
           return
        #Comprobacion y manejo de errores de parametros de usuarios

        if(self.separacionValores(semillasOriginales) != False and self.separacionValores(multiplicadores) != False and self.separacionValores(modulos) != False): 
            semillas = self.separacionValores(semillasOriginales) #Se separan y obtienen todas las semillas a ser usadas
            multiplicadores = self.separacionValores(multiplicadores) #Se separan y obtienen todos los multiplicadores a ser usados
            modulos = self.separacionValores(modulos) #Se separan y obtienen todos los modulos a ser usados
    
            if len(semillas) != len(multiplicadores) or len(multiplicadores) != len(modulos): #Manejo de errores con semillas, multiplicadores y modulos
                self.errorText.set('Introducir el mismo número de semillas, módulos y multiplicadores')
                self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
                return

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
                numeroAleatorio = numeroAleatorio % (modulos[0] - 1) 
                numerosAleatorios.append(numeroAleatorio)
                Ris.append(numeroAleatorio / modulos[0]) #Obtencion de Ri
                for semilla in range(0, len(modulos)):
                    semillasHistoricas[semilla].append(semillas[semilla]) #Obtencion de la semilla usada
                semillas = numerosTemporales
                numerosTemporales = []
                numerosGenerados += 1

            print(numerosAleatorios)
            
            self.creacionCarpeta("Lineal_Combinado")
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
            self.escrituraCsv(datos, columnas, carpetaArchivo)
    
            #Tablas para desplegar los números random generados 
            results = tk.Toplevel()
            results.title("Resultados")
            cols = ('Xn','No. Aleatorio')
            label = tk.Label(results, text="Generador Lineal Combinado", font=("Arial",30)).grid(row=0, columnspan=3)
            table = ttk.Treeview(results, columns=columnas, show='headings',selectmode='browse')
           
            for col in columnas:
                table.heading(col, text=col)  
            

            for x in range(len(numerosAleatorios)):
                table.insert("", "end", values=([y[x] for y in datos]) )
               
            table.grid(row=1, column=0, columnspan=2)
            vsb=ttk.Scrollbar(results, orient="vertical", command=table.yview)
            vsb.place(relx=0.978, rely=0.2, relheight=0.8, relwidth=0.020)
            table.configure(yscrollcommand=vsb.set)
        else:
            self.errorText.set('Favor de seguir el formato y que todos los numeros sean enteros positivos y  mayores a 0')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
            
    def cuadrados_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="Método de los Centros Cuadrados"
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # Display de los inputs necesarios para el método
        semilla_label= ttk.Label(self.frame,  text='Semilla:',font = ("Castellar",8)).grid(column=0,row=1,padx=10,pady=20,sticky="e")
        semilla_input = tk.Entry(self.frame, width=20)
        semilla_input.grid(column=1,row=1,padx=40)
        
        total_label= ttk.Label(self.frame,  text='Total de Números a Generar:',font = ("Castellar",8)).grid(column=0,row=2,padx=10,pady=10,sticky="e")
        total_input = tk.Entry(self.frame, width=20)
        total_input.grid(column=1,row=2,padx=10)
        
        sumbit_btn= tk.Button(self.frame, text="Generar",font = ("Castellar",8), command = lambda: self.aux_cuadrados_frame(semilla_input,total_input))
        sumbit_btn.grid(column=0,row=3, columnspan=3,pady=20)
        
    def aux_cuadrados_frame(self,semilla_input,total_input):
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if semilla_input.get() != '' and total_input.get() != '':
            x1 = str(semilla_input.get())
            try:    
                x2 = int(total_input.get())  
            except:
                self.errorText.set('Numeros a Generar debe se numero entero')
                self.errorMessage.grid(column=0,row=0,columnspan=2)
                return
            self.centrosCuadrados(x1,x2)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=2)    
            
    def congruencial_frame(self, *args):

        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="Método Congruencial"
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        semilla_label= ttk.Label(self.frame,  text='Semilla:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=1,pady=10,padx=10)
        semilla_input = ttk.Entry(self.frame, width=20)
        semilla_input.grid(column=1,row=1,padx=10)
        
        multiplicador_label= ttk.Label(self.frame,  text='Multiplicador:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=2,pady=10,padx=10)
        multiplicador_input = ttk.Entry(self.frame, width=20)
        multiplicador_input.grid(column=1,row=2,padx=10)
        
        incremento_label= ttk.Label(self.frame,  text='Incremento:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=3,pady=10,padx=10)
        incremento_input = ttk.Entry(self.frame, width=20)
        incremento_input.grid(column=1,row=3,padx=10)
        
        modulo_label= ttk.Label(self.frame,  text='Modulo:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=4,pady=10,padx=10)
        modulo_input = ttk.Entry(self.frame, width=20)
        modulo_input.grid(column=1,row=4,padx=10)
        
        total_label= ttk.Label(self.frame,  text='Total de Números a Generar:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=5,pady=10,padx=10)
        total_input = ttk.Entry(self.frame, width=20)
        total_input.grid(column=1,row=5,padx=10) 
        
        #Checkbox para verificar si el usuario quiere que se hagan las diferentes validaciones
        chi_cuadrada=tk.Checkbutton(self.frame, text="Chi-Cuadrada",variable=self.chi,justify="left")
        chi_cuadrada.grid(sticky = "W", column=2,row=1) 
        
        kolmogorov=tk.Checkbutton(self.frame, text="Kolmogorov-Smirnov", variable=self.kov,justify="left")
        kolmogorov.grid(sticky = "W",column=2,row=3) 
         
        helv36 = tkFont.Font(family='MS Sans Serif', size=10)
        porcentaje_Menu = tk.OptionMenu(
            self.frame,
            self.option2,
            *self.porcentajes,
           )
        porcentaje_Menu.config(font=helv36)
        
        porcentaje_Menu2 = tk.OptionMenu(
            self.frame,
            self.option3,
            *self.porcentajes2,
           )
        porcentaje_Menu2.config(font=helv36)
        
        porcentaje_Menu.grid(sticky = "e",column=3,row=1,padx=5) 
        porcentaje_Menu2.grid(sticky = "e",column=3,row=3,padx=5) 
        
        sumbit_btn= tk.Button(self.frame, 
                              text="Generar",
                              font = ("Castellar",8),  
                              command = lambda: self.aux_congruencial_frame(semilla_input,multiplicador_input,incremento_input,modulo_input,total_input) )
        sumbit_btn.grid(column=0,row=6, columnspan=4,pady=20)
    
    def aux_congruencial_frame(self,semilla,multiplicador,incremento,modulo,total):
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        
        if semilla.get() != '' and multiplicador.get()!= '' and incremento.get()!= '' and modulo.get()!= '' and total.get()!= '':
            try:
                x1 = int(semilla.get())
                x2 = int(multiplicador.get())  
                x3 = int(incremento.get())  
                x4 = int(modulo.get())
                x5 = int(total.get()) 
            except:
                self.errorText.set('Verifica que todos los campos sean Números Enteros')
                self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
                return
            
            titulo="Congurencial Lineal"
            self.congruencial(x1,x2,x3,x4,x5,titulo)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4)  
            
    def congruencial_mixto_frame(self, *args):
        
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="Método Congruencial Mixto"
        
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        semilla_label= ttk.Label(self.frame,  text='Semilla:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=1,pady=10,padx=10)
        semilla_input = ttk.Entry(self.frame, width=20)
        semilla_input.grid(column=1,row=1,padx=10)
        
        multiplicador_label= ttk.Label(self.frame,  text='Multiplicador:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=2,pady=10,padx=10)
        multiplicador_input = ttk.Entry(self.frame, width=20)
        multiplicador_input.grid(column=1,row=2,padx=10)
        
        incremento_label= ttk.Label(self.frame,  text='Incremento:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=3,pady=10,padx=10)
        incremento_input = ttk.Entry(self.frame, width=20)
        incremento_input.grid(column=1,row=3,padx=10)
        
        modulo_label= ttk.Label(self.frame,  text='Modulo:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=4,pady=10,padx=10)
        modulo_input = ttk.Entry(self.frame, width=20)
        modulo_input.grid(column=1,row=4,padx=10)
        
        total_label= ttk.Label(self.frame,  text='Total de Números a Generar:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=5,pady=10,padx=10)
        total_input = ttk.Entry(self.frame, width=20)
        total_input.grid(column=1,row=5,padx=10) 
        
        #Checkbox para verificar si el usuario quiere que se hagan las diferentes validaciones
        chi_cuadrada=tk.Checkbutton(self.frame, text="Chi-Cuadrada",variable=self.chi,justify="left")
        chi_cuadrada.grid(sticky = "W", column=2,row=1) 
        
        kolmogorov=tk.Checkbutton(self.frame, text="Kolmogorov-Smirnov", variable=self.kov,justify="left")
        kolmogorov.grid(sticky = "W",column=2,row=3) 
         
        helv36 = tkFont.Font(family='MS Sans Serif', size=10)
        porcentaje_Menu = tk.OptionMenu(
            self.frame,
            self.option2,
            *self.porcentajes,
           )
        porcentaje_Menu.config(font=helv36)
        
        porcentaje_Menu2 = tk.OptionMenu(
            self.frame,
            self.option3,
            *self.porcentajes2,
           )
        porcentaje_Menu2.config(font=helv36)
        
        porcentaje_Menu.grid(sticky = "e",column=3,row=1,padx=5) 
        porcentaje_Menu2.grid(sticky = "e",column=3,row=3,padx=5) 
        
        sumbit_btn= tk.Button(self.frame, 
                              text="Generar",
                              font = ("Castellar",8),  
                              command = lambda: self.aux_congruencial_mixto_frame(semilla_input,multiplicador_input,incremento_input,modulo_input,total_input) )
        sumbit_btn.grid(column=0,row=6, columnspan=4,pady=20)
    
    def aux_congruencial_mixto_frame(self,semilla,multiplicador,incremento,modulo,total):
        
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if semilla.get() != '' and multiplicador.get()!= '' and incremento.get()!= '' and modulo.get()!= '' and total.get()!= '':
            try:
                x1 = int(semilla.get())
                x2 = int(multiplicador.get())  
                x3 = int(incremento.get())  
                x4 = int(modulo.get())
                x5 = int(total.get()) 
            except:
                self.errorText.set('Verifica que todos los campos sean Números Enteros')
                self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
                return
            
            self.congruencialMixto(x1,x2,x3,x4,x5)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4)  
        
    def multiplicativo_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="Generador Multiplicativo"
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # Display de los inputs necesarios para el método
        semilla_label= ttk.Label(self.frame,  text='Semilla:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=1,pady=10,padx=10)
        semilla_input = ttk.Entry(self.frame, width=20)
        semilla_input.grid(column=1,row=1,padx=10)
        
        multiplicador_label= ttk.Label(self.frame,  text='Multiplicador:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=2,pady=10,padx=10)
        multiplicador_input = ttk.Entry(self.frame, width=20)
        multiplicador_input.grid(column=1,row=2,padx=10)
        
        modulo_label= ttk.Label(self.frame,  text='Modulo:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=3,pady=10,padx=10)
        modulo_input = ttk.Entry(self.frame, width=20)
        modulo_input.grid(column=1,row=3,padx=10)
        
        total_label= ttk.Label(self.frame,  text='Total de Números a Generar:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=4,pady=10,padx=10)
        total_input = ttk.Entry(self.frame, width=20)
        total_input.grid(column=1,row=4,padx=10) 
        
        #Checkbox para verificar si el usuario quiere que se hagan las diferentes validaciones
        chi_cuadrada=tk.Checkbutton(self.frame, text="Chi-Cuadrada",variable=self.chi,justify="left")
        chi_cuadrada.grid(sticky = "W", column=2,row=1) 
        
        kolmogorov=tk.Checkbutton(self.frame, text="Kolmogorov-Smirnov", variable=self.kov,justify="left")
        kolmogorov.grid(sticky = "W",column=2,row=3) 
         
        helv36 = tkFont.Font(family='MS Sans Serif', size=10)
        porcentaje_Menu = tk.OptionMenu(
            self.frame,
            self.option2,
            *self.porcentajes,
           )
        porcentaje_Menu.config(font=helv36)
        
        porcentaje_Menu2 = tk.OptionMenu(
            self.frame,
            self.option3,
            *self.porcentajes2,
           )
        porcentaje_Menu2.config(font=helv36)
        
        porcentaje_Menu.grid(sticky = "e",column=3,row=1,padx=5) 
        porcentaje_Menu2.grid(sticky = "e",column=3,row=3,padx=5) 
        
        sumbit_btn= tk.Button(self.frame, 
                              text="Generar",
                              font = ("Castellar",8),  
                              command = lambda: self.aux_multiplicativo_frame(semilla_input,multiplicador_input,modulo_input,total_input) )
        sumbit_btn.grid(column=0,row=5, columnspan=4,pady=20)
        
    def aux_multiplicativo_frame(self,semilla,multiplicador,modulo,total):
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if semilla.get() != '' and multiplicador.get()!= '' and modulo.get()!= '' and total.get()!= '':
            try:
                x1 = int(semilla.get())
                x2=int(multiplicador.get())  
                x3=int(modulo.get())
                x4=int(total.get()) 
            except:
                self.errorText.set('Verifica que todos los campos sean Números Enteros')
                self.errorMessage.grid_configure(column=0,row=0,columnspan=4) 
                return
            self.generadorMultiplicativo(x1,x2,x3,x4)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4)  
            
    def congruencial_lineal_combinado_frame(self, *args):
        
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="Método Congruencial Lineal Combinado"
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Display de los inputs necesarios para el método
        disclaimer = ttk.Label(self.frame,  text='Introduce tus valores con el siguiente formato: 456, 7891, 7831, ...',font = ("Castellar",8))
        disclaimer.grid(column=0,row=1,padx=10,pady=10,columnspan=2)
        
        semilla_label= ttk.Label(self.frame,  text='Semilla:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=2,padx=10,pady=10)
        semilla_input = ttk.Entry(self.frame, width=20)
        semilla_input.grid(column=1,row=2,padx=10)
        
        multiplicador_label= ttk.Label(self.frame,  text='Multiplicador:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=3,padx=10,pady=10)
        multiplicador_input = ttk.Entry(self.frame, width=20)
        multiplicador_input.grid(column=1,row=3,padx=10)
        
        modulo_label= ttk.Label(self.frame,  text='Modulo:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=4,padx=10,pady=10)
        modulo_input = ttk.Entry(self.frame, width=20)
        modulo_input.grid(column=1,row=4,padx=10)
        
        total_label= ttk.Label(self.frame,  text='Total de Números a Generar:',font = ("Castellar",8)).grid(sticky = "e",column=0,row=5,padx=10,pady=10)
        total_input = ttk.Entry(self.frame, width=20)     
        total_input.grid(column=1,row=5,padx=10)
        
        sumbit_btn= tk.Button(self.frame, 
                              text="Generar",
                              font = ("Castellar",8),  
                              command = lambda: self.aux_congruencial_lineal_combinado_frame(semilla_input,multiplicador_input,modulo_input,total_input) )
        
        sumbit_btn.grid(column=0,row=6, columnspan=4,pady=20)
        
    def aux_congruencial_lineal_combinado_frame(self,semilla,multiplicador,modulo,total):
        
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        
        if semilla.get() != '' and multiplicador.get()!= '' and modulo.get()!= '' and total.get()!= '':
            x1 = str(semilla.get())
            x2=str(multiplicador.get())  
            x3=str(modulo.get())
            try:
                x4=int(total.get()) 
            except:
                self.errorText.set('Numeros a Generar debe ser numero entero mayor a 0')
                self.errorMessage.grid_configure(column=0,row=0,columnspan=4)  
                return
            self.congruencialLinealCombinado(x1,x2,x3,x4)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=4)  
        
    def option_changed(self, *args):
        if self.option.get() == self.menu[0]:
            self.cuadrados_frame()
        elif self.option.get() == self.menu[1]:
            self.congruencial_frame()
        elif self.option.get() == self.menu[2]:
            self.congruencial_mixto_frame()
        elif self.option.get() == self.menu[3]:
            self.multiplicativo_frame()
        elif self.option.get() == self.menu[4]:
            self.congruencial_lineal_combinado_frame()        

if __name__ == "__main__":
    app = App()
    app.mainloop()
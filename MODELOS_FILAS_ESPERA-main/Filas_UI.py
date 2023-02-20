# -*- coding: utf-8 -*-
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib as mpl
from PIL import ImageTk, Image
from io import BytesIO
import os
import csv
import sympy as sp
from matplotlib.mathtext import math_to_image
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
import time

import matplotlib
matplotlib.use("TkAgg")

mpl.rcParams.update(mpl.rcParamsDefault)


class App(tk.Tk):

    def __init__(self):
        # Declaracion de la ventana principal y el tamaño de esta
        super().__init__()
        self.geometry("700x500")
        self.title('MODELOS DE FILAS DE ESPERA')
        self.descripciones = ['Factor de utilización',
                              'Notación simplificada para estado estable de sistema',
                              'Probabilidad de que el sistema esté ocioso',
                              'Probabilidad de que el sistema tenga n ',
                              'Promedio de clientes en la cola',
                              'Promedio de clientes en el sistema',
                              'Tiempo esperado en la cola',
                              'Tiempo promeido en el sistema',
                              "Tasa efectiva de arribo al sistema"]
        self.arreglo_titulo = ['p', 'Cn', 'P0',
                               'Pn', 'Lq', 'L', 'Wq', 'W', 'lambdaE']
        # Inicialización del menu principal
        self.menu = ("Modelo M/M/1",
                     "Modelo M/M/s",
                     "Modelo M/M/s/K",
                     "Modelo M/G/1",
                     "Modelo M/D/1",
                     "Modelo M/Erlang/s")

        # Variables para manjear las opciones del menu en caso de comprobaciones
        self.option = tk.StringVar(self)

        # create widget
        self.create_wigets()

    def create_wigets(self):
        # Paddings genéricos
        paddings = {'padx': 5, 'pady': 5}

        # Titulo de la ventana principal
        label = ttk.Label(
            self,  text='MODELOS DE FILAS DE ESPERA', font=("Castellar", 15))
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # Marco donde delimitamos los inputs de los diferentes métodos y declaración del mensaje de error
        self.frame = tk.LabelFrame(
            self, text="m_m_1_frame", borderwidth=8,  labelanchor="nw", font=("Castellar", 12))
        self.frame.grid(column=0, row=1, pady=20, padx=10, rowspan=4)
        self.errorText = tk.StringVar()
        self.errorText.set(" ")
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")

        # option menu
        option_menu = tk.OptionMenu(
            self,
            self.option,
            *self.menu,
            command=self.option_changed)

        helv36 = tkFont.Font(family='Castellar', size=8)
        option_menu.config(font=helv36)
        option_menu.grid(column=1, row=0, sticky='e', **paddings, columnspan=2)
        self.m_m_1_frame()

    def promedio(self, lista):
        suma = 0
        for element in lista:
            suma += element
        return (suma / len(lista))

    #-------------------------------------------------
    #Costos y Probabilidades
    
    def comprobacionPn(self, clientes, caso,widget,factor):

        self.errormsgprob.set('')

        if clientes != '':
            try:
                x1 = int(clientes)                
            except:
                self.errormsgprob.set(
                    'ERROR: Cliente NO es Entero')
                self.errorMessageProb.grid_configure(column=0+factor, row=2, columnspan=4,padx=(20,0))
                return False
            
            if x1 < 0:
                self.errormsgprob.set("ERROR: valores Negativos")
                self.errorMessageProb.grid_configure(column=0+factor, row=2, columnspan=3,padx=(20,0))
                return False
    
            if x1 == 0 and caso == "<":
                self.errormsgprob.set("Error: Clientes < 0")
                self.errorMessageProb.grid_configure(column=0+factor, row=2, columnspan=3,padx=(20,0))
                return False
        else:
            self.errormsgprob.set('Favor de dar un N')
            self.errorMessageProb.grid_configure(column=0+factor, row=2, columnspan=3,padx=(20,0))
            return False
        return True

    def comprobacionCostos(self,Cs,Cw,valoresServidores, valoresLq, carpeta,probWidget):
        self.errormsgcostos.set('')
        
        if Cs != '' and Cw !='':
            try:
                x1 = float(Cs)  
                x2 = float(Cw)  
            except:
                self.errormsgcostos.set(
                    'ERROR: Favor de Ingresar numeros')
                self.errorMessageCostos.grid_configure(column=0, row=6, columnspan=15,padx=(20,0))
                return False
            
            if x1 < 0 or x2 < 0:
                self.errormsgcostos.set("ERROR: valores Negativos")
                self.errorMessageCostos.grid_configure(column=0, row=6, columnspan=15,padx=(20,0))
                return False

        else:
            self.errormsgcostos.set('Favor de llenar todos los rubros')
            self.errorMessageCostos.grid_configure(column=0, row=6, columnspan=15,padx=(20,0))
            return False
        self.calculo_Costos(x2, x1, valoresServidores,valoresLq,carpeta,probWidget)
    
    def graphProb(self,arreglo,method,arreglo_prob):
        probWidget = tk.Toplevel()
        probWidget.title("Graficas y probabilidades")

        title = tk.Label(probWidget,
             text="Probabilidad", font=("Castellar", 13))
        title.grid(row=0, column=0,  padx=15, pady=(20,0) , columnspan=15)
        
        self.errormsgprob=  tk.StringVar()
        self.errormsgprob.set(" ")
        self.errorMessageProb = tk.Label(
            probWidget,  textvariable=self.errormsgprob, font=("Castellar", 8), fg="red")
        
        self.errormsgcostos =  tk.StringVar()
        self.errormsgcostos.set(" ")
        self.errorMessageCostos = tk.Label(
            probWidget,  textvariable=self.errormsgcostos, font=("Castellar", 8), fg="red") 
        
        self.labelsProb(probWidget,arreglo,method,arreglo_prob)
        
        title = tk.Label(probWidget,
             text="Costos", font=("Castellar", 13))
        title.grid(row=5, column=0,  padx=15, pady=(20,0) , columnspan=15)
        
        cs_label=tk.Label(probWidget,text="Costos Servidor:",font=("Verdana", 10))
        cs_label.grid(row=7, column=0,  padx=(20,0), pady=5, columnspan=3)

        cs_input = tk.Entry(probWidget, width=10)
        cs_input.grid(column=3, row=7, padx=(5,0),columnspan=2)
        
        cw_label=tk.Label(probWidget,text="Costos Clientes:",font=("Verdana", 10))
        cw_label.grid(row=7, column=5,  padx=(20,0), pady=5, columnspan=3)

        cw_input = tk.Entry(probWidget, width=10)
        cw_input.grid(column=8, row=7, padx=(0,0),columnspan=1)
        
        if method=="modelo_M_G_1" or method =="modelo_M_D_1" or method=="modelo_M_Ek_s":
           x=7
           y=8
        elif method=="modelo_M_M_s_K":
            x=9
            y=10
        else:
            x=8
            y=9
        costosBtn= tk.Button(probWidget,
                   text="Calcular",
                   font=("Verdana", 7),
                   command=lambda: self.comprobacionCostos(cs_input.get(), cw_input.get(),arreglo[1][x],arreglo[1][y],method,probWidget ))
        costosBtn.grid(column=9, row=7, columnspan=3, pady=10)  
      
    def calculo_Costos(self,Cw, Cs, valoresServidores, valoresLq, carpeta,probWidget):
        
        self.creacionCarpeta(carpeta)
        valoresCw = []
        valoresCs = []
        valoresCt = []
        info_tabla = []
        info_tabla.append(["Ct (USD)", "Cw (USD)", "Cs (USD)"])
        for index in range(0, len(valoresServidores)):
            valoresCw.append(round(valoresLq[index] * Cw, 6))
            valoresCs.append(round(valoresServidores[index] * Cs, 6))
            valoresCt.append(round(valoresCw[index] + valoresCs[index], 6))
            info_tabla.append([valoresCt[index],valoresCw[index], valoresCs[index]])
    
        costoOriginal = valoresCt[0] ##ESTE ES EL COSTO A DESPLEGAR EN LA PARTE DE ABAJO
    
        try:
            self.escrituraCsv(info_tabla, carpeta)
        except:
            print("No se pudo generar el archivo csv")
            
      
        f = Figure(figsize=(6, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(valoresServidores, valoresCw, label="Costo por tiempo espera (USD)")
        a.plot(valoresServidores, valoresCs, label="Costo por servicio (USD)")
        a.plot(valoresServidores, valoresCt, label="Costo Total Esperado (USD)")

        a.set_xticks(range(valoresServidores[0], valoresServidores[len(valoresServidores) - 1] + 1))
        a.set_ylabel("Costo por unidad de tiempo (USD)")
        a.set_xlabel("Numero de servidores atendiendo a clientes")
        a.legend()
        canvas = FigureCanvasTkAgg(f, master=probWidget)
        canvas.get_tk_widget().grid(row=9,column=0,columnspan=14)
        
        toolbarFrame = tk.Frame(master=probWidget)
        toolbarFrame.grid(row=10,column=0,columnspan=14)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        
        labelCt=tk.Label(probWidget,
             text=("Costo Total: "+str(costoOriginal)+" USD"), font=("Castellar", 13))
        labelCt.grid(row=11,column=0,columnspan=14)

    def creacionCarpeta(self,nombreCarpeta):
        pathActual = os.getcwd()
        pathActual = pathActual.replace("\\", "/")
        pathCarpeta = pathActual + "/" + nombreCarpeta + "/"
        if os.path.exists(pathCarpeta):
            pass
        else:
            os.mkdir(pathCarpeta)
    
    def escrituraCsv(self,datos, carpetaArchivo):
        pathActual = os.getcwd()
        pathActual = pathActual.replace("\\", "/")
        pathActual = pathActual + "/" + carpetaArchivo + "/"
    
        t = time.localtime()
        nombreArchivo = time.strftime("%H:%M:%S", t)
        nombreArchivo = nombreArchivo.replace(":", "_") 
        nombreArchivo += carpetaArchivo + ".csv"
        nombreArchivo = pathActual + nombreArchivo
    
        with open(nombreArchivo, "w", newline = "") as file:
            escritor = csv.writer(file)
            escritor.writerows(datos)

    def labelsProb(self,probWidget,arreglo,method,arreglo_prob):
        subEquals=tk.Label(probWidget,
             text="P(N=n)", font=("Verdana", 11))
        subEquals.grid(row=1, column=0,  padx=22, pady=5, columnspan=2)
        
        n_eq=tk.Label(probWidget,text="n",font=("Verdana", 10))
        n_eq.grid(row=3, column=0,  padx=(20,0), pady=5)
    
        equals_input = tk.Entry(probWidget, width=10)
        equals_input.grid(column=1, row=3, padx=(0,0))
        
        eq_l_eq=tk.Label(probWidget,text="=",font=("Verdana", 10))
        eq_l_eq.grid(row=3, column=2,  padx=5, pady=5)
        
        res_eq_input = tk.Entry(probWidget, width=10)
        res_eq_input.grid(column=3, row=3, padx=(0,0))
        res_eq_input.configure(state=tk.DISABLED)
        
        subGre=tk.Label(probWidget,
             text="P(N>n)", font=("Verdana", 11))
        subGre.grid(row=1, column=5,  padx=30, pady=5,columnspan=2)
        
        n_gre=tk.Label(probWidget,text="n",font=("Verdana", 10))
        n_gre.grid(row=3, column=5,  padx=(25,0), pady=5)
        
        greater_input = tk.Entry(probWidget, width=10)
        greater_input.grid(column=6, row=3, padx=(0,0))
        
        gre_l_eq=tk.Label(probWidget,text="=",font=("Verdana", 10))
        gre_l_eq.grid(row=3, column=7,  padx=5, pady=5)
        
        res_gre_input = tk.Entry(probWidget, width=10)
        res_gre_input.grid(column=8, row=3, padx=(0,0))
        res_gre_input.configure(state=tk.DISABLED)
        
        subLess=tk.Label(probWidget,
             text="P(N<n)", font=("Verdana", 11))
        subLess.grid(row=1, column=9,  padx=30, pady=5,columnspan=2)
        
        n_less=tk.Label(probWidget,text="n",font=("Verdana", 10))
        n_less.grid(row=3, column=9,  padx=(25,0), pady=5)
        
        less_input = tk.Entry(probWidget, width=10)
        less_input.grid(column=10, row=3, padx=(0,0))
        
        less_l_eq=tk.Label(probWidget,text="=",font=("Verdana", 10))
        less_l_eq.grid(row=3, column=11,  padx=5, pady=5)
        
        less_re_input = tk.Entry(probWidget, width=10)
        less_re_input.grid(column=12, row=3, padx=(0,10)) 
        less_re_input.configure(state=tk.DISABLED)
        
        equalsBtn= tk.Button(probWidget,
                           text="Calcular",
                           font=("Verdana", 7),
                
                            command=lambda: self.probabilidades(probWidget,method,"=",equals_input,arreglo,res_eq_input,arreglo_prob))
        equalsBtn.grid(column=0, row=4, columnspan=4, pady=10)
         
        greaterBtn= tk.Button(probWidget,
                           text="Calcular",
                           font=("Verdana", 7),
                
                            command=lambda: self.probabilidades(probWidget,method,">",greater_input,arreglo,res_gre_input,arreglo_prob))
        greaterBtn.grid(column=5, row=4, columnspan=4, pady=10)
    
        lessBtn= tk.Button(probWidget,
                           text="Calcular",
                           font=("Verdana", 7),
                
                            command=lambda: self.probabilidades(probWidget,method,"<",less_input,arreglo,less_re_input,arreglo_prob))
        lessBtn.grid(column=9, row=4, columnspan=4, pady=10)

    def probabilidades(self,probWidget,method,caso,n,arreglo,resContainer,arreglo_prob):
        if(caso=="="):
            x=0
        elif(caso==">"):
            x=5
        elif(caso=="<"):
            x=9
            
        if self.comprobacionPn(n.get(),caso,probWidget,x):
            if method=="modelo_M_M_1":
                print("mm1")
                self.calculo_Pn_Modelo_M_M_1(arreglo[1][2],arreglo[1][0],int(n.get()),caso,resContainer)
            if method=="modelo_M_M_s":
                print("mms")
                self.calculo_Pn_Modelo_M_M_s(arreglo[1][2],arreglo_prob[0],arreglo_prob[1],arreglo_prob[2],int(n.get()),caso,resContainer)
            if method=="modelo_M_M_s_K":
                print("mmsk")
                self.calculo_Pn_Modelo_M_M_s_K(arreglo[1][2],arreglo_prob[0],arreglo_prob[1],arreglo_prob[2],arreglo_prob[3],int(n.get()),caso,resContainer)
            if method=="modelo_M_G_1" or method =="modelo_M_D_1" or method=="modelo_M_Ek_s":
                print("mg1")
                self.calculo_Pn_Modelo_M_M_1(arreglo[1][1],arreglo[1][0],int(n.get()),caso,resContainer)    
    
    def calculo_Pn_Modelo_M_M_1(self,pCero, p, clientes, caso,container):
        if caso == "=":
            if clientes == 0:
                pN = pCero
            else:
                pN = round((pCero * pow(p, clientes)), 4)
        elif caso == ">":
            if clientes == 0:
                pN = 1 - pCero
            else:
                pN = 1
                acumulado = pCero
                for cliente in range(1, clientes + 1):
                    acumulado += round((pCero * pow(p, cliente)), 4)
                pN = pN - acumulado
        else:
            if clientes == 1:
                pN = pCero
            else:
                pN = pCero
                for cliente in range(1, clientes+1):
                    pN += round((pCero * pow(p, cliente)), 4)
        print(round(pN, 4))
        container.configure(state=tk.NORMAL)
        container.delete(0,tk.END)
        container.insert(tk.END, round(pN, 4))
        container.configure(state=tk.DISABLED)
        return round(pN, 4)

    def calculo_Pn_Modelo_M_M_s(self,pCero, lamda, mu, s, clientes, caso,container):

        if caso == "=":
            if clientes == 0:
                pN = pCero
            elif (clientes >= 0) and (s > clientes):
                pN = round((((pow(lamda/mu,clientes)) / self.factorial(clientes)) * pCero), 4)
            else:
                pN = round((((pow(lamda/mu,clientes)) / (self.factorial(s) * pow(s, clientes-s))) * pCero), 4)
        elif caso == ">":
            if clientes == 0:
                pN = 1 - pCero
            else:
                pN = 1
                acumulado = pCero
                for cliente in range(1, clientes + 1):
                    if (cliente >= 0) and (s > cliente):
                        acumulado += round((((pow(lamda/mu,cliente)) / self.factorial(cliente)) * pCero), 4)
                    else:
                        acumulado += round((((pow(lamda/mu,cliente)) / (self.factorial(s) * pow(s, cliente-s))) * pCero), 4)
                pN = pN - acumulado
        else:
            if clientes == 1:
                pN = pCero
            else:
                pN = pCero
                for cliente in range(1, clientes+1):
                    if (cliente >= 0) and (s > cliente):
                        pN += round((((pow(lamda/mu,cliente)) / self.factorial(cliente)) * pCero), 4)
                    else:
                        pN+= round((((pow(lamda/mu,cliente)) / (self.factorial(s) * pow(s, cliente-s))) * pCero), 4)
        print(round(pN, 4))
        container.configure(state=tk.NORMAL)
        container.delete(0,tk.END)
        container.insert(tk.END, round(pN, 4))
        container.configure(state=tk.DISABLED)
        return(round(pN, 4))
    
    def calculo_Pn_Modelo_M_M_s_K(self,pCero, lamda, mu, s, K, clientes, caso,container):

        if caso == "=":
            if clientes == 0:
                pN = pCero
            elif clientes <= (s - 1):
                pN = round((((pow((lamda / mu), clientes)) / (self.factorial(clientes))) * pCero), 4)
            elif clientes == s or clientes < (s + 1) or clientes == K:
                pN = round((((pow((lamda / mu), clientes)) / (self.factorial(s) * pow(s, clientes - s))) * pCero), 4)
            else:
                pN = 0
        elif caso == ">":
            if clientes == 0:
                pN = 1 - pCero
            else:
                pN = 1
                acumulado = pCero
                for cliente in range(1, clientes + 1):
                    if cliente <= (s - 1):
                        acumulado += round((((pow((lamda / mu), cliente)) / (self.factorial(cliente))) * pCero), 4)
                    elif cliente == s or cliente < (s + 1) or cliente == K:
                        acumulado += round((((pow((lamda / mu), cliente)) / (self.factorial(s) * pow(s, cliente - s))) * pCero), 4)
                    else:
                        acumulado += 0
                pN = pN - acumulado
        else:
            if clientes == 1:
                pN = pCero
            else:
                pN = pCero
                for cliente in range(1, clientes + 1):
                    if cliente <= (s - 1):
                        pN += round((((pow((lamda / mu), cliente)) / (self.factorial(cliente))) * pCero), 4)
                    elif cliente == s or cliente < (s + 1) or cliente == K:
                        pN += round((((pow((lamda / mu), cliente)) / (self.factorial(s) * pow(s, cliente - s))) * pCero), 4)
                    else:
                        pN += 0
        print(round(pN, 4))
        container.configure(state=tk.NORMAL)
        container.delete(0,tk.END)
        container.insert(tk.END, round(pN, 4))
        container.configure(state=tk.DISABLED)
        return(round(pN, 4))

    #-------------------------------------------------------------
    #Tabla de resultados 2nda pantalla

    def mm1_iniciacionDeTabla(self, arreglo, frame_result, tiempo, method, size,arreglo_prob):
        helv36 = tkFont.Font(family='Helvetica',
                             size=11, weight='bold')
        for i in range(size):

            l = tk.Label(frame_result,
                         borderwidth=2,
                         justify=tk.CENTER,
                         foreground="White",
                         background="green",
                         text=(arreglo[0][i]))

            l.grid(row=i+1, column=0, sticky='NSEW')

        for i in range(size):
            if(i >= 6):
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i], padx=10)
            label1.grid(column=3, row=i+1, sticky='w')
        addBtn = tk.Button(frame_result,
                           text="Costos y Probabilidades",
                           font=("Castellar", 8),
                           fg="green",
                            command=lambda: self.graphProb(arreglo,method,arreglo_prob))
        addBtn.grid(column=0, row=10, columnspan=5, pady=10)

    def mm1_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()
        buffer2 = BytesIO()
        for i in range(size):

            if i == 1:
                math_to_image(r'${0}^n$'.format(
                    str(arreglo[1][1])), buffer, dpi=100, format='png')
                buffer.seek(0)

                pimage = Image.open(buffer)
                image = ImageTk.PhotoImage(pimage)

                l = tk.Label(frame_result, image=image, text="")
                l.img = image
                l.grid(row=i+1, column=1, sticky='NSEW')
            elif i == 3:
                math_to_image(r'${0}({1}^n)$'.format(str(arreglo[1][2]), str(
                    arreglo[1][0])), buffer2, dpi=100, format='jpg')
                buffer2.seek(0)

                pimage2 = Image.open(buffer2)
                image2 = ImageTk.PhotoImage(pimage2)

                l2 = tk.Label(frame_result, image=image2)
                l2.img = image2
                l2.grid(row=i+1, column=1, sticky='NSEW')
            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=i+1, column=1, sticky='NSEW')

        buffer.flush()
        buffer2.flush()

    def mms_iniciacionDeTabla(self, arreglo, frame_result, tiempo, method, size,arreglo_prob):
        helv36 = tkFont.Font(family='Helvetica',
                             size=11, weight='bold')
        x = 0
        for i in range(size):
            if i == 1 or i == 3:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             height=10,
                             width=7,
                             foreground="White",
                             background="green",
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, rowspan=2, padx=5, pady=2)
                x += 2
            else:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             foreground="White",
                             background="green",
                             height=3,
                             width=7,
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, padx=5, pady=2)
                x += 1
        x = 0
        for i in range(size):
            if(i >= 6):
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i], padx=10)

            if i == 1 or i == 3:
                label1.grid(column=3, row=x+1, sticky='NSEW')
                x += 2
            else:
                label1.grid(column=3, row=x+1, sticky='w')
                x += 1

        addBtn = tk.Button(frame_result,
                           text="Costos y Probabilidades",
                           font=("Castellar", 8),
                           fg="green",
                           command=lambda: self.graphProb(arreglo,method,arreglo_prob))
        addBtn.grid(column=0, row=12, columnspan=5, pady=10)

    def mms_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()
        buffer2 = BytesIO()
        buffer3 = BytesIO()
        buffer4 = BytesIO()
        arrayBuffer = [buffer, buffer2, buffer3, buffer4]

        x = 0
        for i in range(size):

            # print(arreglo[1][3][0])
            if i == 1:

                for y in range(2):
                    math_to_image(arreglo[1][1][y],
                                  arrayBuffer[y], dpi=150, format='jpg')
                    arrayBuffer[y].seek(0)
                    pimage = Image.open(arrayBuffer[y])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 1

            elif i == 3:
                for y in range(2):
                    math_to_image(arreglo[1][3][y],
                                  arrayBuffer[y+2], dpi=150, format='jpg')
                    arrayBuffer[y+2].seek(0)
                    pimage = Image.open(arrayBuffer[y+2])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 1

            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=x+1, column=1, sticky='NSEW')
            x += 1
        buffer.flush()
        buffer2.flush()
        buffer3.flush()
        buffer4.flush()

    def mmsK_iniciacionDeTabla(self, arreglo, frame_result, tiempo, method, size,arreglo_prob):
        helv36 = tkFont.Font(family='Helvetica',
                             size=11, weight='bold')
        x = 0
        for i in range(size):
            if i == 1 or i == 3:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             height=10,
                             width=7,
                             foreground="White",
                             background="green",
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, rowspan=3, padx=5, pady=2)
                x += 3
            else:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             foreground="White",
                             background="green",
                             height=3,
                             width=7,
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, padx=5, pady=2)
                x += 1
        x = 0
        for i in range(size):
            if(i >= 6):
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i], padx=10)

            if i == 1 or i == 3:
                label1.grid(column=3, row=x+1, sticky='NSEW')
                x += 3
            else:
                label1.grid(column=3, row=x+1, sticky='w')
                x += 1

        addBtn = tk.Button(frame_result,
                           text="Costos y Probabilidades",
                           font=("Castellar", 8),
                           fg="green",
                           command=lambda: self.graphProb(arreglo,method,arreglo_prob))
        addBtn.grid(column=0, row=15, columnspan=5, pady=10)

    def mmsK_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()
        buffer2 = BytesIO()
        buffer3 = BytesIO()
        buffer4 = BytesIO()
        buffer5 = BytesIO()
        buffer6 = BytesIO()
        arrayBuffer = [buffer, buffer2, buffer3, buffer4, buffer5, buffer6]

        x = 0
        for i in range(size):

            print(arreglo[1][3][2])
            if i == 1:

                for y in range(3):
                    math_to_image(arreglo[1][1][y],
                                  arrayBuffer[y], dpi=150, format='jpg')
                    arrayBuffer[y].seek(0)
                    pimage = Image.open(arrayBuffer[y])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 2

            elif i == 3:
                for y in range(3):
                    math_to_image(arreglo[1][3][y],
                                  arrayBuffer[y+3], dpi=150, format='jpg')
                    arrayBuffer[y+3].seek(0)
                    pimage = Image.open(arrayBuffer[y+3])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 2

            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=x+1, column=1, sticky='NSEW')
            x += 1
        buffer.flush()
        buffer2.flush()
        buffer3.flush()
        buffer4.flush()

    def mg1_iniciacionDeTabla(self, arreglo, frame_result, tiempo, size,method,arreglo_prob):
        descripciones2 = ['Factor de utilización',
                              'Probabilidad de que el sistema esté ocioso',
                              'Probabilidad de que el sistema tenga n ',
                              'Promedio de clientes en la cola',
                              'Promedio de clientes en el sistema',
                              'Tiempo esperado en la cola',
                              'Tiempo promeido en el sistema']
        for i in range(size):
            
            l = tk.Label(frame_result,
                         borderwidth=2,
                         justify=tk.CENTER,
                         foreground="White",
                         background="green",
                         text=(arreglo[0][i]))

            l.grid(row=i+1, column=0, sticky='NSEW')

        for i in range(size):
            if(i >= 5):
                label1 = tk.Label(
                    frame_result, text=arreglo[0][i]+" : "+descripciones2[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=arreglo[0][i]+" : "+descripciones2[i], padx=10)
            label1.grid(column=3, row=i+1, sticky='w')
        addBtn = tk.Button(frame_result,
                           text="Costos y Probabilidades",
                           font=("Castellar", 8),
                           fg="green",
                           command=lambda: self.graphProb(arreglo,method,arreglo_prob))
        addBtn.grid(column=0, row=10, columnspan=5, pady=10)

    def mg1_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()

        for i in range(size):

            if i == 2:
                math_to_image(r'${0}({1}^n)$'.format(str(arreglo[1][1]), str(
                    arreglo[1][0])), buffer, dpi=100, format='jpg')
                buffer.seek(0)

                pimage2 = Image.open(buffer)
                image2 = ImageTk.PhotoImage(pimage2)

                l2 = tk.Label(frame_result, image=image2)
                l2.img = image2
                l2.grid(row=i+1, column=1, sticky='NSEW')
            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=i+1, column=1, sticky='NSEW')

        buffer.flush()

    #-------------------------------------------------------------
    #Modelos Matimaticos    

    def factorial(self, numero):
        factorial = 1
        for i in range(1, numero + 1):
            factorial = factorial * i
        return factorial

    def comprobacion_Modelo_M_M_1(self, lamda, mu):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(lamda > mu or lamda == mu):
            self.errorText.set(
                "El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_M_1(self, lamda, mu, tiempo):
        p = round((lamda / mu), 4)
        Cn = p
        pCero = round((1 - p), 4)
        # round((pCero * pow(p, n)), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"
        Lq = round((pow(lamda, 2) / (mu * (mu - lamda))), 4)
        L = round((lamda / (mu - lamda)), 4)
        Wq = round((lamda / (mu * (mu - lamda))), 4)
        W = round((1 / (mu - lamda)), 4)

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        valores_servidores = list(range(1,9))
        valores_Lq = []
        valores_Lq.append(Lq)
        for valor in valores_servidores[1:]:
            p_valor = round((lamda / (valor * mu)), 6)
            primerTerminoPCero = 0
            for index in range (0, valor): #el ciclo solo hace hasta s - 1
                primerTerminoPCero += (pow(lamda/mu, index) / self.factorial(index))
            PCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, valor) / self.factorial(valor)) * (1 / (1 - (lamda / (valor * mu)))))), 6)
            valores_Lq.append(round(((PCero * pow(lamda / mu, valor) * p_valor) / (self.factorial(valor) * pow((1 - p_valor), 2))), 6))

        arreglo_valores_UI.append(valores_servidores)
        arreglo_valores_UI.append(valores_Lq)
        
        arreglo_tabla = [self.arreglo_titulo, arreglo_valores_UI]
        arreglo_prob=[lamda,mu,tiempo]
        results = tk.Toplevel()
        results.title("Resultados")

        result_title = tk.Label(results, text='Resultados del Modelo M/M/1 :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)

        # self.creacionTabla(arreglo_tabla,results,tiempo,"m/m/1",8)
        self.mm1_iniciacionDeTabla(
            arreglo_tabla, results, tiempo, "modelo_M_M_1", 8,arreglo_prob)
        self.mm1_tabla_latex(arreglo_tabla, results, 8)

    def comprobacion_Modelo_M_M_s(self, lamda, mu, s):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        """if(lamda > mu or lamda == mu):
            print("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            return False"""
        if(mu * s <= lamda):
            self.errorText.set(
                "El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s < 0):
            self.errorText.set("El valor de s es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s % 1 != 0):
            self.errorText.set("El valor de s NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_M_s(self, lamda, mu, tiempo, s):

        p = round((lamda / (s * mu)), 4)
        temp1 = str(round((lamda/mu), 4))
        temp2 = str(self.factorial(s))
        Cn = []

        Cn1 = r'$ (\frac{{{0}^n}} {{n!}}) \Longrightarrow 0 \leq n < s$.'.format(
            temp1)
 
        Cn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-{2}}} ) }}) \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s)

        Cn.extend([Cn1, Cn2])

        primerTerminoPCero = 0
        for index in range(0, s):  # el ciclo solo hace hasta s - 1
            primerTerminoPCero += (pow(lamda/mu, index) /
                                   self.factorial(index))
        pCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, s) /
                      self.factorial(s)) * (1 / (1 - (lamda / (s * mu)))))), 4)
        pN = []
        Pn1 = r'$ (\frac{{{0}^n}} {{n!}}){{{1}}} \Longrightarrow 0 \leq n < s$.'.format(
            temp1, pCero)

        Pn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-{2}}} ) }}){{{3}}} \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s, pCero)

        pN.extend([Pn1, Pn2])
        """if n >= 0 and n < s:
            pN = round((((pow(lamda/mu,n)) / factorial(n)) * pCero), 4)
        else:
            pN = round((((pow(lamda/mu,n)) / (factorial(s) * pow(s, n-s))) * pCero), 4)"""
        Lq = round(((pCero * pow(lamda / mu, s) * p) /
                   (self.factorial(s) * pow((1 - p), 2))), 4)
        L = round((Lq + (lamda / mu)), 4)
        Wq = round((Lq / lamda), 4)
        W = round((Wq + (1/mu)), 4)
       
        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        
        valores_servidores = list(range(s,s + 8))
        valores_Lq = []
        valores_Lq.append(Lq)
        for valor in valores_servidores[1:]:
            p_valor = round((lamda / (valor * mu)), 6)
            primerTerminoPCero = 0
            for index in range (0, valor): #el ciclo solo hace hasta s - 1
                primerTerminoPCero += (pow(lamda/mu, index) / self.factorial(index))
            PCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, valor) / self.factorial(valor)) * (1 / (1 - (lamda / (valor * mu)))))), 6)
            valores_Lq.append(round(((PCero * pow(lamda / mu, valor) * p_valor) / (self.factorial(valor) * pow((1 - p_valor), 2))), 6))

        print(valores_servidores)
        print(valores_Lq)
        arreglo_valores_UI.append(valores_servidores)
        arreglo_valores_UI.append(valores_Lq)
        
        arreglo_tabla = [self.arreglo_titulo, arreglo_valores_UI]
        arreglo_prob=[lamda,mu,s,tiempo]
        
        results = tk.Toplevel()
        results.title("Resultados")
        rows = []
        result_title = tk.Label(results, text='Resultados del Modelo M/M/S :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)
        # self.creacionTabla(arreglo_tabla,results,tiempo,"M/M/S",8)
        self.mms_iniciacionDeTabla(arreglo_tabla, results, tiempo, "modelo_M_M_s", 8,arreglo_prob)
        self.mms_tabla_latex(arreglo_tabla, results, 8)

    def comprobacion_Modelo_M_M_s_K(self, lamda, mu, s, K):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(mu * s <= lamda):
            self.errorText.set(
                "El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(K < 0):
            self.errorText.set("El valor de K es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(K % 1 != 0):
            self.errorText.set("El valor de K NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s < 0):
            self.errorText.set("El valor de s es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s % 1 != 0):
            self.errorText.set("El valor de s NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s > K):
            self.errorText.set(
                "El valor de K debe ser menor o igual a S para este modelo")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_M_s_K(self, lamda, mu, tiempo, s, K):
        p = round((lamda / (s * mu)), 4)
        Cn = []
        temp1 = str(round((lamda/mu), 4))
        temp2 = str(self.factorial(s))
        #Cn1 = "(" + str(round((lamda/mu), 4)) + " ** n) / n!"
        Cn1 = r'$ (\frac{{{0}^n}} {{n!}}) \Longrightarrow 0 \leq n < s$.'.format(
            temp1)

        Cn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-{2}}} ) }}) \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s)
        Cn3 = r'$ 0 \Longrightarrow n\geq K$.'
        # Cn1 es para casos donde n = 0,1,2,...,s-1,  Cn2 es para casos donde n = s,s+1,...K y Cn3 es para casos donde n > K
        Cn.extend([Cn1, Cn2, Cn3])

        primerTerminoPCero = 0
        for index in range(0, (s+1)):  # el ciclo solo llega a s
            primerTerminoPCero += (pow((lamda / mu), index)
                                   ) / (self.factorial(index))
        tercerTerminoPCero = 0
        for index in range((s+1), (K + 1)):  # el ciclo solo llega a K
            tercerTerminoPCero += pow(lamda / (s * mu), (index - s))
        pCero = round((1 / (primerTerminoPCero + (pow((lamda / mu),
                      s) / self.factorial(s)) * tercerTerminoPCero)), 4)
        pN = []
        Pn1 = r'$ (\frac{{{0}^n}} {{n!}}){{{1}}} \Longrightarrow 0 \leq n < s$.'.format(
            temp1, pCero)
        Pn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-{2}}} ) }}){{{3}}} \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s, pCero)

        Pn3 = r'$ 0 \Longrightarrow n\geq K$.'
        pN.extend([Pn1, Pn2, Pn3])

        Lq = round((((pCero * (pow((lamda / mu), s)) * p) / (self.factorial(s) * (pow((1 - p), 2))))
                   * (1 - pow(p, K - s) - (K - s) * pow(p, K - s) * (1 - p))), 4)

        if K <= (s - 1):
            pK = round(
                (((pow((lamda / mu), K)) / (self.factorial(K))) * pCero), 4)
        elif K == s or K < (s + 1) or K == K:
            pK = round(
                (((pow((lamda / mu), K)) / (self.factorial(s) * pow(s, (K - s)))) * pCero), 4)
        else:
            pK = 0
        lamdaE = round((lamda * (1 - pK)), 4)
        Wq = round((Lq / lamdaE), 4)
        W = round((Wq + (1 / mu)), 4)
        L = round((lamdaE * W), 4)

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W, lamdaE]

        valores_servidores = list(range(s, K+1))
        if len(valores_servidores) > 8:
            valores_servidores = valores_servidores[0:8]
        valores_Lq = []
        valores_Lq.append(Lq)
        for valor in valores_servidores[1:]:
            p_valor = round((lamda / (valor * mu)), 6)
            primerTerminoPCero = 0
            for index in range (0, (valor+1)): #el ciclo solo llega a s
                primerTerminoPCero += (pow((lamda / mu), index)) / (self.factorial(index))
            tercerTerminoPCero = 0
            for index in range((valor+1), (K + 1)): #el ciclo solo llega a K
                tercerTerminoPCero += pow(lamda / (valor * mu), (index - valor))
            PCero = round((1 / (primerTerminoPCero + (pow((lamda / mu), valor) / self.factorial(valor)) * tercerTerminoPCero)), 6)
            valores_Lq.append(round((((PCero * (pow((lamda / mu), valor)) * p_valor) / (self.factorial(valor) * (pow((1 - p_valor), 2)))) * (1 - pow(p_valor, K - valor) - (K- valor) * pow(p_valor, K - valor) * (1 - p_valor))), 6))

        arreglo_valores_UI.append(valores_servidores)
        arreglo_valores_UI.append(valores_Lq)

        arreglo_tabla = [self.arreglo_titulo, arreglo_valores_UI]
        arreglo_prob=[lamda,mu,s,K,tiempo]
        results = tk.Toplevel()
        results.title("Resultados")
        rows = []
        result_title = tk.Label(results, text='Resultados del Modelo M/M/S/K :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)

        self.mmsK_iniciacionDeTabla(arreglo_tabla, results, tiempo, "modelo_M_M_s_K", 9,arreglo_prob)
        self.mmsK_tabla_latex(arreglo_tabla, results, 9)

    def comprobacion_Modelo_M_G_1(self,lamda, mu, desviacion):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False  
        if(lamda > mu or lamda == mu):
            self.errorText.set("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if((type(desviacion) != int) and (type(desviacion) != float)):
            self.errorText.set("El valor de la desviacion debe ser ENTERO/Decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(desviacion < 0):
            self.errorText.set("El sistema M/G/1 tiene que tener una desv. estandar mayor a 0 ")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_G_1(self,lamda, mu, tiempo, desviacion):
        s = 1 #Pero hay que checar svenx
        p = round((lamda / mu), 4)
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((((pow(lamda,2) * pow(desviacion,2))+ pow(p,2))/(2*(1-p))) , 4) #formula de pollaczek khintchine
        L = round((p + Lq), 4)
        Wq = round((Lq/lamda), 4)
        W = round((Wq + (1/mu)), 4)

        arreglo_valores_UI = [p, pCero, pN, Lq, L, Wq, W]
        
        valores_servidores = list(range(1,9))
        valores_Lq = []
        valores_Lq.append(Lq)
        for valor in valores_servidores[1:]:
            p_valor = round((lamda / (valor * mu)), 6)
            valores_Lq.append(p_valor + round((((pow(lamda,2) * pow(desviacion,2))+ pow(p_valor,2))/(2*(1-p_valor))) , 6))

        print(valores_servidores)
        print(valores_Lq)
        arreglo_valores_UI.append(valores_servidores)
        arreglo_valores_UI.append(valores_Lq)
        
        arreglo_titulo2 = ['p', 'P0',
                               'Pn', 'Lq', 'L', 'Wq', 'W']
        arreglo_tabla = [arreglo_titulo2, arreglo_valores_UI]
        results = tk.Toplevel()
        results.title("Resultados")
        arreglo_prob=[lamda,mu,desviacion,tiempo]
        result_title = tk.Label(results, text='Resultados del Modelo M/G/1 :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)
        self.mg1_iniciacionDeTabla(
            arreglo_tabla, results, tiempo,  7,"modelo_M_G_1",arreglo_prob)
        self.mg1_tabla_latex(arreglo_tabla, results, 7)

    def comprobacion_Modelo_M_D_1(self,lamda, mu):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False  
        if(lamda > mu or lamda == mu):
            self.errorText.set("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False

        return True
    
    def modelo_M_D_1(self,lamda, mu, tiempo):
        s = 1 #Pero hay que checar svenx

        p = round((lamda / mu), 4)
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((pow(p,2)/(2*(1-p))) , 4) #formula de pollaczek khintchine con desv = 0
        L = round((p + Lq), 4)
        Wq = round((Lq/lamda), 4)
        W = round((Wq + (1/mu)), 4)

        arreglo_valores_UI = [p, pCero, pN, Lq, L, Wq, W]
        arreglo_titulo2 = ['p', 'P0',
                               'Pn', 'Lq', 'L', 'Wq', 'W']
        
        valores_servidores = list(range(1,9))
        valores_Lq = []
        valores_Lq.append(Lq)
        for valor in valores_servidores[1:]:
            p_valor = round((lamda / (valor * mu)), 6)
            valores_Lq.append(p_valor + round((pow(p_valor,2)/(2*(1-p_valor))), 6))

        print(valores_servidores)
        print(valores_Lq)
        arreglo_valores_UI.append(valores_servidores)
        arreglo_valores_UI.append(valores_Lq)
        
        arreglo_tabla = [arreglo_titulo2, arreglo_valores_UI]
        arreglo_prob=[lamda,mu,tiempo]
        results = tk.Toplevel()
        results.title("Resultados")

        result_title = tk.Label(results, text='Resultados del Modelo M/D/1 :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)
        self.mg1_iniciacionDeTabla(
            arreglo_tabla, results, tiempo,  7,"modelo_M_D_1",arreglo_prob)
        self.mg1_tabla_latex(arreglo_tabla, results, 7)
    
    def comprobacion_modelo_M_Ek_s(self,lamda, mu, K,s):

        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False  
        if(lamda > mu or lamda == mu):
            self.errorText.set("El sistema siendo planeteado NO es estable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(K < 0):
            self.errorText.set("El valor de K es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(K % 1 != 0):
            self.errorText.set("El valor de K NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s < 0):
            self.errorText.set("El valor de s es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s % 1 != 0):
            self.errorText.set("El valor de s NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True
    
    def modelo_M_Ek_s(self,lamda, mu, s, tiempo, k):

        p = round((lamda / (s * mu)), 4)
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((((1 + k) / (2 * k)) * ((pow(lamda,2)) / (mu * (mu - lamda)))), 4) #formula de pollaczek khintchine para modelo Erlang
        Wq = round((Lq/ lamda), 4)
        W = round((Wq + (1/mu)), 4)
        L = round((lamda * W), 4)


        arreglo_valores_UI = [p, pCero, pN, Lq, L, Wq, W]
        arreglo_titulo2 = ['p', 'P0',
                               'Pn', 'Lq', 'L', 'Wq', 'W']
        
        valores_servidores = list(range(s,s + 8))
        valores_Lq = []
        valores_Lq.append(Lq)
        for valor in valores_servidores[1:]:
            p_valor = round((lamda / (valor * mu)), 6)
            valores_Lq.append(round((((pow(lamda, 2)/(k * pow(mu, 2))) + (pow(p_valor, 2))) / (2 * (1 - p_valor))), 6))

        print(valores_servidores)
        print(valores_Lq)
        arreglo_valores_UI.append(valores_servidores)
        arreglo_valores_UI.append(valores_Lq)       
        
        arreglo_tabla = [arreglo_titulo2, arreglo_valores_UI]
        arreglo_prob=[lamda,mu,s,k,tiempo]
        results = tk.Toplevel()
        results.title("Resultados")

        result_title = tk.Label(results, text='Resultados del Modelo M/Ek/s :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)
        self.mg1_iniciacionDeTabla(
            arreglo_tabla, results, tiempo,  7,"modelo_M_Ek_s",arreglo_prob)
        self.mg1_tabla_latex(arreglo_tabla, results, 7)
   
    #-------------------------------------------------------------
    # UI 
    
    def m_m_1_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_m_1_frame"

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)
        
        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        lambda_input.insert(tk.END, '1')
        mu_input.insert(tk.END, '2')
        tiempo_input.insert(tk.END, '3')
        
        sumbit_btn = tk.Button(self.frame, text="Generar", font=(
            "Castellar", 8), command=lambda: self.aux_m_m_1_frame(lambda_input, mu_input, tiempo_input))
        sumbit_btn.grid(column=0, row=5, columnspan=3, pady=20)

    def aux_m_m_1_frame(self, lambda_input, mu_input, tiempo_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())

            except:
                self.errorText.set('Lambda y mu deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_1(x1, x2):
                self.modelo_M_M_1(x1, x2, tiempo_input.get())
            # self.centrosCuadrados(x1,x2)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_m_s_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_m_s_frame"
       

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        server_label = ttk.Label(self.frame,  text='No. de Servidores :', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1, row=4, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_m_s_frame(lambda_input, mu_input, tiempo_input, server_input))

        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_m_s_frame(self, lambda_input, mu_input, tiempo_input, server_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and server_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())
                #x3 = int(server_input.get())

            except:
                self.errorText.set(
                    'Lambda, mu y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            try:
                x3 = int(server_input.get())
            except:
                self.errorText.set('El no. de servidores debe ser Entero')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            
            if self.comprobacion_Modelo_M_M_s(x1, x2, x3):
                self.modelo_M_M_s(x1, x2, tiempo_input.get(), x3)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_m_s_K_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_m_s_K_frame"
       

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        server_label = ttk.Label(self.frame,  text='No. de Servidores :', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1, row=4, padx=10)

        k_label = ttk.Label(self.frame,  text='K :', font=("Castellar", 8)).grid(
            column=0, row=5, padx=10, pady=20, sticky="e")
        k_input = tk.Entry(self.frame, width=20)
        k_input.grid(column=1, row=5, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_m_s_K_frame(lambda_input, mu_input, tiempo_input, k_input, server_input))

        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_m_s_K_frame(self, lambda_input, mu_input, tiempo_input, k_input, server_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and k_input.get() != '' and server_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())

            except:
                self.errorText.set(
                    'Lambda y mu deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            try:
                x3 = int(server_input.get())
                x4 = int(k_input.get())
                
            except:
                self.errorText.set(
                    'El no. de servidores y K deben ser enteros')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_s_K(x1, x2, x3, x4):
                self.modelo_M_M_s_K(x1, x2, tiempo_input.get(), x3, x4)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_G_1_frame(self, *args):

        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_G_1_frame"

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        dst_label = ttk.Label(self.frame,  text='Desvisacion Estandar:', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        dst_input = tk.Entry(self.frame, width=20)
        dst_input.grid(column=1, row=4, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_G_1_frame(lambda_input, mu_input, tiempo_input,dst_input))
        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_G_1_frame(self, lambda_input, mu_input, tiempo_input, dst_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and dst_input.get() != '' :
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())
                x3 = float(dst_input.get())
            except:
                self.errorText.set(
                    'Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_G_1(x1, x2, x3):
                self.modelo_M_G_1(x1, x2, tiempo_input.get(), x3)
                #self.modelo_M_M_1(x1, x2, tiempo_input.get(), x4)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_D_1_frame(self, *args):

        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_D_1_frame"

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=(
            "Castellar", 8), command=lambda: self.aux_m_D_1_frame(lambda_input, mu_input, tiempo_input))
        sumbit_btn.grid(column=0, row=5, columnspan=3, pady=20)

    def aux_m_D_1_frame(self, lambda_input, mu_input, tiempo_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())

            except:
                self.errorText.set('Lambda y mu deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_D_1(x1, x2):
                self.modelo_M_D_1(x1, x2, tiempo_input.get())
            # self.centrosCuadrados(x1,x2)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_erlang_s_frame(self, *args):

        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_Erlang_s_frame"

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        server_label = ttk.Label(self.frame,  text='No. de Servidores :', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1, row=4, padx=10)

        k_label = ttk.Label(self.frame,  text='K :', font=("Castellar", 8)).grid(
            column=0, row=5, padx=10, pady=20, sticky="e")
        k_input = tk.Entry(self.frame, width=20)
        k_input.grid(column=1, row=5, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_erlang_s_frame(lambda_input, mu_input, tiempo_input, k_input, server_input))

        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_erlang_s_frame(self, lambda_input, mu_input, tiempo_input, k_input, server_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and k_input.get() != '' and server_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())

            except:
                self.errorText.set(
                    'Lambda y mu deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            try:
                x3 = int(server_input.get())
                x4 = int(k_input.get())
                
            except:
                self.errorText.set(
                    'El no. de servidores y K deben ser enteros')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_modelo_M_Ek_s(x1,x2,x4,x3):
                self.modelo_M_Ek_s(x1,x2,x3,tiempo_input.get(),x4)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def option_changed(self, *args):
        if self.option.get() == self.menu[0]:
            self.m_m_1_frame()
        elif self.option.get() == self.menu[1]:
            self.m_m_s_frame()
        elif self.option.get() == self.menu[2]:
            self.m_m_s_K_frame()
        elif self.option.get() == self.menu[3]:
            self.m_G_1_frame()
        elif self.option.get() == self.menu[4]:
            self.m_D_1_frame()
        elif self.option.get() == self.menu[5]:
            self.m_erlang_s_frame()



if __name__ == "__main__":
    app = App()
    app.mainloop()

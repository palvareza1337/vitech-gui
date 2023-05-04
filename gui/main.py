#!/usr/bin/env python
# -*- coding: utf-8 -*-
# profiler
import cProfile, pstats
import time
start = time.time()

# normals imports
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import image, style
import pandas as pd
import matplotlib.animation as animation
from functools import partial
from matplotlib.ticker import FormatStrFormatter
from tkinter import PhotoImage, ttk
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
from math import *
import sys, os
from fpdf import FPDF

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Custom Creations
import sesion
import sql_service
import s3_service
import Sidebar
from CustomNotebook import CustomNotebook
from CustomToolbar import CustomToolbar
import maquina



global id_empresa 
id_empresa = 17123456 

# literal un diccionario para convertir XYZ a HORIZONTAL VERTICAL Y AXIAL
mapping_ejes = {'X': 'Horizontal', 'Y': 'Vertical', 'Z': 'Axial'}

# llamada a la carga de variables de entorno desde un archivo .env

# creacion de la ventana principal
root = tk.Tk()
root.wm_title("VITECH")
root.geometry("1000x700")

"""
icon = os.path.join(sys.path[0], "LOGO_VITECH.ico")
root.iconbitmap(icon)

"""



ribbon = ttk.Notebook(root)
ribbon.pack(side=tk.TOP, fill=tk.BOTH)

# creacion de la barra lateral con la informacion de las areas, maquinas, zonas, puntos y mediciones
sidebar = tk.Frame(root, bg="blue")
sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
treeview = ttk.Treeview(sidebar, selectmode="browse", bootstyle='info')
# place the Treeview widget on the root window
treeview.pack(fill=tk.BOTH, expand=1)
    
tab1 = ttk.Frame(ribbon)
ribbon.add(tab1, text='Iniciar')
ttk.Button(tab1, text='Iniciar Sesion', bootstyle=(SUCCESS, OUTLINE)).pack(side=tk.LEFT)

ttk.Button(tab1, text='Nueva Máquina', command=partial(maquina.nueva_maquina, root), bootstyle=(INFO, OUTLINE)).pack(side=tk.LEFT)
ttk.Button(tab1, text='Actualizar Lista', command=partial(Sidebar.populate_sidebar, treeview), bootstyle=(INFO, OUTLINE)).pack(side=tk.LEFT)
ttk.Button(tab1, text='Nuevo Reporte', bootstyle=(INFO, OUTLINE)).pack(side=tk.LEFT)
ttk.Button(tab1, text='Soporte', bootstyle=(INFO, OUTLINE)).pack(side=tk.LEFT)
ttk.Button(tab1, text='Tutoriales', bootstyle=(INFO, OUTLINE)).pack(side=tk.LEFT) 

ttk.Button(tab1, text='Cerrar Sesion', command=partial(sesion.cerrar_sesion, root), bootstyle=(DANGER, OUTLINE)).pack(side=tk.RIGHT)

tab2 = tk.Frame(ribbon)
ribbon.add(tab2, text='BBDD')
tk.Button(tab2, text='Boton 2').pack(side=tk.LEFT)

tab3 = tk.Frame(ribbon)
ribbon.add(tab3, text='Analizar')
tk.Button(tab3, text='Boton 3').pack(side=tk.LEFT)

tab4 = tk.Frame(ribbon)
ribbon.add(tab4, text='Funciones')
tk.Button(tab4, text='Boton 4').pack(side=tk.LEFT)

tab5 = tk.Frame(ribbon)
ribbon.add(tab5, text='Sensor')
tk.Button(tab5, text='Boton 5').pack(side=tk.LEFT)

tab6 = tk.Frame(ribbon)
ribbon.add(tab6, text='Tools')
tk.Button(tab6, text='Boton 6').pack(side=tk.LEFT)



def OnDoubleClick(event):
    filename = treeview.selection()[0]
    query = sql_service.get_pestana(filename)
    sample_rate = query[0]
    name = '/'.join(query[1:]) + '/' + mapping_ejes[filename[0]]
    filename = s3_service.get_reading(filename)
    newtab(filename, name, sample_rate)

def OnDoubleClickhistorico(event):
    filename = table.selection()[0]
    query = sql_service.get_pestana(filename)
    sample_rate = query[0]
    name = '/'.join(query[1:]) + '/' + mapping_ejes[filename[0]]
    filename = s3_service.get_reading(filename)
    newtab(filename, name, sample_rate)

def OnSelect(event):
    item = treeview.selection()
    print(item)


treeview.bind("<Double-1>", OnDoubleClick)

# creacion de tabs
graphs = tk.Frame(root, bg="green")
graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
tabControl = CustomNotebook(graphs)
tabControl.pack(fill=tk.BOTH, expand=1)

mediciones_historicas = tk.Canvas(tabControl)

#table = ttk.Treeview(mediciones_historicas, columns=('#0'), show="headings", bootstyle=INFO)
table = ttk.Treeview(mediciones_historicas, columns=('#0'), show="headings", bootstyle=LIGHT)
table.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)

def change_table(event):
    selected_item = treeview.selection()
    try:
        tipo, id = selected_item[0].split(">:<")
    except:
        return 
    
    for item in table.get_children():
        table.delete(item)
    print(tipo)
    match tipo:
        case "area":
            table['columns'] = ('modelo', 'N° puntos')
            table.heading('modelo', text='modelo')
            table.heading('N° puntos', text='N° puntos')
            results = sql_service.buscar_maquinas_por_area(id)
            for result in results:
                table.insert("", tk.END, values=(result["modelo"], result["cant_puntos_monitoreo"]))

        case "maquina":
            table['columns'] = ('Zona', 'Punto', 'Ejes', 'Fecha')
            table.heading('Zona', text='Zona')
            table.heading('Punto', text='Punto')
            table.heading('Ejes', text='Ejes')
            table.heading('Fecha', text='Fecha')
            results = sql_service.buscar_zona_analisis_por_maquina(id)
            for result in results:
                zona = result["id_zona_analisis"]
                results2 = sql_service.buscar_punto_por_zona(zona)
                for result2 in results2:
                    lectura = sql_service.buscar_lectura_por_punto(result2["id_punto"])
                    if lectura[0]["ruta_canal_2"] != None:
                        count = 3
                    else:
                        count = 1
                    table.insert("", tk.END, values=(result["nombre_zona"], result2["nombre_punto"], count, lectura[0]["date_time"]))

        case "zona":
            table['columns'] = ('Punto', 'Ejes', 'Fecha')
            table.heading('Punto', text='Punto')
            table.heading('Ejes', text='Cantidad de ejes')
            table.heading('Fecha', text='Fecha')
            results = sql_service.buscar_punto_por_zona(id)
            for result in results:
                # siempre se busca la ultima lectura
                lectura = sql_service.buscar_lectura_por_punto(result["id_punto"])[-1]
                if lectura["ruta_canal_2"] != None:
                    count = 3
                else:
                    count = 1
                table.insert("", tk.END, values=(result["nombre_punto"], count, lectura["date_time"]))

        case "punto":
            table['columns'] = ('punto', 'Eje', 'Fecha')# lecturas
            table.heading('punto', text='Punto')
            table.heading('Eje', text='Eje')
            table.heading('Fecha', text='Fecha')
            results = sql_service.buscar_lectura_por_punto(id)
            nombre_punto = sql_service.buscar_punto_por_id(results[0]["id_punto"])["nombre_punto"]
            for result in results:
                table.insert("", tk.END, iid=result["ruta_canal_1"], values=(nombre_punto, 'Horizontal', result["date_time"]))
                table.insert("", tk.END, iid=result["ruta_canal_2"], values=(nombre_punto, 'Vertical', result["date_time"]))
                table.insert("", tk.END, iid=result["ruta_canal_3"], values=(nombre_punto, 'Axial', result["date_time"]))


table.bind("<Double-1>", OnDoubleClickhistorico)
treeview.bind("<<TreeviewSelect>>", change_table)


def listar_mediciones():
    tabControl.add(mediciones_historicas, text='Mediciónes historica') 
    tabControl.select(mediciones_historicas)

ttk.Button(tab1, text='Mediciones Historicas', command=partial(listar_mediciones), bootstyle=(INFO, OUTLINE)).pack(side=tk.LEFT)


def newtab(filename, name, sample_rate):
    try:
        signal = pd.read_csv(filename, decimal=',', sep=';')
    except:
        messagebox.showwarning("Error","El archivo no se a podido encontrar")
        return
    # creacion de una nueva tab 
    tab1 = tk.Canvas(tabControl)
    tabControl.add(tab1, text=name) 
    tabControl.select(tab1)
    # creacion de una figura de matplotlib para poder mostrar un nuevo grafico
    
    fig = Figure()
    # creacion de plot 1 de 2 en la figura
    #style.use('seaborn-v0_8')
    style.use('bmh')
    ax1 = fig.add_subplot(211)
    # cambio de color
    # creacion de plot 2 de 2 en la figura
    ax2 = fig.add_subplot(212)

    # agregar espacio entre subplots
    fig.subplots_adjust(hspace=0.5)

    # conexion de matplotlib a tkinter, junto con la figura
    canvas = FigureCanvasTkAgg(fig, master=tab1)  # CREAR AREA DE DIBUJO DE TKINTER.
    
    # barra de navegacion para confugraciones de matplotlib
    toolbar = CustomToolbar(canvas, tab1, name)# barra de iconos
    toolbar.update()

    canvas.draw()
    

    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
    # abrir el archivo para obtener los datos, en caso de falla, usar un messagebox explicando que no se encontro el archivo
    
    # codigo de pablo
    Fs = int(sample_rate)#int(sample_rate[0]) #Sample Rate o Frecuencia de muestreo
    Tstep = 1/Fs #TimeStep o Intervalo de tiempo
    N = len(signal) #Lengt de La captura de datos (Número de muestras)
    t = np.linspace(0, (N-1)*Tstep, N) #TimeStep de señal
    Fstep = Fs/N # Frequency Interval o Intervalo de Frecuencia (Dimensión en la frecuencia)
    f = np.linspace(0, (N-1)*Fstep, N) #TimeStewp de Frecuencia

    # Plot 
    ax1.plot(t, signal, color="#d2361d")
    
    #FFT
    yf= fft(signal)
    xf= fftfreq(N, Tstep)[:N//2]

    # Plot 2
    ax2.plot(xf, 2/N * np.abs(yf[0:N//2]), color="#294fb8")

    ax1.set_xlabel('s')
    ax1.set_ylabel('G')
    ax2.set_xlabel('Hz')
    ax2.set_ylabel('G')


if __name__ == '__main__':

    Sidebar.populate_sidebar(treeview)
    end = time.time()
    print("Gui loaded in " + str(end-start) + " seconds")
    tk.mainloop()
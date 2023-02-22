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

# profiler
import cProfile, pstats
import time
start = time.time()

# Custom Creations
import sesion
import sql_service
import s3_service
import Sidebar
from CustomNotebook import CustomNotebook
from CustomToolbar import CustomToolbar

global id_empresa 
id_empresa = 17123456 

# literal un diccionario para convertir XYZ a HORIZONTAL VERTICAL Y AXIAL
mapping_ejes = {'X': 'Horizontal', 'Y': 'Vertical', 'Z': 'Axial'}

# llamada a la carga de variables de entorno desde un archivo .env

# creacion de la ventana principal
root = tk.Tk()
root.wm_title("Graficador")
root.geometry("1000x700")
icon = os.path.join(sys.path[0], "LOGO_VITECH.ico")
root.iconbitmap(icon)


ribbon = ttk.Notebook(root)
ribbon.pack(side=tk.TOP, fill=tk.BOTH)

def nueva_maquina():

    # Lógica para recuperar información relacionada


    def guardar_nueva_maquina():
        nombre = entrada_modelo.get()
        descripcion = entrada_descripcion.get("1.0", tk.END)
        # Lógica para guardar la nueva máquina en la base de datos
        id_area = combo_area.get().split(' - ')[0]
        query = sql_service.agregar_maquina(id_area, combo_tipo.get(), entrada_sucursal.get(), entrada_modelo.get(), entrada_puntos.get(), combo_criticidad.get(), entrada_pendiente_deg.get(), entrada_descripcion.get('1.0', tk.END))
        ventana_nueva_maquina.destroy()

    def cancelar():
        ventana_nueva_maquina.destroy()

    ventana_nueva_maquina = tk.Toplevel(root)
    ventana_nueva_maquina.title("Nueva Máquina")
    ventana_nueva_maquina.geometry("500x550")
    ventana_nueva_maquina.resizable(False, False)
    ventana_nueva_maquina.attributes('-topmost', 'true')
    ventana_nueva_maquina.focus_force()

    # Crear frame para la información previa
    frame_info_previa = tk.LabelFrame(ventana_nueva_maquina, text="Información Previa")
    frame_info_previa.pack(padx=10, pady=10)

    def actualizar_areas_cmbx(cmbx: ttk.Combobox, event):
        sucursal_selected = event.widget.get()
        sucursal_selected_id = sucursal_selected.split(" - ")[0]
        query_areas = sql_service.buscar_areas_por_sucursal(sucursal_selected_id)
        opciones_area = [x[0] + " - " + x[2] for x in query_areas]
        cmbx['values'] = opciones_area
    
    etiqueta_sucursal_id = tk.Label(frame_info_previa, text="Sucursal:")
    etiqueta_sucursal_id.grid(row=0, column=0, sticky="w")
    query_sucursales = sql_service.buscar_sucursales_por_empresa(id_empresa)
    opciones_sucursal_id = [x[0] + " - " + x[2] for x in query_sucursales]
    combo_sucursal_id = ttk.Combobox(frame_info_previa, values=opciones_sucursal_id, state="readonly") 
    combo_sucursal_id.grid(row=0, column=1, padx=5, pady=5)

    etiqueta_area = tk.Label(frame_info_previa, text="Área:")
    etiqueta_area.grid(row=1, column=0, sticky="w")
    opciones_area = ["Fija", "Movil"]
    combo_area = ttk.Combobox(frame_info_previa, values=opciones_area, state="readonly") 
    combo_area.grid(row=1, column=1, padx=5, pady=5)
    
    actualizar_areas_cmbx_partial = partial(actualizar_areas_cmbx, combo_area)
    combo_sucursal_id.bind("<<ComboboxSelected>>", actualizar_areas_cmbx_partial)

    # Crear frame para la información básica
    frame_info_basica = tk.LabelFrame(ventana_nueva_maquina, text="Información básica")
    frame_info_basica.pack(padx=10, pady=10)

    etiqueta_tipo = tk.Label(frame_info_basica, text="Tipo:")
    etiqueta_tipo.grid(row=0, column=0, sticky="w")
    opciones_tipo = ["Fija", "Movil"]
    combo_tipo = ttk.Combobox(frame_info_basica, values=opciones_tipo, state="readonly") 
    combo_tipo.grid(row=0, column=1, padx=5, pady=5)

    etiqueta_modelo = tk.Label(frame_info_basica, text="Modelo:")
    etiqueta_modelo.grid(row=1, column=0, sticky="w")
    entrada_modelo = tk.Entry(frame_info_basica)
    entrada_modelo.grid(row=1, column=1, padx=5, pady=5)
    

    # Crear frame para la información avanzada
    frame_info_avanzada = tk.LabelFrame(ventana_nueva_maquina, text="Información avanzada")
    frame_info_avanzada.pack(padx=10, pady=10)

    etiqueta_puntos = tk.Label(frame_info_avanzada, text="Cant. Puntos de monitoreo:")
    etiqueta_puntos.grid(row=0, column=0, sticky="w")
    entrada_puntos = tk.Entry(frame_info_avanzada)
    entrada_puntos.grid(row=0, column=1, padx=5, pady=5)
    

    etiqueta_criticidad = tk.Label(ventana_nueva_maquina, text="Nivel de criticidad:")
    etiqueta_criticidad.pack()

    # Creamos la lista de opciones
    opciones_criticidad = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    # Creamos el widget "Combobox"
    combo_criticidad = ttk.Combobox(ventana_nueva_maquina, values=opciones_criticidad, state="readonly")
    combo_criticidad.pack()

    etiqueta_pendiente_deg = tk.Label(ventana_nueva_maquina, text="Pendiente de degradación:")
    etiqueta_pendiente_deg.pack()
    # Creamos el widget "Entry"
    entrada_pendiente_deg = tk.Entry(ventana_nueva_maquina)
    entrada_pendiente_deg.pack()

    # Función para validar la entrada como un número con máximo 8 dígitos
    def validar_numero(new_value):
        if not new_value:
            return True
    
        try:
            float(new_value)
            if len(new_value) <= 8: # Verifica que el número tenga como máximo 8 dígitos
                return True
            else:
                return False
        except ValueError:
            return False
    
    # Creamos la etiqueta
    etiqueta_sucursal = tk.Label(ventana_nueva_maquina, text="Contacto sucursal:")
    etiqueta_sucursal.pack()

    # Creamos el widget "Entry"
    entrada_sucursal = tk.Entry(ventana_nueva_maquina, validate="key")
    entrada_sucursal.pack()

    # Agregamos la validación para que solo se permitan números con máximo 8 dígitos
    entrada_sucursal.config(validatecommand=(ventana_nueva_maquina.register(validar_numero), "%P"))

    etiqueta_descripcion = tk.Label(ventana_nueva_maquina, text="Descripción:")
    etiqueta_descripcion.pack()

    # Creamos el widget "Text"
    entrada_descripcion = tk.Text(ventana_nueva_maquina, height=5)
    entrada_descripcion.pack()

    botones_frame = tk.Frame(ventana_nueva_maquina)
    botones_frame.pack(pady=10)

    boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
    boton_cancelar.grid(row=0, column=0, padx=5)

    boton_guardar = tk.Button(botones_frame, text="Guardar", command=guardar_nueva_maquina, bg="#3366CC") 
    boton_guardar.grid(row=0, column=1, padx=5)





    
tab1 = tk.Frame(ribbon)
ribbon.add(tab1, text='Iniciar')
tk.Button(tab1, text='Iniciar Sesion').pack(side=tk.LEFT)
tk.Button(tab1, text='Cerrar Sesion', command=partial(sesion.cerrar_sesion, root)).pack(side=tk.LEFT)
#tk.Button(tab1, text='Nueva Máquina').pack(side=tk.LEFT)
tk.Button(tab1, text='Nueva Máquina', command=nueva_maquina).pack(side=tk.LEFT)
tk.Button(tab1, text='Nuevo Reporte').pack(side=tk.LEFT)


tk.Button(tab1, text='Soporte').pack(side=tk.LEFT)
tk.Button(tab1, text='Tutoriales').pack(side=tk.LEFT) 

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

# creacion de la barra lateral con la informacion de las areas, maquinas, zonas, puntos y mediciones
sidebar = tk.Frame(root, bg="blue")
sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
treeview = ttk.Treeview(sidebar)
# place the Treeview widget on the root window
treeview.pack(fill=tk.BOTH, expand=1)

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

def OnSingleClick(event):
    print("clickeaste")

def OnSelect(event):
    item = treeview.selection()
    print(item)


treeview.bind("<Double-1>", OnDoubleClick)
#treeview.bind("<Button-1>", OnSingleClick)
#treeview.bind("<<TreeviewSelect>>", OnSelect)

# creacion de tabs
graphs = tk.Frame(root, bg="green")
graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
tabControl = CustomNotebook(graphs)
tabControl.pack(fill=tk.BOTH, expand=1)

mediciones_historicas = tk.Canvas(tabControl)

table = ttk.Treeview(mediciones_historicas, columns=('#0'), show="headings")
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
                table.insert("", tk.END, values=(result[4], result[5]))

        case "maquina":
            table['columns'] = ('Zona', 'Punto', 'Ejes', 'Fecha')
            table.heading('Zona', text='Zona')
            table.heading('Punto', text='Punto')
            table.heading('Ejes', text='Ejes')
            table.heading('Fecha', text='Fecha')
            results = sql_service.buscar_zona_analisis_por_maquina(id)
            for result in results:
                zona = result[0]
                results2 = sql_service.buscar_sensor_por_zona(zona)
                for result2 in results2:
                    lectura = sql_service.buscar_lectura_por_sensor(result2[0])
                    if lectura[0][-2] != None:
                        count = 3
                    else:
                        count = 1
                    table.insert("", tk.END, values=(result[2], result2[2], count, lectura[0][1]))

        case "zona":
            table['columns'] = ('Punto', 'Ejes', 'Fecha')
            table.heading('Punto', text='Punto')
            table.heading('Ejes', text='Cantidad de ejes')
            table.heading('Fecha', text='Fecha')
            results = sql_service.buscar_sensor_por_zona(id)
            for result in results:
                lectura = sql_service.buscar_lectura_por_sensor(result[0])
                if lectura[2] != None:
                    count = 3
                else:
                    count = 1
                table.insert("", tk.END, values=(result[2], count, lectura[0][1]))

        case "sensor":
            table['columns'] = ('punto', 'Eje', 'Fecha')# lecturas
            table.heading('punto', text='Punto')
            table.heading('Eje', text='Eje')
            table.heading('Fecha', text='Fecha')
            results = sql_service.buscar_lecturas_por_sensor(id)
            zona = sql_service.buscar_nombre_punto_por_id_sensor(results[0][0])[0]
            for result in results:
                table.insert("", tk.END, iid=result[4], values=(zona, 'Horizontal', result[1]))
                table.insert("", tk.END, iid=result[5], values=(zona, 'Vertical', result[1]))
                table.insert("", tk.END, iid=result[6], values=(zona, 'Axial', result[1]))


table.bind("<Double-1>", OnDoubleClickhistorico)
treeview.bind("<<TreeviewSelect>>", change_table)


def listar_mediciones():
    tabControl.add(mediciones_historicas, text='Mediciónes historica') 
    tabControl.select(mediciones_historicas)

tk.Button(tab1, text='Mediciones Historicas', command=partial(listar_mediciones)).pack(side=tk.LEFT)


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



if __name__ == '__main__':

#    pr = cProfile.Profile()
 #   pr.enable()  # start profiling

    Sidebar.populate_sidebar(treeview)
    end = time.time()
    print("Gui loaded in " + str(end-start) + " seconds")
    tk.mainloop()

#    pr.disable()  # end profiling
#    sortby = 'cumulative'
#    ps = pstats.Stats(pr).sort_stats(sortby)
#    ps.print_stats()

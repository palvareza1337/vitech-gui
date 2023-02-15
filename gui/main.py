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
import CustomNotebook
import s3_service
import Sidebar


# llamada a la carga de variables de entorno desde un archivo .env

# creacion de la ventana principal
root = tk.Tk()
root.wm_title("Graficador")
root.geometry("1000x700")
icon = os.path.join(sys.path[0], "LOGO_VITECH.ico")
root.iconbitmap(icon)


ribbon = ttk.Notebook(root)
ribbon.pack(side=tk.TOP, fill=tk.BOTH)


tab1 = tk.Frame(ribbon)
ribbon.add(tab1, text='Iniciar')
tk.Button(tab1, text='Iniciar Sesion').pack(side=tk.LEFT)
tk.Button(tab1, text='Cerrar Sesion', command=partial(sesion.cerrar_sesion, root)).pack(side=tk.LEFT)
tk.Button(tab1, text='Nueva Máquina').pack(side=tk.LEFT)
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
    item = treeview.selection()[0]
    filename, name, sample_rate = item.split("<:>")
    print("you clicked on", item)
    filename = s3_service.get_reading(filename)
    newtab(filename, name, sample_rate)

def OnSingleClick(event):
    print("clickeaste")

def OnSelect(event):
    item = treeview.selection()
    print(item)


treeview.bind("<Double-1>", OnDoubleClick)
#treeview.bind("<Button-1>", OnSingleClick)
treeview.bind("<<TreeviewSelect>>", OnSelect)




# creacion de tabs
graphs = tk.Frame(root, bg="green")
graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
tabControl = CustomNotebook.CustomNotebook(graphs)
tabControl.pack(fill=tk.BOTH, expand=1)

frame_mediciones = tk.Canvas(root, background='green')

def listar_mediciones():
    tabControl.add(frame_mediciones, text='Mediciónes historica') 
    tabControl.select(frame_mediciones)

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

    
class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, parent, var_nombre_tentativo):
        # var_nombre_tentativo -> cambiar nombre a futuro dependiendo del uso 
        self.var_nombre_tentativo = var_nombre_tentativo.replace("/", " - ")
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            ('Save', 'Export to PDF', 'filesave', 'my_icon_callback'),
        )
        NavigationToolbar2Tk.__init__(self, canvas, parent)

    def my_icon_callback(self):
        # Write your custom functionality here
        #print("My custom icon was clicked!")
        
        #self.canvas.figure.axes[1]
        extent = self.canvas.figure.axes[1].get_window_extent().transformed(self.canvas.figure.dpi_scale_trans.inverted())
        #fig.savefig('ax2_figure.png', bbox_inches=extent)
        #
        ## Pad the saved area by 10% in the x-direction and 20% in the y-direction
        self.canvas.figure.savefig('ax2_figure_expanded.png', bbox_inches=extent.expanded(1.1, 1.2))

        # Guardar el gráfico en un archivo png
        self.canvas.figure.savefig("signal.png")
        #fig.savefig("signal.png")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        #fpdf.cell(w, h = 0, txt = '', border = 0, ln = 0, align = '', fill = False, link = '')
        #pdf.cell(40, 10, 'Área 2 - Máquina 4 - Zona 8 - Punto 9.', 0, 20)
        pdf.cell(40, 10, self.var_nombre_tentativo, 0, 20)
        #pdf.cell(40, 10, 'Área 2 - Máquina 4 - Zona 8 - Punto 9.', 0, 1, 'C')
        pdf.image('ax2_figure_expanded.png', x = None, y = None, w = 200, h = 0, type = 'png', link = '')
        pdf.ln(h = '')

        # Cabecera de la tabla
        pdf.cell(40,7,'Unidad',1,0,'C')
        pdf.cell(40,7,'Horizontal',1,0,'C')
        pdf.cell(40,7,'Vertical',1,0,'C')
        pdf.cell(40,7,'Axial',1,0,'C')
        pdf.ln(h = '')

        # Datos de la tabla
        pdf.cell(40,7,'G',1,0,'C')
        pdf.cell(40,7,'0,12',1,0,'C')
        pdf.cell(40,7,'0,09',1,0,'C')
        pdf.cell(40,7,'0,05',1,0,'C')
        pdf.ln(h = '')
        pdf.cell(40,7,'GE',1,0,'C')
        pdf.cell(40,7,'0,07',1,0,'C')
        pdf.cell(40,7,'0,06',1,0,'C')
        pdf.cell(40,7,'0,04',1,0,'C')
        pdf.ln(h = '')
        pdf.cell(40,7,'in',1,0,'C')
        pdf.cell(40,7,'0,09',1,0,'C')
        pdf.cell(40,7,'0,12',1,0,'C')
        pdf.cell(40,7,'0,06',1,0,'C')
        pdf.ln(h = '')
        pdf.cell(40,7,'Fahrenheit',1,0,'C')
        pdf.cell(120,7,'78,40',1,0,'C')

        pdf.output('tuto1.pdf', 'F')
        os.system('tuto1.pdf')





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

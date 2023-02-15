#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
from math import *

##importar el servicio sql
import sql_service
##

# bloque que se encarga de generar la ventana con el grafico
root = tkinter.Tk()
root.wm_title("Graficador")
ta=root.geometry("1000x700")
# los colores del grafico
style.use('fivethirtyeight')
# figura del matplotlib
fig = Figure()
ax1 = fig.add_subplot(111)
# conexion de matplotlib a tkinter, junto con la figura
canvas = FigureCanvasTkAgg(fig, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
canvas.draw()
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
 # barra de navegacion para confugraciones de matplotlib
toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

data = sql_service.ultima_lectura()
filename = data[4]
sample_rate = data[2]

print(filename, "con un sample rate de ", sample_rate)

act_rango=False
ul_ran=""
ran=""

def graficar(i):
    try:
        signal = pd.read_csv(filename)
    except:
        messagebox.showwarning("Error","El archivo no se a podido encontrar")
    Fs = sample_rate#int(sample_rate[0]) #Sample Rate o Frecuencia de muestreo
    Tstep = 1/Fs #TimeStep o Intervalo de tiempo
    N = len(signal) #Lengt de La captura de datos (Número de muestras)}



    t = np.linspace(0, (N-1)*Tstep, N) #TimeStep de señal
    Fstep = Fs/N # Frequency Interval o Intervalo de Frecuencia (Dimensión en la frecuencia)
    f = np.linspace(0, (N-1)*Fstep, N) #TimeStewp de Frecuencia
    # Plot 

    ax1.plot(t, signal)
    ani.event_source.stop()

def animate(i):
    global act_rango
    global ul_ran
    if act_rango==True:
        try:
            lmin = float(ran[0]); lmax = float(ran[1])
            if lmin < lmax:
                x = np.arange(lmin, lmax, .01)#.01
                ul_ran = [lmin, lmax]
            else:
                act_rango = False
        except:
            messagebox.showwarning("Error","Introduzca los valores del rango de x, separado por coma.")
            act_rango=False
            ets.delete(0,len(ets.get()))
    else:
        if ul_ran!="":
            x = np.arange(ul_ran[0],ul_ran[1], .01)#.01
        else:
            x = np.arange(1, 10, .01)#.01
    try:
        solo=eval(graph_data)
        ax1.clear()
        ax1.plot(x,solo)
    except:
        ax1.plot()
    ax1.axhline(0, color="gray")
    ax1.axvline(0, color="gray")
    ani.event_source.stop() #DETIENE ANIMACIÓN
 
def represent():
    global graph_data
    global ran
    global act_rango
    fig.savefig('test.png')

    texto_orig=et.get()
    if ets.get()!="":
        rann=ets.get()
        ran=rann.split(",")
        act_rango=True
    
    ani.event_source.start() #INICIA/REANUDA ANIMACIÓN
    
ani = animation.FuncAnimation(fig, graficar, interval=1000)
 
plt.show()
 
et = tkinter.Entry(master=root,width=60)
et.config(bg="gray87", justify="left")
 
button = tkinter.Button(master=root, text="SET", bg="gray69", command=represent)
button.pack(side=tkinter.BOTTOM)

 
et.pack(side=tkinter.BOTTOM)
ets=tkinter.Entry(master=root,width=20)
ets.config(bg="gray87")
ets.pack(side=tkinter.RIGHT)
 
tkinter.mainloop()
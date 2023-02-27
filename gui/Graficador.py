import tkinter as tk
from tkinter import ttk
import pandas as pd
import s3_service
import sql_service
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style

from scipy.fft import fft, fftfreq


from CustomToolbar import CustomToolbar


class grafico(tk.Canvas):
    
    def __init__(self, tkParent, filename):
        query = sql_service.get_pestana(filename)
        self.sample_rate = query[0]
        self.name = "/".join(query[1:])
        print(self.name)
        filename = s3_service.get_reading(filename)


        try:
            self.signal = pd.read_csv(filename, decimal=',', sep=';')
        except:
            tk.messagebox.showwarning("Error","El archivo no se a podido encontrar")
        tk.Canvas.__init__(self, tkParent)



        self.graficar()
    
    def graficar(self):
        fig = Figure()
        # creacion de plot 1 de 2 en la figura
        #style.use('seaborn-v0_8')
        style.use('bmh')
        ax1 = fig.add_subplot(211)
        # cambio de color
        # creacion de plot 2 de 2 en la figura
        ax2 = fig.add_subplot(212)

        # conexion de matplotlib a tkinter, junto con la figura
        canvas = FigureCanvasTkAgg(fig, master=self)  # CREAR AREA DE DIBUJO DE TKINTER.

        # barra de navegacion para confugraciones de matplotlib
        toolbar = CustomToolbar(canvas, self, self.name)# barra de iconos
        toolbar.update()

        canvas.draw()


        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        # abrir el archivo para obtener los datos, en caso de falla, usar un messagebox explicando que no se encontro el archivo

        # codigo de pablo
        Fs = int(self.sample_rate)#int(sample_rate[0]) #Sample Rate o Frecuencia de muestreo
        Tstep = 1/Fs #TimeStep o Intervalo de tiempo
        N = len(self.signal) #Lengt de La captura de datos (Número de muestras)
        t = np.linspace(0, (N-1)*Tstep, N) #TimeStep de señal
        Fstep = Fs/N # Frequency Interval o Intervalo de Frecuencia (Dimensión en la frecuencia)
        f = np.linspace(0, (N-1)*Fstep, N) #TimeStewp de Frecuencia

        # Plot 
        ax1.plot(t, self.signal, color="#d2361d")



        #FFT
        yf= fft(self.signal)
        xf= fftfreq(N, Tstep)[:N//2]

        # Plot 2
        ax2.plot(xf, 2/N * np.abs(yf[0:N//2]), color="#294fb8")


  
# Creating tkinter window and set dimensions
window = tk.Tk() 
window.title('graficador') 
window.geometry('500x250')

grafico(window, "Y - 18927630213-02-2023 16,55,34.csv").pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

tk.mainloop()

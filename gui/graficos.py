import pandas as pd
import matplotlib.pyplot as ptl
import seaborn as sns
import numpy as np
import sql_service

sns.set()

def graficar(sample_rate, signal):
    Fs = int(sample_rate) #Sample Rate o Frecuencia de muestreo
    Tstep = 1/Fs #TimeStep o Intervalo de tiempo
    N = len(signal) #Lengt de La captura de datos (Número de muestras)

    t = np.linspace(0, (N-1)*Tstep, N) #TimeStep de señal

    Fstep = Fs/N # Frequency Interval o Intervalo de Frecuencia (Dimensión en la frecuencia)
    f = np.linspace(0, (N-1)*Fstep, N) #TimeStewp de Frecuencia
    # Plot 
    fig, ax = ptl.subplots(nrows = 1, ncols = 1)
    ax.plot(t, signal)

    fig1, ax1 = ptl.subplots(nrows = 1, ncols = 1)
    ax1.plot(f, signal)
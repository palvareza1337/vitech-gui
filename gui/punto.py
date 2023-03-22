import tkinter as tk
from functools import partial
import random
import string

import pandas as pd
from pandastable import Table

def configurar_punto(event):

    def cancelar():
        pass

    def buscar_rodamiento():
        # Crear una nueva ventana de tkinter
        ventana_buscar_rodamiento = tk.Toplevel()
        ventana_buscar_rodamiento.title("Buscador de rodamientos")
        ventana_buscar_rodamiento.geometry("600x500")
        ventana_buscar_rodamiento.resizable(False, False)
        ventana_buscar_rodamiento.focus_set()
        global new_dataframe

        def buscar(df):
            global table, new_dataframe
            valor = entrada_busqueda.get()
            new_dataframe = df.loc[df['Nombre'].str.contains(valor, case=False)]
            print(df)
            table = Table(frame_tabla, dataframe=new_dataframe[['Nombre','Sexo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_rodamiento)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_excel('C:\\Users\\Pablo\\Downloads\\titanic.xlsx')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe
            entrada_descripcion.configure(state="normal")
            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
            
            entrada_descripcion.configure(state="disabled")
            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_rodamiento)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Nombre','Sexo']])
        table.editable = False
        table.bind("<Double-Button-1>", cargar_data)
        table.show()

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_descripcion = tk.Frame(ventana_buscar_rodamiento)
        frame_descripcion.pack(side="top")
        global entrada_descripcion
        entrada_descripcion = tk.Text(frame_descripcion, height=5, width=30)
        entrada_descripcion.configure(state="disabled")
        entrada_descripcion.pack()

        # Crear un Frame para los botones y colocarlos en él
        botones_frame = tk.Frame(ventana_buscar_rodamiento)
        botones_frame.pack(side="top", pady=10)

        boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
        boton_cancelar.pack(side=tk.LEFT, padx=5)

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=cancelar, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)


        item = table.selection()[0]
        values = table.item(item, "values")



    def buscar_engranes():
        # Crear una nueva ventana de tkinter
        ventana_buscar_engrane = tk.Toplevel()
        ventana_buscar_engrane.title("Buscador de engranes")
        ventana_buscar_engrane.geometry("600x500")
        ventana_buscar_engrane.resizable(False, False)
        ventana_buscar_engrane.focus_set()
        global new_dataframe

        def buscar(df):
            global table, new_dataframe
            valor = entrada_busqueda.get()
            new_dataframe = df.loc[df['Nombre'].str.contains(valor, case=False)]
            print(df)
            table = Table(frame_tabla, dataframe=new_dataframe[['Nombre','Sexo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_engrane)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_excel('C:\\Users\\Pablo\\Downloads\\titanic.xlsx')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe
            entrada_descripcion.configure(state="normal")
            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
            
            entrada_descripcion.configure(state="disabled")
            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_engrane)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Nombre','Sexo']])
        table.editable = False
        table.bind("<Double-Button-1>", cargar_data)
        table.show()

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_descripcion = tk.Frame(ventana_buscar_engrane)
        frame_descripcion.pack(side="top")
        global entrada_descripcion
        entrada_descripcion = tk.Text(frame_descripcion, height=5, width=30)
        entrada_descripcion.configure(state="disabled")
        entrada_descripcion.pack()

        # Crear un Frame para los botones y colocarlos en él
        botones_frame = tk.Frame(ventana_buscar_engrane)
        botones_frame.pack(side="top", pady=10)

        boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
        boton_cancelar.pack(side=tk.LEFT, padx=5)

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=cancelar, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)


        item = table.selection()[0]
        values = table.item(item, "values")



    def buscar_phantom():
        # Crear una nueva ventana de tkinter
        ventana_buscar_phantom = tk.Toplevel()
        ventana_buscar_phantom.title("Buscador de sensores")
        ventana_buscar_phantom.geometry("600x500")
        ventana_buscar_phantom.resizable(False, False)
        ventana_buscar_phantom.focus_set()
        global new_dataframe

        def buscar(df):
            global table, new_dataframe
            valor = entrada_busqueda.get()
            new_dataframe = df.loc[df['Nombre'].str.contains(valor, case=False)]
            print(df)
            table = Table(frame_tabla, dataframe=new_dataframe[['Nombre','Sexo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_phantom)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_excel('C:\\Users\\Pablo\\Downloads\\titanic.xlsx')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe
            entrada_descripcion.configure(state="normal")
            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
            
            entrada_descripcion.configure(state="disabled")
            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_phantom)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Nombre','Sexo']])
        table.editable = False
        table.bind("<Double-Button-1>", cargar_data)
        table.show()

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_descripcion = tk.Frame(ventana_buscar_phantom)
        frame_descripcion.pack(side="top")
        global entrada_descripcion
        entrada_descripcion = tk.Text(frame_descripcion, height=5, width=30)
        entrada_descripcion.configure(state="disabled")
        entrada_descripcion.pack()

        # Crear un Frame para los botones y colocarlos en él
        botones_frame = tk.Frame(ventana_buscar_phantom)
        botones_frame.pack(side="top", pady=10)

        boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
        boton_cancelar.pack(side=tk.LEFT, padx=5)

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=cancelar, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)


        item = table.selection()[0]
        values = table.item(item, "values")







    # Aquí empieza el código para la nueva ventana de tkinter
    nueva_ventana = tk.Toplevel()
    #nueva_ventana.lift()
    nueva_ventana.title("Configuración de puntos")
    nueva_ventana.geometry("400x400")
    nueva_ventana.resizable(False, False)
    nueva_ventana.focus_set()

    # Crear un nuevo frame
    frame_nombre_punto = tk.Frame(nueva_ventana)
    frame_nombre_punto.pack()
    # Crear un nuevo widget de etiqueta dentro del frame
    etiqueta_nombre_punto = tk.Label(frame_nombre_punto, text="Nombre del punto:")
    etiqueta_nombre_punto.pack(side="left")
    # Crear un nuevo widget de entrada dentro del frame
    entrada_nombre_punto = tk.Entry(frame_nombre_punto)
    entrada_nombre_punto.pack(side="left")

    # Crear un nuevo frame
    frame_rpm = tk.LabelFrame(nueva_ventana, text="RPM")
    frame_rpm.pack()
    # Crear etiqueta para el Spinbox
    etiqueta_min = tk.Label(frame_rpm, text="Min")
    etiqueta_min.grid(row=1, column=0, sticky="w")
    # Crear un nuevo widget de entrada dentro del frame
    spinbox_min = tk.Spinbox(frame_rpm, from_=0, to=10)
    spinbox_min.grid(row=1, column=1, padx=5, pady=5)
    # Crear etiqueta para el Spinbox
    etiqueta_max = tk.Label(frame_rpm, text="Max")
    etiqueta_max.grid(row=1, column=2, sticky="w")
    # Crear un nuevo widget de entrada dentro del frame
    spinbox_max = tk.Spinbox(frame_rpm, from_=0, to=10)
    spinbox_max.grid(row=1, column=3, padx=5, pady=5)

    # Crear un nuevo frame
    frame_rodamiento = tk.LabelFrame(nueva_ventana, text="Rodamiento")
    frame_rodamiento.pack()

    entrada_rodamiento_cargado = tk.Text(frame_rodamiento, height=4, width=20)
    entrada_rodamiento_cargado.grid(row=0, column=0, padx=5)
    entrada_rodamiento_cargado.configure(state="disabled")

    boton_agregar_rodamiento = tk.Button(frame_rodamiento, text="Agregar", command=buscar_rodamiento, bg="#9b9b9b") 
    boton_agregar_rodamiento.grid(row=0, column=1, padx=5)

    boton_borrar_rodamiento = tk.Button(frame_rodamiento, text="Eliminar", command=cancelar, bg="#ff4040") 
    boton_borrar_rodamiento.grid(row=0, column=2, padx=5)

    # Crear un nuevo frame
    frame_caja_engranes = tk.LabelFrame(nueva_ventana, text="Caja de engranes")
    frame_caja_engranes.pack()

    entrada_caja_cargada = tk.Text(frame_caja_engranes, height=4, width=20)
    entrada_caja_cargada.grid(row=0, column=0, padx=5)
    entrada_caja_cargada.configure(state="disabled")

    boton_agregar_caja_engranes = tk.Button(frame_caja_engranes, text="Agregar", command=buscar_engranes, bg="#9b9b9b") 
    boton_agregar_caja_engranes.grid(row=0, column=1, padx=5)

    boton_borrar_caja_engranes = tk.Button(frame_caja_engranes, text="Eliminar", command=cancelar, bg="#ff4040") 
    boton_borrar_caja_engranes.grid(row=0, column=2, padx=5)

    # Crear un nuevo frame
    frame_phantom = tk.LabelFrame(nueva_ventana, text="Phantom")
    frame_phantom.pack()

    entrada_phantom_cargado = tk.Text(frame_phantom, height=4, width=20)
    entrada_phantom_cargado.grid(row=0, column=0, padx=5)
    entrada_phantom_cargado.configure(state="disabled")

    boton_agregar_phantom = tk.Button(frame_phantom, text="Agregar", command=buscar_phantom, bg="#9b9b9b") 
    boton_agregar_phantom.grid(row=0, column=1, padx=5)

    boton_borrar_phantom = tk.Button(frame_phantom, text="Eliminar", command=cancelar, bg="#ff4040") 
    boton_borrar_phantom.grid(row=0, column=2, padx=5)

    # Crear un nuevo frame
    botones_frame = tk.Frame(nueva_ventana)
    botones_frame.pack(pady=10)

    boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
    boton_cancelar.grid(row=0, column=0, padx=5)

    boton_guardar = tk.Button(botones_frame, text="Guardar", command=cancelar, bg="#3366CC") 
    boton_guardar.grid(row=0, column=1, padx=5)

import tkinter as tk
from functools import partial
import random
import string
from tkinter import ttk
import sql_service

import pandas as pd
from pandastable import Table

import random
import string

def configurar_punto(event, id_zona):

    print("id_zona: ", id_zona)

    print(event.widget.selection()[0])

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
            table = Table(frame_tabla, dataframe=new_dataframe[['Marca','Fabricante','Modelo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_rodamiento)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_csv('rodamientos.csv')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe, entrada_rodamiento_cargado
            entrada_descripcion.configure(state="normal")
            entrada_rodamiento_cargado.configure(state="normal")
            entrada_descripcion.delete('1.0',tk.END)
            entrada_rodamiento_cargado.delete('1.0',tk.END)

            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
                entrada_rodamiento_cargado.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])

            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
                entrada_rodamiento_cargado.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])

            entrada_rodamiento_cargado.configure(state="disabled")
            entrada_descripcion.configure(state="disabled")
            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_rodamiento)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Marca','Fabricante','Modelo']])
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

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=ventana_buscar_rodamiento.destroy, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)



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
            table = Table(frame_tabla, dataframe=new_dataframe[['Marca','Fabricante','Modelo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_engrane)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_csv('engranes.csv')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe, entrada_caja_cargada
            entrada_descripcion.configure(state="normal")
            entrada_caja_cargada.configure(state="normal")
            entrada_descripcion.delete('1.0',tk.END)
            entrada_caja_cargada.delete('1.0',tk.END)


            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
                entrada_caja_cargada.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])

            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
                entrada_caja_cargada.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
            
            entrada_descripcion.configure(state="disabled")
            entrada_caja_cargada.configure(state="disabled")

            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_engrane)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Marca','Fabricante','Modelo']])
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

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=ventana_buscar_engrane.destroy, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)


        item = table.selection()[0]
        values = table.item(item, "values")


    def buscar_ejes():
        # Crear una nueva ventana de tkinter
        ventana_buscar_ejes = tk.Toplevel()
        ventana_buscar_ejes.title("Buscador de ejes")
        ventana_buscar_ejes.geometry("600x500")
        ventana_buscar_ejes.resizable(False, False)
        ventana_buscar_ejes.focus_set()
        global new_dataframe

        def buscar(df):
            global table, new_dataframe
            valor = entrada_busqueda.get()
            new_dataframe = df.loc[df['Nombre'].str.contains(valor, case=False)]
            print(df)
            table = Table(frame_tabla, dataframe=new_dataframe[['Marca','Fabricante','Modelo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_ejes)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_csv('ejes.csv')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe, entrada_ejes_cargada
            entrada_descripcion.configure(state="normal")
            entrada_ejes_cargada.configure(state="normal")
            entrada_descripcion.delete('1.0',tk.END)
            entrada_ejes_cargada.delete('1.0',tk.END)

            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
                entrada_ejes_cargada.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
                entrada_ejes_cargada.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
            
            entrada_ejes_cargada.configure(state="disabled")
            entrada_descripcion.configure(state="disabled")
            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_ejes)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Marca','Fabricante','Modelo']])
        table.editable = False
        table.bind("<Double-Button-1>", cargar_data)
        table.show()

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_descripcion = tk.Frame(ventana_buscar_ejes)
        frame_descripcion.pack(side="top")
        global entrada_descripcion
        entrada_descripcion = tk.Text(frame_descripcion, height=5, width=30)
        entrada_descripcion.configure(state="disabled")
        entrada_descripcion.pack()

        # Crear un Frame para los botones y colocarlos en él
        botones_frame = tk.Frame(ventana_buscar_ejes)
        botones_frame.pack(side="top", pady=10)

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=ventana_buscar_ejes.destroy, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)


        item = table.selection()[0]
        values = table.item(item, "values")


    def buscar_rotor():
        # Crear una nueva ventana de tkinter
        ventana_buscar_rotor = tk.Toplevel()
        ventana_buscar_rotor.title("Buscador de rotores")
        ventana_buscar_rotor.geometry("600x500")
        ventana_buscar_rotor.resizable(False, False)
        ventana_buscar_rotor.focus_set()
        global new_dataframe

        def buscar(df):
            global table, new_dataframe
            valor = entrada_busqueda.get()
            new_dataframe = df.loc[df['Nombre'].str.contains(valor, case=False)]
            print(df)
            table = Table(frame_tabla, dataframe=new_dataframe[['Marca','Fabricante','Modelo']])
            table.editable = False
            table.show()
            

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_busqueda = tk.Frame(ventana_buscar_rotor)
        frame_busqueda.pack(side="top", fill=tk.X)

        # Crear una entrada de texto para la búsqueda
        entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        entrada_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Leer el archivo de Excel con Pandas
        df = pd.read_csv('rotores.csv')

        # Crear un botón para iniciar la búsqueda
        busqueda = partial(buscar, df)
        boton_busqueda = tk.Button(frame_busqueda, text="Buscar", command=busqueda)
        boton_busqueda.pack(side=tk.LEFT, padx=5, pady=5)

        # Funcion para mostrar datos de rodamiento
        def cargar_data(event):
            global entrada_descripcion, table, new_dataframe, entrada_rotor_cargada
            entrada_descripcion.configure(state="normal")
            entrada_rotor_cargada.configure(state="normal")
            entrada_descripcion.delete('1.0',tk.END)
            entrada_rotor_cargada.delete('1.0',tk.END)

            try:
                entrada_descripcion.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
                entrada_rotor_cargada.insert(tk.INSERT, new_dataframe.iloc[int(table.getSelectedRow())])
            except:
                entrada_descripcion.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
                entrada_rotor_cargada.insert(tk.INSERT, df.iloc[int(table.getSelectedRow())])
            
            entrada_rotor_cargada.configure(state="disabled")
            entrada_descripcion.configure(state="disabled")
            print(table.getSelectedRow())
            

        # Crear un Frame para la tabla y colocarla en él
        frame_tabla = tk.Frame(ventana_buscar_rotor)
        frame_tabla.pack(side="top")
        global table
        table = Table(frame_tabla, dataframe=df[['Marca','Fabricante','Modelo']])
        table.editable = False
        table.bind("<Double-Button-1>", cargar_data)
        table.show()

        # Crear un Frame para el cuadro de texto y colocarlo en él
        frame_descripcion = tk.Frame(ventana_buscar_rotor)
        frame_descripcion.pack(side="top")
        global entrada_descripcion
        entrada_descripcion = tk.Text(frame_descripcion, height=5, width=30)
        entrada_descripcion.configure(state="disabled")
        entrada_descripcion.pack()

        # Crear un Frame para los botones y colocarlos en él
        botones_frame = tk.Frame(ventana_buscar_rotor)
        botones_frame.pack(side="top", pady=10)

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=ventana_buscar_rotor.destroy, bg="#3366CC") 
        boton_guardar.pack(side=tk.LEFT, padx=5)


        item = table.selection()[0]
        values = table.item(item, "values")



    def guardar_punto():
        #TODO:
        nombre_punto = entrada_nombre_punto.get()
        tipo_sensor = combo_tipo.get()
        codigo_sensor = entrada_phantom.get()
        rpm_min = spinbox_min.get()
        rpm_max = spinbox_max.get()
        axiales = ""
        sql_service.agregar_punto( id_zona, nombre_punto, tipo_sensor, codigo_sensor, rpm_min, rpm_max, axiales)


    # Aquí empieza el código para la nueva ventana de tkinter
    nueva_ventana = tk.Toplevel()
    #nueva_ventana.lift()
    nueva_ventana.title("Configuración de puntos")
    nueva_ventana.geometry("400x550")
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
    spinbox_min = tk.Spinbox(frame_rpm, from_=-1, to=100000)
    spinbox_min.grid(row=1, column=1, padx=5, pady=5)
    # Crear etiqueta para el Spinbox
    etiqueta_max = tk.Label(frame_rpm, text="Max")
    etiqueta_max.grid(row=1, column=2, sticky="w")
    # Crear un nuevo widget de entrada dentro del frame
    spinbox_max = tk.Spinbox(frame_rpm, from_=-1, to=100000)
    spinbox_max.grid(row=1, column=3, padx=5, pady=5)

    # Crear un nuevo frame
    frame_rodamiento = tk.LabelFrame(nueva_ventana, text="Rodamiento")
    frame_rodamiento.pack()
    
    global entrada_rodamiento_cargado
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

    global entrada_caja_cargada
    entrada_caja_cargada = tk.Text(frame_caja_engranes, height=4, width=20)
    entrada_caja_cargada.grid(row=0, column=0, padx=5)
    entrada_caja_cargada.configure(state="disabled")

    boton_agregar_caja_engranes = tk.Button(frame_caja_engranes, text="Agregar", command=buscar_engranes, bg="#9b9b9b") 
    boton_agregar_caja_engranes.grid(row=0, column=1, padx=5)

    boton_borrar_caja_engranes = tk.Button(frame_caja_engranes, text="Eliminar", command=cancelar, bg="#ff4040") 
    boton_borrar_caja_engranes.grid(row=0, column=2, padx=5)

    # ejes
    # Crear un nuevo frame
    frame_caja_ejes = tk.LabelFrame(nueva_ventana, text="Ejes")
    frame_caja_ejes.pack()

    global entrada_ejes_cargada
    entrada_ejes_cargada = tk.Text(frame_caja_ejes, height=4, width=20)
    entrada_ejes_cargada.grid(row=0, column=0, padx=5)
    entrada_ejes_cargada.configure(state="disabled")

    boton_agregar_ejes = tk.Button(frame_caja_ejes, text="Agregar", command=buscar_ejes, bg="#9b9b9b") 
    boton_agregar_ejes.grid(row=0, column=1, padx=5)

    boton_borrar_ejes = tk.Button(frame_caja_ejes, text="Eliminar", command=cancelar, bg="#ff4040") 
    boton_borrar_ejes.grid(row=0, column=2, padx=5)

    # rotores
    # Crear un nuevo frame
    frame_rotor = tk.LabelFrame(nueva_ventana, text="Rotores")
    frame_rotor.pack()

    global entrada_rotor_cargada
    entrada_rotor_cargada = tk.Text(frame_rotor, height=4, width=20)
    entrada_rotor_cargada.grid(row=0, column=0, padx=5)
    entrada_rotor_cargada.configure(state="disabled")

    boton_agregar_rotor = tk.Button(frame_rotor, text="Agregar", command=buscar_rotor, bg="#9b9b9b") 
    boton_agregar_rotor.grid(row=0, column=1, padx=5)

    boton_borrar_rotor = tk.Button(frame_rotor, text="Eliminar", command=cancelar, bg="#ff4040") 
    boton_borrar_rotor.grid(row=0, column=2, padx=5)

    #codigo phantom
    # Crear un nuevo frame
    frame_phantom = tk.LabelFrame(nueva_ventana, text="Phantom")
    frame_phantom.pack()

    etiqueta_phantom = tk.Label(frame_phantom, text="Codigo del sensor:")
    etiqueta_phantom.grid(row=0, column=0, sticky="w")
    entrada_phantom = tk.Entry(frame_phantom)
    entrada_phantom.grid(row=1, column=1, padx=5)

    etiqueta_tipo = tk.Label(frame_phantom, text="Tipo:")
    etiqueta_tipo.grid(row=0, column=2, sticky="w")
    opciones_tipo = ["Alta", "Baja"]
    global combo_tipo
    combo_tipo = ttk.Combobox(frame_phantom, values=opciones_tipo, state="readonly") 
    combo_tipo.grid(row=1, column=2, padx=5, pady=5)

    # Crear un nuevo frame
    botones_frame = tk.Frame(nueva_ventana)
    botones_frame.pack(pady=10)

    def cancelar():
        nueva_ventana.destroy()

    boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
    boton_cancelar.grid(row=0, column=0, padx=5)

    boton_guardar = tk.Button(botones_frame, text="Guardar", command=guardar_punto, bg="#3366CC") 
    boton_guardar.grid(row=0, column=1, padx=5)

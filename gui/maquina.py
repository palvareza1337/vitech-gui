from functools import partial
import sql_service
import tkinter as tk 
from tkinter import ttk
import random
import string



global id_empresa 
id_empresa = 17123456

# creacion de un diccionario con la relacion nombre de entidad y su id
# usando diccionarios podemos ocultar la informacion de id que el usuario no deberia ver
# esta parte no es realmente necesaria, pero hace que sea mas visible el codigo
diccionario_sucursales = dict()
diccionario_areas = dict()
diccionario_maquinas = dict()
diccionario_zonas = dict()

def nueva_maquina(root):

    # Lógica para recuperar información relacionada


    def guardar_nueva_maquina():
        # Lógica para guardar la nueva máquina en la base de datos
        id_sucursal = diccionario_sucursales[combo_sucursal_id.get()]
        try:
            id_area = diccionario_areas[combo_area.get()]
        except:
            # codigo para crear un area en la sucursal en caso de ser necesario
            nombre_area = combo_area.get()
            id_area = sql_service.agregar_area(nombre_area, id_sucursal)
            print(id_area)
            diccionario_areas[nombre_area] = id_area

        try:
            id_maquina = diccionario_maquinas[combo_maquina.get()]
        except:
            tipo_maquina = combo_tipo.get()
            cant_puntos_monitoreo = spinbox_cant_monitoreo.get()
            criticidad = 2 #combo_criticidad.get()
            pendiente_degradacion = 1 #entrada_pendiente_deg.get()
            notas = entrada_descripcion.get('1.0', tk.END)
            modelo = combo_maquina.get()
            print((id_area, tipo_maquina, modelo, cant_puntos_monitoreo, criticidad, pendiente_degradacion, notas))
            query = sql_service.agregar_maquina(id_area, tipo_maquina, modelo, cant_puntos_monitoreo, criticidad, pendiente_degradacion, notas)
            id_maquina = query 
            print(id_maquina)
            diccionario_maquinas[combo_maquina.get()] = id_maquina
        
        try:
            id_zona = diccionario_zonas[combo_zona.get()]
        except:
        #print(id_area, combo_tipo.get(), combo_sucursal_id.get(), combo_maquina.get())#, entrada_puntos.get(), combo_criticidad.get(), entrada_pendiente_deg.get(), entrada_descripcion.get('1.0', tk.END))
            nombre_zona = combo_zona.get()
            estado_salud = "OK" # investar algo aca
            cant_sensores = 4 # falta crear una rutina para ver cuantos sensores tiene cada cosa
            query = sql_service.agregar_zona(nombre_zona, id_maquina, estado_salud, cant_sensores)
            id_zona = query 
            print(id_zona)
            diccionario_zonas[combo_zona.get()] = id_zona
        
        
        ventana_nueva_maquina.destroy()

    def cancelar():
        ventana_nueva_maquina.destroy()

    ventana_nueva_maquina = tk.Toplevel(root)
    ventana_nueva_maquina.title("Configurar Máquina")
    ventana_nueva_maquina.geometry("1000x450")
    ventana_nueva_maquina.resizable(False, False)
    #ventana_nueva_maquina.attributes('-topmost', 'true')
    ventana_nueva_maquina.focus_force()


    # Crear los cuatro frames
    frame1 = tk.Frame(ventana_nueva_maquina)
    
    
    frame2 = tk.Frame(ventana_nueva_maquina)
    # Crear Treeview
    table = ttk.Treeview(frame2, show='headings', selectmode="browse")


    def abrir_ventana_nueva(event):
        item = table.selection()[0]
        values = table.item(item, "values")

        # Aquí empieza el código para la nueva ventana de tkinter
        nueva_ventana = tk.Toplevel()
        #nueva_ventana.lift()
        nueva_ventana.title("Nueva Ventana")
        nueva_ventana.geometry("200x200")
        nueva_ventana.focus_set()

        # Agregar widgets a la nueva ventana de tkinter
        etiqueta = tk.Label(nueva_ventana, text="Esta es una nueva ventana")
        etiqueta.pack()
    
    


    # Definir columnas
    table['columns'] = ("Nombre", "RPM", "Ejes", "Alarmas", "Extras", "Rodamientos", "Agregar")
    #table.column("#0", width=0, stretch=tk.FALSE)


    # Definir etiquetas de cabecera
    table.heading("Nombre", text="Nombre")
    table.heading("RPM", text="RPM")
    table.heading("Ejes", text="Ejes")
    table.heading("Alarmas", text="Alarmas")
    table.heading("Extras", text="Extras")
    table.heading("Rodamientos", text="Rodamientos")
    table.heading("Agregar", text="Agregar")

    table.column("Nombre", width=50)
    table.column("RPM", width=50)
    table.column("Ejes", width=50)
    table.column("Alarmas", width=50)
    table.column("Extras", width=50)
    table.column("Rodamientos", width=50)
    table.column("Agregar", width=50)


    # Agregar datos a la tabla
    table.insert(parent="", index=0, iid=0, values=("LD", "80,180", "H,V,A", "V,AE", "Acelerati..", "", "Agregar"))
    table.insert(parent="", index=1, iid=1, values=("LI", "80,180", "H,V,A", "V,AE", "Acelerati..", "", "Agregar"))

    # Empaquetar la tabla dentro del frame
    table.pack()#expand=1, fill=tk.BOTH)

    table.bind("<Double-1>", abrir_ventana_nueva)


    frame3 = tk.Frame(ventana_nueva_maquina)
    # Crear frame para la información básica
    frame_info_basica = tk.LabelFrame(frame3, text="Información básica")
    frame_info_basica.pack(padx=10, pady=10, anchor="w")

    etiqueta_tipo = tk.Label(frame_info_basica, text="Tipo:")
    etiqueta_tipo.grid(row=0, column=0, sticky="w")
    opciones_tipo = ["Fija", "Movil"]
    combo_tipo = ttk.Combobox(frame_info_basica, values=opciones_tipo, state="readonly") 
    combo_tipo.grid(row=0, column=1, padx=5, pady=5)

    etiqueta_modelo = tk.Label(frame_info_basica, text="Modelo:")
    etiqueta_modelo.grid(row=1, column=0, sticky="w")
    entrada_modelo = tk.Entry(frame_info_basica)
    entrada_modelo.grid(row=1, column=1, padx=5, pady=5)

    # Crear etiqueta para el Spinbox
    etiqueta_spinbox = tk.Label(frame_info_basica, text="Cant. Puntos de monitoreo:")
    etiqueta_spinbox.grid(row=2, column=0, sticky="w")
    spinbox_cant_monitoreo = tk.Spinbox(frame_info_basica, from_=0, to=10)
    spinbox_cant_monitoreo.grid(row=2, column=1, padx=5, pady=5)
    
    #frame4 = tk.Frame(ventana_nueva_maquina, bg='yellow')

    frame5 = tk.Frame(ventana_nueva_maquina)

    frame6 = tk.Frame(ventana_nueva_maquina)

    frame7 = tk.Frame(ventana_nueva_maquina)

    # Posicionar los frames utilizando grid
    frame1.grid(row=0, column=0)
    frame2.grid(row=0, column=1, rowspan=3, sticky="N")
    frame3.grid(row=1, column=0)
    #frame4.grid(row=1, column=1)
    frame5.grid(row=2, column=0)
    frame6.grid(row=2, column=1)
    #frame7.grid(row=3, column=0, columnspan=2)
    frame7.grid(row=3, column=0)


    # Crear frame para la información previa
    frame_info_previa = tk.LabelFrame(frame1, text="Información Previa")
    frame_info_previa.pack(padx=10, pady=10, anchor="w")
    

    def actualizar_areas_cmbx(cmbx: ttk.Combobox, event):
        sucursal_selected = event.widget.get()
        sucursal_selected_id = diccionario_sucursales[sucursal_selected]
        query_areas = sql_service.buscar_areas_por_sucursal(sucursal_selected_id)
        global diccionario_areas
        diccionario_areas = {area[2]: area[0] for area in query_areas}
        opciones_area = list(diccionario_areas.keys())
        cmbx['values'] = opciones_area

    etiqueta_sucursal_id = tk.Label(frame_info_previa, text="Sucursal:")
    etiqueta_sucursal_id.grid(row=0, column=1, sticky="w")
    query_sucursales = sql_service.buscar_sucursales_por_empresa(id_empresa)
    diccionario_sucursales = {sucursal[2]: sucursal[0] for sucursal in query_sucursales}
    print(list(diccionario_sucursales.keys()))
    opciones_sucursal_id = list(diccionario_sucursales.keys())
    combo_sucursal_id = ttk.Combobox(frame_info_previa, values=opciones_sucursal_id, state="readonly") 
    combo_sucursal_id.grid(row=0, column=2, padx=5, pady=5)


    def actualizar_maquinas_cmbx(cmbx: ttk.Combobox, event):
        area_selected = event.widget.get()
        area_selected_id = diccionario_areas[area_selected]
        query_maquinas = sql_service.buscar_maquinas_por_area(area_selected_id)
        global diccionario_maquinas
        diccionario_maquinas = {maquina[3]: maquina[0] for maquina in query_maquinas}
        opciones_maquina = list(diccionario_maquinas.keys())
        cmbx['values'] = opciones_maquina
    
    etiqueta_area = tk.Label(frame_info_previa, text="Área:")
    etiqueta_area.grid(row=1, column=1, sticky="w")
    opciones_area = []
    combo_area = ttk.Combobox(frame_info_previa, values=opciones_area, state="normal") 
    combo_area.grid(row=1, column=2, padx=5, pady=5)
    
    

    def actualizar_zonas_cmbx(cmbx: ttk.Combobox, event):
        maquina_selected = event.widget.get()
        maquina_selected_id = diccionario_maquinas[maquina_selected]
        query_zonas = sql_service.buscar_zona_analisis_por_maquina(maquina_selected_id)
        global diccionario_zonas
        print(query_zonas)
        diccionario_zonas = {zona[2]: zona[0] for zona in query_zonas}
        opciones_zonas = list(diccionario_zonas.keys())
        cmbx['values'] = opciones_zonas

    etiqueta_maquina = tk.Label(frame_info_previa, text="Máquina:")
    etiqueta_maquina.grid(row=2, column=1, sticky="w")
    opciones_maquina = ["Fija", "Movil"]
    combo_maquina = ttk.Combobox(frame_info_previa, values=opciones_maquina, state="normal") 
    combo_maquina.grid(row=2, column=2, padx=5, pady=5)
    

    etiqueta_zona = tk.Label(frame_info_previa, text="Zona:")
    etiqueta_zona.grid(row=3, column=1, sticky="w")
    opciones_zona = []
    combo_zona = ttk.Combobox(frame_info_previa, values=opciones_zona, state="normal") 
    combo_zona.grid(row=3, column=2, padx=5, pady=5)
    

    actualizar_areas_cmbx_partial = partial(actualizar_areas_cmbx, combo_area)
    combo_sucursal_id.bind("<<ComboboxSelected>>", actualizar_areas_cmbx_partial)

    actualizar_maquinas_cmbx_partial = partial(actualizar_maquinas_cmbx, combo_maquina)
    combo_area.bind("<<ComboboxSelected>>", actualizar_maquinas_cmbx_partial)

    actualizar_zonas_cmbx_partial = partial(actualizar_zonas_cmbx, combo_zona)
    combo_maquina.bind("<<ComboboxSelected>>", actualizar_zonas_cmbx_partial)

    etiqueta_descripcion = tk.Label(frame5, text="Descripción:")
    etiqueta_descripcion.pack()

    # Creamos el widget "Text"
    entrada_descripcion = tk.Text(frame5, height=4, width=50)
    entrada_descripcion.pack()

    botones_frame = tk.Frame(frame7)
    botones_frame.pack(pady=10)

    boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
    boton_cancelar.grid(row=0, column=0, padx=5)

    boton_guardar = tk.Button(botones_frame, text="Guardar", command=guardar_nueva_maquina, bg="#3366CC") 
    boton_guardar.grid(row=0, column=1, padx=5)
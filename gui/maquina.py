from functools import partial
import sql_service
import tkinter as tk 
from tkinter import ttk

import punto


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
        # verificar la existencia del area donde ingresar la maquina
        try:
            id_area = diccionario_areas[combo_area.get()]
        except:
            # codigo para crear un area en la sucursal en caso de ser necesario
            nombre_area = combo_area.get()
            id_area = sql_service.agregar_area(nombre_area, id_sucursal)
            print(id_area)
            diccionario_areas[nombre_area] = id_area

        # seleccion o creacion de nueva maquina con los valores entregados
        try:
            id_maquina = diccionario_maquinas[combo_maquina.get()]
        except:
            tipo_maquina = combo_tipo.get()
            cant_puntos_monitoreo = spinbox_cant_monitoreo.get()
            criticidad = 2 #combo_criticidad.get()
            pendiente_degradacion = 1 #entrada_pendiente_deg.get()
            nombre = combo_maquina.get()
            modelo = entrada_modelo.get()
            query = sql_service.agregar_maquina(id_area, tipo_maquina, modelo, cant_puntos_monitoreo, criticidad, nombre)
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
        
        
        #ventana_nueva_maquina.destroy()

    def cancelar():
        ventana_nueva_maquina.destroy()

    ventana_nueva_maquina = tk.Toplevel(root)
    ventana_nueva_maquina.title("Configurar Máquina")
    ventana_nueva_maquina.geometry("700x350")
    ventana_nueva_maquina.resizable(False, False)
    #ventana_nueva_maquina.attributes('-topmost', 'true')
    ventana_nueva_maquina.focus_force()


    # Crear los cuatro frames
    frame1 = tk.Frame(ventana_nueva_maquina)
    
    
    frame2 = tk.Frame(ventana_nueva_maquina)
    # Crear Treeview
    table = ttk.Treeview(frame2, show='headings', selectmode="browse")

    

    



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

    def clear_table():
        for child in table.get_children():
            table.delete(child)

    def add_to_table_from_db(id_punto, nombre, rpm_min, rpm_max, axiales, alarmas, extras, rodamiento):
        rpmString = str(rpm_min) + ', ' + str(rpm_max)
        table.insert(parent="", index=int(id_punto), iid=id_punto, values=(nombre, rpmString, axiales, "V,AE", "Acelerati..", "", "Agregar"))


    def add_to_table(event):
        print("aiuda")
        print(table.get_children())
        if(len(table.get_children()) > 9):
            return
        try:
            new_index = max(list(map(int, table.get_children()))) + 1
        except:
            new_index = 0
        table.insert(parent="", index=new_index, iid=new_index, values=("LD", "80,180", "H,V,A", "V,AE", "Acelerati..", "", "Agregar"))
    
    def del_from_table(event):
        print("porfa")
        print(table.get_children())
        print(table.selection_get())
        if(len(table.get_children()) < 2):
            return
        try:
            del_index = table.selection_get()
            table.delete(del_index)
        except:
            del_index = max(table.get_children())
            table.delete(del_index)

    # Empaquetar la tabla dentro del frame
    table.pack()#expand=1, fill=tk.BOTH)

    def configurar_punto(event):
        guardar_nueva_maquina()
        id_zona = diccionario_zonas[combo_zona.get()]
        punto.configurar_punto(event, id_zona)

    table.bind("<Double-1>", configurar_punto)


    frame3 = tk.Frame(ventana_nueva_maquina)
    # Crear frame para la información básica
    frame_info_basica = tk.LabelFrame(frame3, text="Información básica")
    frame_info_basica.pack(padx=10, pady=10, anchor="w")

    etiqueta_tipo = tk.Label(frame_info_basica, text="Tipo:")
    etiqueta_tipo.grid(row=0, column=0, sticky="w")
    opciones_tipo = ["Fija", "Movil"]
    global combo_tipo
    combo_tipo = ttk.Combobox(frame_info_basica, values=opciones_tipo, state="readonly") 
    combo_tipo.grid(row=0, column=1, padx=5, pady=5)
    etiqueta_modelo = tk.Label(frame_info_basica, text="Modelo:")
    etiqueta_modelo.grid(row=1, column=0, sticky="w")
    global entrada_modelo
    entrada_modelo = tk.Entry(frame_info_basica)
    entrada_modelo.grid(row=1, column=1, padx=5, pady=5)

    # Crear etiqueta para el Spinbox
    etiqueta_spinbox = tk.Label(frame_info_basica, text="Cant. Puntos de monitoreo:")
    etiqueta_spinbox.grid(row=2, column=0, sticky="w")
    spinbox_cant_monitoreo = ttk.Spinbox(frame_info_basica, from_=1, to=10)
    spinbox_cant_monitoreo.grid(row=2, column=1, padx=5, pady=5)
    print("ta bueno el bind")
    spinbox_cant_monitoreo.bind("<<Increment>>", add_to_table)
    spinbox_cant_monitoreo.bind("<<Decrement>>", del_from_table)
    
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
        diccionario_areas = {area["nombre_area"]: area["id_area"] for area in query_areas}
        opciones_area = list(diccionario_areas.keys())
        cmbx['values'] = opciones_area

    etiqueta_sucursal_id = tk.Label(frame_info_previa, text="Sucursal:")
    etiqueta_sucursal_id.grid(row=0, column=1, sticky="w")
    query_sucursales = sql_service.buscar_sucursales_por_empresa(id_empresa)
    diccionario_sucursales = {sucursal["nombre_sucursal"]: sucursal["id_sucursal"] for sucursal in query_sucursales}
    print(list(diccionario_sucursales.keys()))
    opciones_sucursal_id = list(diccionario_sucursales.keys())
    combo_sucursal_id = ttk.Combobox(frame_info_previa, values=opciones_sucursal_id, state="readonly") 
    combo_sucursal_id.grid(row=0, column=2, padx=5, pady=5)


    def actualizar_maquinas_cmbx(cmbx: ttk.Combobox, event):
        area_selected = event.widget.get()
        area_selected_id = diccionario_areas[area_selected]
        query_maquinas = sql_service.buscar_maquinas_por_area(area_selected_id)
        global diccionario_maquinas
        diccionario_maquinas = {maquina["nombre_maquina"]: maquina["id_maquina"] for maquina in query_maquinas}
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
        query_maquina = sql_service.buscar_maquina_por_id(maquina_selected_id)
        global diccionario_zonas, combo_tipo, entrada_modelo
        combo_tipo.set(query_maquina["tipo_maquina"])
        entrada_modelo.delete('0',tk.END)
        entrada_modelo.insert('0', query_maquina["modelo"])
        print(query_zonas)
        diccionario_zonas = {zona["nombre_zona"]: zona["id_zona_analisis"] for zona in query_zonas}

        opciones_zonas = list(diccionario_zonas.keys())
        cmbx['values'] = opciones_zonas
    
    def actualizar_puntos_cmbx(cmbx: ttk.Combobox, event):
        clear_table()
        zona_selected = event.widget.get()
        zona_selected_id = diccionario_zonas[zona_selected]
        query_zonas = sql_service.buscar_zona_analisis_por_id(zona_selected_id)
        spinbox_cant_monitoreo.set(query_zonas["cant_sensores"])
        query_puntos = sql_service.buscar_punto_por_zona(zona_selected_id)
        spinbox_cant_monitoreo.set(len(query_puntos))
        for punto in query_puntos:
            add_to_table_from_db(punto["id_punto"], punto["nombre_punto"], punto["rpm_min"],
                                 punto["rpm_max"], punto["axiales"], "", "", "")

        

    etiqueta_maquina = tk.Label(frame_info_previa, text="Máquina:")
    etiqueta_maquina.grid(row=2, column=1, sticky="w")
    opciones_maquina = []#["Fija", "Movil"]
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

    actualizar_puntos_cmbx_partial = partial(actualizar_puntos_cmbx, combo_zona)
    combo_zona.bind("<<ComboboxSelected>>", actualizar_puntos_cmbx_partial)


    botones_frame = tk.Frame(frame7)
    botones_frame.pack(pady=10)

    boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
    boton_cancelar.grid(row=0, column=0, padx=5)

    
    def boton_guardar_func(event):
        guardar_nueva_maquina()
        ventana_nueva_maquina.destroy()

    boton_guardar = tk.Button(botones_frame, text="Guardar", command=boton_guardar_func, bg="#3366CC") 
    boton_guardar.grid(row=0, column=1, padx=5)
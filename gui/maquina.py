from functools import partial
import sql_service
import tkinter as tk 
from tkinter import ttk


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
        nombre = entrada_modelo.get()
        descripcion = entrada_descripcion.get("1.0", tk.END)
        # Lógica para guardar la nueva máquina en la base de datos
        id_area = diccionario_areas[combo_area.get()]
        tipo_maquina = combo_tipo.get()
        contacto_sucursal = ""
        try:
            modelo = diccionario_maquinas[combo_maquina.get()]
        except:
            modelo = combo_maquina.get()
        cant_puntos_monitoreo = 2
        criticidad = 2
        pendiente_degradacion = 2
        notas = entrada_descripcion.get('1.0', tk.END)
        
        print((id_area, tipo_maquina, contacto_sucursal, modelo, cant_puntos_monitoreo, criticidad, pendiente_degradacion, notas))
        #print(id_area, combo_tipo.get(), combo_sucursal_id.get(), combo_maquina.get())#, entrada_puntos.get(), combo_criticidad.get(), entrada_pendiente_deg.get(), entrada_descripcion.get('1.0', tk.END))
        #query = sql_service.agregar_maquina(id_area, combo_tipo.get(), entrada_sucursal.get(), entrada_modelo.get(), entrada_puntos.get(), combo_criticidad.get(), entrada_pendiente_deg.get(), entrada_descripcion.get('1.0', tk.END))
        
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
        #sucursal_selected_id = sucursal_selected.split(" - ")[0]
        sucursal_selected_id = diccionario_sucursales[sucursal_selected]
        query_areas = sql_service.buscar_areas_por_sucursal(sucursal_selected_id)
        global diccionario_areas
        diccionario_areas = {area[2]: area[0] for area in query_areas}
        #opciones_area = [x[0] + " - " + x[2] for x in query_areas]
        opciones_area = list(diccionario_areas.keys())
        cmbx['values'] = opciones_area

    etiqueta_sucursal_id = tk.Label(frame_info_previa, text="Sucursal:")
    etiqueta_sucursal_id.grid(row=0, column=1, sticky="w")
    query_sucursales = sql_service.buscar_sucursales_por_empresa(id_empresa)
    diccionario_sucursales = {sucursal[2]: sucursal[0] for sucursal in query_sucursales}
    print(list(diccionario_sucursales.keys()))
    #opciones_sucursal_id = [x[0] + " - " + x[2] for x in query_sucursales]
    opciones_sucursal_id = list(diccionario_sucursales.keys())
    combo_sucursal_id = ttk.Combobox(frame_info_previa, values=opciones_sucursal_id, state="readonly") 
    combo_sucursal_id.grid(row=0, column=2, padx=5, pady=5)


    # Agregar botón a la izquierda de etiqueta_area
    #boton_area = tk.Button(frame_info_previa, text="+")
    #boton_area.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def actualizar_maquinas_cmbx(cmbx: ttk.Combobox, event):
        area_selected = event.widget.get()
        #sucursal_selected_id = sucursal_selected.split(" - ")[0]
        area_selected_id = diccionario_areas[area_selected]
        query_maquinas = sql_service.buscar_maquinas_por_area(area_selected_id)
        global diccionario_maquinas
        diccionario_maquinas = {maquina[4]: maquina[0] for maquina in query_maquinas}
        #opciones_area = [x[0] + " - " + x[2] for x in query_areas]
        opciones_maquina = list(diccionario_maquinas.keys())
        cmbx['values'] = opciones_maquina
    
    etiqueta_area = tk.Label(frame_info_previa, text="Área:")
    etiqueta_area.grid(row=1, column=1, sticky="w")
    opciones_area = []
    combo_area = ttk.Combobox(frame_info_previa, values=opciones_area, state="normal") 
    combo_area.grid(row=1, column=2, padx=5, pady=5)
    
    # Función para manejar el evento de hacer clic en el botón de Área
    def manejar_clic_boton_area():
        ventana_nueva_area = tk.Toplevel(root)
        ventana_nueva_area.title("Nueva Área")
        ventana_nueva_area.geometry("400x350")
        ventana_nueva_area.resizable(False, False)
        ventana_nueva_area.attributes('-topmost', 'true')
        ventana_nueva_area.focus_force()

        # Crear frame para la información básica
        frame_info_basica = tk.LabelFrame(ventana_nueva_area, text="Información básica")
        frame_info_basica.pack(padx=10, pady=10)

        etiqueta_area = tk.Label(frame_info_basica, text="Área:")
        etiqueta_area.grid(row=0, column=0, sticky="w")
        entrada_area = tk.Entry(frame_info_basica)
        entrada_area.grid(row=0, column=1, padx=5, pady=5)

        etiqueta_maquina = tk.Label(frame_info_basica, text="Máquina:")
        etiqueta_maquina.grid(row=1, column=0, sticky="w")
        entrada_maquina = tk.Entry(frame_info_basica)
        entrada_maquina.grid(row=1, column=1, padx=5, pady=5)

        etiqueta_zona = tk.Label(frame_info_basica, text="Zona:")
        etiqueta_zona.grid(row=2, column=0, sticky="w")
        entrada_zona = tk.Entry(frame_info_basica)
        entrada_zona.grid(row=2, column=1, padx=5, pady=5)

        # Crear etiqueta para el Spinbox
        etiqueta_spinbox = tk.Label(ventana_nueva_area, text="Puntos de análisis:")
        etiqueta_spinbox.pack(padx=10, pady=10)

        spinbox = tk.Spinbox(ventana_nueva_area, from_=1, to=20)
        spinbox.pack()

        def cancelar():
            ventana_nueva_area.destroy()

        botones_frame = tk.Frame(ventana_nueva_area)
        botones_frame.pack(pady=50)

        boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
        boton_cancelar.grid(row=0, column=0, padx=5)

        boton_guardar = tk.Button(botones_frame, text="Guardar", command=cancelar, bg="#3366CC") 
        boton_guardar.grid(row=0, column=1, padx=5)
    

    #boton_area.config(command=manejar_clic_boton_area)


    # Agregar botón a la izquierda de etiqueta_maquina
    #boton_maquina = tk.Button(frame_info_previa, text="+")
    #boton_maquina.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    def actualizar_zonas_cmbx(cmbx: ttk.Combobox, event):
        maquina_selected = event.widget.get()
        #sucursal_selected_id = sucursal_selected.split(" - ")[0]
        maquina_selected_id = diccionario_maquinas[maquina_selected]
        query_zonas = sql_service.buscar_zona_analisis_por_maquina(maquina_selected_id)
        global diccionario_zonas
        print(query_zonas)
        diccionario_zonas = {zona[2]: zona[0] for zona in query_zonas}
        #opciones_area = [x[0] + " - " + x[2] for x in query_areas]
        opciones_zonas = list(diccionario_zonas.keys())
        cmbx['values'] = opciones_zonas

    etiqueta_maquina = tk.Label(frame_info_previa, text="Máquina:")
    etiqueta_maquina.grid(row=2, column=1, sticky="w")
    opciones_maquina = ["Fija", "Movil"]
    combo_maquina = ttk.Combobox(frame_info_previa, values=opciones_maquina, state="normal") 
    combo_maquina.grid(row=2, column=2, padx=5, pady=5)
    
    # Función para manejar el evento de hacer clic en el botón de máquina
    def manejar_clic_boton_maquina():
        ventana_maquina = tk.Toplevel(root)
        ventana_maquina.title("Nueva Máquina")
        ventana_maquina.geometry("400x400")
        ventana_maquina.resizable(False, False)
        ventana_maquina.attributes('-topmost', 'true')
        ventana_maquina.focus_force()

    #boton_maquina.config(command=manejar_clic_boton_maquina)


# Agregar botón a la izquierda de etiqueta_zona
    #boton_zona = tk.Button(frame_info_previa, text="+")
    #boton_zona.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    etiqueta_zona = tk.Label(frame_info_previa, text="Zona:")
    etiqueta_zona.grid(row=3, column=1, sticky="w")
    opciones_zona = []
    combo_zona = ttk.Combobox(frame_info_previa, values=opciones_zona, state="normal") 
    combo_zona.grid(row=3, column=2, padx=5, pady=5)
    
    # Función para manejar el evento de hacer clic en el botón de zona
    def manejar_clic_boton_zona():
        ventana_zona = tk.Toplevel(root)
        ventana_zona.title("Nueva Zona")
        ventana_zona.geometry("400x400")
        ventana_zona.resizable(False, False)
        ventana_zona.attributes('-topmost', 'true')
        ventana_zona.focus_force()

    #boton_zona.config(command=manejar_clic_boton_zona)

    actualizar_areas_cmbx_partial = partial(actualizar_areas_cmbx, combo_area)
    combo_sucursal_id.bind("<<ComboboxSelected>>", actualizar_areas_cmbx_partial)

    actualizar_maquinas_cmbx_partial = partial(actualizar_maquinas_cmbx, combo_maquina)
    combo_area.bind("<<ComboboxSelected>>", actualizar_maquinas_cmbx_partial)

    actualizar_zonas_cmbx_partial = partial(actualizar_zonas_cmbx, combo_zona)
    combo_maquina.bind("<<ComboboxSelected>>", actualizar_zonas_cmbx_partial)



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

    
    """
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
    """

    etiqueta_descripcion = tk.Label(ventana_nueva_maquina, text="Descripción:")
    etiqueta_descripcion.pack()

    # Creamos el widget "Text"
    entrada_descripcion = tk.Text(ventana_nueva_maquina, height=4)
    entrada_descripcion.pack()

    botones_frame = tk.Frame(ventana_nueva_maquina)
    botones_frame.pack(pady=10)

    boton_cancelar = tk.Button(botones_frame, text="Cancelar", command=cancelar, bg="#9b9b9b") 
    boton_cancelar.grid(row=0, column=0, padx=5)

    boton_guardar = tk.Button(botones_frame, text="Guardar", command=guardar_nueva_maquina, bg="#3366CC") 
    #boton_guardar = tk.Button(botones_frame, text="Guardar", command=cancelar, bg="#3366CC")
    boton_guardar.grid(row=0, column=1, padx=5)
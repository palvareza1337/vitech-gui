import sql_service
import tkinter as tk
from tkinter import ttk

"""
Este código es un conjunto de funciones que se utilizan para poblar un widget Treeview de tkinter que se utiliza como barra lateral en la aplicación.

"""


def populate_lectura(id_punto, tree: ttk.Treeview): # tabname_stack es una lista que se utiliza para crear las rutas de los elementos en el Treeview
    tipo, id_punto_db = id_punto.split('>:<')
    lecturas = sql_service.buscar_lectura_por_sensor(id_punto_db)
    # [('189276403', datetime.datetime(2023, 1, 18, 18, 15, 48), 25980, 0.0, 'C:\\Ruta\\X - 1892764031-18-2023 6,15,48 PM.csv', 
    # 'C:\\Ruta\\Y - 1892764031-18-2023 6,15,48 PM.csv', 'C:\\Ruta\\Z - 1892764031-18-2023 6,15,48 PM.csv')]
    try:
        tree.insert(id_punto, tk.END, text="Horizontal", iid=lecturas[-1]["ruta_canal_1"], open=False)
        if (lecturas[-1]["ruta_canal_2"] != None):
            tree.insert(id_punto, tk.END, text="Vertical", iid=lecturas[-1]["ruta_canal_2"], open=False)
            tree.insert(id_punto, tk.END, text="Axial", iid=lecturas[-1]["ruta_canal_3"], open=False)
    except:
        return



"""
Las siguientes funciones se utilizan para buscar los elementos y sus relaciones con los elementos superiores, 
y luego llamar a populate_lectura para agregar las lecturas del sensor al Treeview.

"""



def populate_punto(id_zona, tree: ttk.Treeview):
    tipo, id_zona_db = id_zona.split('>:<')
    puntos = sql_service.buscar_punto_por_zona(id_zona_db)
    # [('189276403', 'qwerty21', 'Rodamiento 1', 'B', '100%')]
    for punto in puntos:
        treeParent = tree.insert(id_zona, tk.END, text=punto["nombre_punto"], iid='sensor>:<' + punto["id_punto"], open=False)
        populate_lectura(treeParent, tree)


def populate_zonas(id_maquina, tree: ttk.Treeview):
    tipo, id_maquina_db = id_maquina.split('>:<')
    zonas = sql_service.buscar_zona_analisis_por_maquina(id_maquina_db)
    # [('qwerty21', 'j879w1', 'sistema de transmision', '', 1)]
    for zona in zonas:
        treeParent = tree.insert(id_maquina, tk.END, text=zona["nombre_zona"], iid='zona>:<' + str(zona["id_zona_analisis"]), open=False)
        populate_punto(treeParent, tree)


def populate_maquina(id_area, tree: ttk.Treeview):
    tipo, id_area_db = id_area.split('>:<')
    maquinas = sql_service.buscar_maquinas_por_area(id_area_db)
    # [('j879w1', 'e435y7', 'movil', 12345678, 'liebher', 1, 10, 4, '')]
    for maquina in maquinas:
        treeParent = tree.insert(id_area, tk.END, text=maquina["nombre_maquina"], iid='maquina>:<' + str(maquina["id_maquina"]), open=False)
        populate_zonas(treeParent, tree)


def populate_area(id_sucursal, tree: ttk.Treeview):
    areas = sql_service.buscar_areas_por_sucursal(id_sucursal)
    # [('e435y7', '85296374', 'Apilado', 1)]
    for area in areas:
        treeParent = tree.insert(id_sucursal, tk.END, text=area["nombre_area"], iid='area>:<' + str(area["id_area"]), open=False)
        populate_maquina(treeParent, tree)
 
 
def populate_sidebar(tree: ttk.Treeview): 
    tree.delete(*tree.get_children())
    # buscar la empresa y luego busca sus sucursales, áreas, máquinas, zonas y sensores para insertarlos en el Treeview
    empresa = sql_service.buscar_empresa()
    #('17123456', 'lunartech', 'usarmy', 12345678)
    sucursales = sql_service.buscar_sucursales_por_empresa(empresa["id_empresa"])
    #[('85296374', '17123456', 'Valparaíso Centro', 'Av. Brazil 2241', 12345678)]

    tree.heading('#0', text=empresa[1])
    for sucursal in sucursales:
        treeParent = tree.insert('', tk.END, text=sucursal["nombre_sucursal"], iid=sucursal["id_sucursal"], open=False)
        populate_area(treeParent, tree)
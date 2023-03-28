from tkinter import ttk, tk
import sql_service, s3_service

mapping_ejes = {'X': 'Horizontal', 'Y': 'Vertical', 'Z': 'Axial'}

class mediciones_historicas:

    def __init__(self, *args, **kwargs):
        
        self.table = ttk.Treeview.__init__(self, *args, **kwargs)
        self._active = None
        self.table.bind("<Double-1>", self.OnDoubleClickhistorico)


    def change_table(self, event):
        
        selected_item = event.widget.selection()
        try:
            tipo, id = selected_item[0].split(">:<")
        except:
            return 
        
        for item in self.table.get_children():
            self.table.delete(item)
        print(tipo)
        match tipo:
            case "area":
                self.table['columns'] = ('modelo', 'N° puntos')
                self.table.heading('modelo', text='modelo')
                self.table.heading('N° puntos', text='N° puntos')
                results = sql_service.buscar_maquinas_por_area(id)
                for result in results:
                    self.table.insert("", tk.END, values=(result["modelo"], result["cant_puntos_monitoreo"]))

            case "maquina":
                self.table['columns'] = ('Zona', 'Punto', 'Ejes', 'Fecha')
                self.table.heading('Zona', text='Zona')
                self.table.heading('Punto', text='Punto')
                self.table.heading('Ejes', text='Ejes')
                self.table.heading('Fecha', text='Fecha')
                results = sql_service.buscar_zona_analisis_por_maquina(id)
                for result in results:
                    zona = result["id_zona_analisis"]
                    results2 = sql_service.buscar_punto_por_zona(zona)
                    for result2 in results2:
                        lectura = sql_service.buscar_lectura_por_punto(result2["id_punto"])
                        if lectura[0]["ruta_canal_2"] != None:
                            count = 3
                        else:
                            count = 1
                        self.table.insert("", tk.END, values=(result["nombre_zona"], result2["nombre_punto"], count, lectura[0]["date_time"]))

            case "zona":
                self.table['columns'] = ('Punto', 'Ejes', 'Fecha')
                self.table.heading('Punto', text='Punto')
                self.table.heading('Ejes', text='Cantidad de ejes')
                self.table.heading('Fecha', text='Fecha')
                results = sql_service.buscar_punto_por_zona(id)
                for result in results:
                    # siempre se busca la ultima lectura
                    lectura = sql_service.buscar_lectura_por_punto(result["id_punto"])[-1]
                    if lectura["ruta_canal_2"] != None:
                        count = 3
                    else:
                        count = 1
                    self.table.insert("", tk.END, values=(result["nombre_punto"], count, lectura["date_time"]))

            case "punto":
                self.table['columns'] = ('punto', 'Eje', 'Fecha')# lecturas
                self.table.heading('punto', text='Punto')
                self.table.heading('Eje', text='Eje')
                self.table.heading('Fecha', text='Fecha')
                results = sql_service.buscar_lectura_por_punto(id)
                nombre_punto = sql_service.buscar_punto_por_id(results[0]["id_punto"])["nombre_punto"]
                for result in results:
                    self.table.insert("", tk.END, iid=result["ruta_canal_1"], values=(nombre_punto, 'Horizontal', result["date_time"]))
                    self.table.insert("", tk.END, iid=result["ruta_canal_2"], values=(nombre_punto, 'Vertical', result["date_time"]))
                    self.table.insert("", tk.END, iid=result["ruta_canal_3"], values=(nombre_punto, 'Axial', result["date_time"]))
    
    def OnDoubleClickhistorico(self, event):
        filename = event.widget.selection()[0]
        query = sql_service.get_pestana(filename)
        sample_rate = query[0]
        name = '/'.join(query[1:]) + '/' + mapping_ejes[filename[0]]
        filename = s3_service.get_reading(filename)
        #newtab(filename, name, sample_rate)



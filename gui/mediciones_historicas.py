import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")
root.title("Menú Treeview con Estructura de Carpetas")

# Crear el menú Treeview
tree = ttk.Treeview(root, columns=("size", "modified"), show="tree")
tree.heading("#0", text="Nombre de Archivo", anchor="w")
tree.heading("size", text="Tamaño", anchor="w")
tree.heading("modified", text="Modificado", anchor="w")

# Agregar elementos al menú Treeview
folder1_iid = tree.insert("", "end", text="Carpeta 1")
folder2_iid = tree.insert("", "end", text="Carpeta 2")
file1_iid = tree.insert(folder1_iid, "end", text="Archivo 1", values=("1 MB", "12/2/2022"))
file2_iid = tree.insert(folder2_iid, "end", text="Archivo 2", values=("500 KB", "13/2/2022"))

# Configurar el tamaño y la ubicación del menú Treeview
tree.place(relx=0, rely=0, relheight=1, relwidth=0.25)

# Crear una tabla de ejemplo con cuatro columnas y cinco registros
table = ttk.Treeview(root, columns=("column1", "column2", "column3", "column4"), show="headings")
table.column("column1", width=100, anchor="center")
table.column("column2", width=100, anchor="center")
table.column("column3", width=100, anchor="center")
table.column("column4", width=100, anchor="center")
table.heading("column1", text="Columna 1")
table.heading("column2", text="Columna 2")
table.heading("column3", text="Columna 3")
table.heading("column4", text="Columna 4")

table.focus_set()


for i in range(5):
    table.insert("", "end", text=f"Fila {i+1}", values=(f"{i+1}A", f"{i+1}B", f"{i+1}C", f"{i+1}D"))

# Ubicar la tabla en la parte libre de la ventana
table.place(relx=0.3, rely=0.1, relheight=0.8, relwidth=0.6)

# Función para cambiar la tabla en la parte libre de la ventana
def change_table(event):
    selected_items = tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        item_text = tree.item(selected_item)["text"]
        if item_text == "Carpeta 1":
            for i in range(5):
                values = (f"{i+1}A", f"{i+1}B", f"{i+1}C", f"{i+1}D")
                table.item(table.get_children()[i], values=values)
        elif item_text == "Carpeta 2":
            for i in range(5):
                values = (f"{i+1}E", f"{i+1}F", f"{i+1}G", f"{i+1}H")
                table.item(table.get_children()[i], values=values)


# Asociar la función de cambio de tabla al evento de selección de elemento en el menú Treeview
tree.bind("<<TreeviewSelect>>", change_table)


root.mainloop()

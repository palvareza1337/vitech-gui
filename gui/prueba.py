import tkinter as tk 
 
class Window(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.evar = tk.StringVar()  # Crear la variable StringVar
        self.label = tk.Label(self, textvariable=self.evar)  # Asignar la variable StringVar al texto de la etiqueta
        self.label.pack(padx=50, pady=50)
        button= tk.Button(self, text="Open window", command=self.onClick)
        button.pack(padx=50, pady=50)
 
    def onClick(self):
        settingsWindow = tk.Toplevel()
        tk.Label(settingsWindow, text="Settings Window").grid(row=0)
 
        note = tk.Entry(settingsWindow, width=30, textvariable=self.evar)  # Asignar la variable StringVar al valor del Entry
        note.grid(row=6,padx=5,pady=5)
 
        button = tk.Button(settingsWindow, text="Submit Data", command=settingsWindow.destroy)
        button.grid(row=7)
 
        settingsWindow.wait_window()
        print("finished waiting...")

 
root = tk.Tk()
Window(root).pack(side="top", fill="both", expand=True)
root.mainloop()

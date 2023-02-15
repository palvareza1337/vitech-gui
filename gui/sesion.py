import tkinter as tk
from tkinter import messagebox


def cerrar_sesion(root):
    opcion = messagebox.askquestion("Salir", "Quieres salir de la aplicacion")
    if opcion == "yes":
        print("close")
        root.destroy()

def iniciar_sesion():
    return True


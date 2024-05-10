from tkinter import ttk
from tkinter import *
import sqlite3
from ventanaPrincipal import *
from VentanaEditarProducto import *




if __name__=='__main__':
    root = Tk() # Instancia de la ventana principal
    app = VentanaPrincipal(root)#Se envia a la clase VentanaPrincipal el control sobre la ventana root
    root.mainloop() #comenzamos el bucle de aplicacion, es como un while True

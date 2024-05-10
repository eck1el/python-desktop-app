from tkinter import ttk
from tkinter import *
import sqlite3
from ventanaPrincipal import *
class VentanaEditarProducto:

    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        #Creacion del contenedor frame para la edición del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente producto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row = 0, column=0, columnspan=2, pady=20, padx=20)

        #Label y Entry para el nombre antiguo(Solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri',13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1, column=1)

        # Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri',13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3, column=1)
        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri',13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        # Botón Actualizar Producto
        ttk.Style().configure('my.TButton', font=('Calibri', 14, 'bold'))
        # Ejemplo de cómo creamos y configuramos el estilo en una sola línea
        ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=self.actualizar).grid(row=5, columnspan=2, sticky=W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio

        if nuevo_nombre and nuevo_precio:
            query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(self.nombre)
        else:
            self.mensaje['text'] = 'No se pudo actualizar el producto {}'.format(self.nombre)

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()
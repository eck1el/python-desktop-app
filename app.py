from tkinter import ttk
from tkinter import *
import sqlite3

class VentanaPrincipal:
    db = 'database/productos.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos") # titulo de la ventana
        self.ventana.resizable(1,1) #Activar la redimension de la ventana, para desactivarla:(0,0)
        self.ventana.wm_iconbitmap('recursos/folder.png')

        #Creacion del contenedor Frame principal
        frame = LabelFrame(self.ventana, text = "Registrar un nuevo Producto")
        frame.grid(row = 0, column=0, columnspan=3, pady=20)

        #Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ") #Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre.grid(row=1, column=0)

        #Entry Nombre(Caja de texto que recibira el nombre)
        self.nombre = Entry(frame) #Caja de texto(input de texto) ubicada en el frame
        self.nombre.focus() #Para que el foco del raton vaya a este Entry al inicio
        self.nombre.grid(row=1, column=1)

        #Label precio
        self.etiqueta_precio = Label(frame, text="Precio: ") #Etiqueta de texto ubicada en el frame
        self.etiqueta_precio.grid(row=2, column=0)
        #Entry Precio (Caja de texto que recibira el precio)
        self.precio = Entry(frame) #Caja de texto (input de texto) ubicada en el frame
        self.precio.grid(row=2, column=1)

        #Boton Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text = "Guardar Producto", command=self.add_producto)
        self.boton_aniadir.grid(row = 3, columnspan=2, sticky=W + E)

        #Tabla de Productos
        #Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold')) # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})]) # Eliminamos los bordes

        #Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W + E)

        #Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row = 4, column = 0, columnspan=2)
        self.tabla.heading('#0', text = 'Nombre', anchor=CENTER) #Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 0

        #Llamada al metodo get_productos() para obtener el listado de productos al inicio de la app
        self.get_productos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con: #Iniciamos una conexion con la base de datos
            cursor = con.cursor() #Generamos un cursor de la conexion para poder operar en la base de datos
            resultado = cursor.execute(consulta, parametros) #Preparar la consulta SQL(con parametros si los hay)
            con.commit()#Ejecutar la consulta SQL preparada anteriormente
        return resultado #Retornar el resultado de la consulta SQL

    def get_productos(self):
        #Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children() #Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)


        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query) #Se hace la llamada al metodo db_consultas

        for fila in registros_db:
            print(fila) #print para verificar por consola los datos
            self.tabla.insert('', 0, text=fila[1], values=fila[2])

    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacio'
            return
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje['text'] = "El precio es obligatorio y debe ser un número válido mayor que 0"
            return

        query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
        parametros = (self.nombre.get(), self.precio.get())
        self.db_consulta(query, parametros)
        #print("Datos guardados")
        self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
        self.nombre.delete(0, END) #Borrar el campo nombre del formulario
        self.precio.delete(0, END)  # Borrar el campo precio del formulario

        #Debug
        self.get_productos() # Cuando se finalice la insercion de datos volvemos a invocar a este metodo para actualizar el contenido

        #print(self.nombre.get())
        #print(self.precio.get())


if __name__=='__main__':
    root = Tk() # Instancia de la ventana principal
    app = VentanaPrincipal(root)#Se envia a la clase VentanaPrincipal el control sobre la ventana root
    root.mainloop() #comenzamos el bucle de aplicacion, es como un while True

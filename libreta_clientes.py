from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import os
from customtkinter import *

import appdirs
import platform

set_appearance_mode("light")
root = CTk()
root.title('Libreta de Clientes')

# Identificación de aplicación en windows
myappid = "CRM-app-libreta-v1.0"

# # directorio_actual = os.path.dirname(__file__)
directorio_base = os.path.dirname(__file__)

# Agregar icono de la app
# Verificar el sistema operativo
if platform.system() == "Windows":
    from ctypes import windll  # Only exists on Windows.
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    root.iconbitmap(os.path.join(directorio_base, 'libreta.ico'))
elif platform.system() == "Linux":
    root.iconphoto(True, PhotoImage(file=os.path.join(directorio_base, "libreta.png")))

# # conexión base de datos
# nombre_db = 'crm.db'
# ruta_base_de_datos = os.path.join(directorio_base, nombre_db)
# conn = sqlite3.connect(ruta_base_de_datos)

# Directorio donde se guardara la base de datos
app_name = "LibretaClientes"
app_author = myappid
db_dir = appdirs.user_data_dir(app_name, app_author)
os.makedirs(db_dir, exist_ok=True)

# Conexión a la base de datos
ruta_base_de_datos = os.path.join(db_dir, 'crm.db')
conn = sqlite3.connect(ruta_base_de_datos)

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        empresa TEXT NOT NULL
    );
""")
conn.commit()

def render_cliente():
    rows = c.execute("SELECT * FROM cliente")
    conn.commit()

    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

def insertar(cliente):
    c.execute(""" 
    INSERT INTO cliente (nombre, telefono, empresa) VALUES (?, ?, ?)
    """, (cliente['nombre'], cliente['telefono'], cliente['empresa']))
    conn.commit()
    render_cliente()

def nuevo_cliente():
    def guardar():
        if not nombre.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return
        if not telefono.get():
            messagebox.showerror('Error', 'El telefono es obligatorio')
            return
        if not empresa.get():
            messagebox.showerror('Error', 'La empresa es obligatorio')
            return
        
        cliente = {
            'nombre': nombre.get(),
            'telefono': telefono.get(),
            'empresa': empresa.get()
        }
        insertar(cliente)
        top.destroy()

    top = CTkToplevel(root)
    top.title('Nuevo Cliente')
    top.geometry('500x180')

    lnombre = CTkLabel(top, text='Nombre')
    lnombre.grid(row=0, column=0, padx=5, pady=5)
    nombre = CTkEntry(top, width=400)
    nombre.grid(row=0, column=1, padx=5, pady=5)

    ltelefono= CTkLabel(top, text='Teléfono')
    ltelefono.grid(row=1, column=0, padx=5, pady=5)
    telefono = CTkEntry(top, width=400)
    telefono.grid(row=1, column=1, padx=5, pady=5)

    lempresa = CTkLabel(top, text='Empresa')
    lempresa.grid(row=2, column=0, padx=5, pady=5)
    empresa = CTkEntry(top, width=400)
    empresa.grid(row=2, column=1, padx=5, pady=5)

    btn_guardar = CTkButton(top, text='Guardar', command=guardar)
    btn_guardar.grid(row=3, column=1, padx=5, pady=5)

def eliminar_cliente():
    id = tree.selection()[0]
    cliente = c.execute("SELECT * FROM cliente WHERE id = ?", (id, )).fetchone()
    respuesta = messagebox.askokcancel('Seguro?', 'Estas seguro de eliminar el cliente ' + cliente[1] + '?')
    if respuesta:
        c.execute("DELETE FROM cliente WHERE id = ?", (id, ))
        conn.commit()
        render_cliente()
    else:
        pass

btn_newClient = CTkButton(root, text='Nuevo', command=nuevo_cliente)
btn_newClient.grid(row=0, column=0)
btn_eliminar = CTkButton(root, text='Eliminar', command=eliminar_cliente)
btn_eliminar.grid(row=0, column=1)

tree = ttk.Treeview(root)
tree['columns'] = ('Nombre', 'Telefono', 'Empresa')

tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Teléfono')
tree.heading('Empresa', text='Empresa')

tree.grid(row=1, column=0, columnspan=2)

render_cliente()

root.mainloop()

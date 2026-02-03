import tkinter as tk
from tkinter import ttk, messagebox
import os

ARCHIVO = "gastos.txt"
nombresProductos = []
categoriasProductos = []

usuario = "Byron"
clave = "2025"

# ---------------- LOGIN ----------------
def verificar_login():

    if entrada_usuario.get() == "" or entrada_clave.get() == "":
        messagebox.showerror("Error", "Complete todos los campos")
        return
    
    if entrada_usuario.get() == usuario and entrada_clave.get() == clave:
        login.destroy()
        abrir_app()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        entrada_usuario.delete(0, tk.END)
        entrada_clave.delete(0, tk.END)


login = tk.Tk()
login.title("Login")
login.geometry("700x350")
login.resizable(False, False)

contenedor = tk.Frame(login)
contenedor.pack(fill="both", expand=True)

# -------- PANEL IZQUIERDO login --------
panel_izq = tk.Frame(contenedor, bg="#E85C55", width=300)
panel_izq.pack(side="left", fill="both")

tk.Label(
    panel_izq,
    text="Bienvenido\nal Sistema",
    bg="#E85C55",
    fg="white",
    font=("Arial", 20, "bold"),
    justify="center"
).place(relx=0.5, rely=0.4, anchor="center")

tk.Label(
    panel_izq,
    text="\nControla tus gastos\nde forma sencilla",
    bg="#E85C55",
    fg="white",
    font=("Arial", 11),
    justify="center"
).place(relx=0.5, rely=0.55, anchor="center")

# -------- PANEL DERECHO login --------
panel_der = tk.Frame(contenedor, bg="#0F253D")
panel_der.pack(side="right", fill="both", expand=True)

form = tk.Frame(panel_der, bg="#0F253D")
form.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    form,
    text="INICIAR SESIÓN",
    bg="#0F253D",
    fg="white",
    font=("Arial", 16, "bold")
).pack(pady=10)

# Usuario
tk.Label(form, text="Usuario", bg="#0F253D", fg="white").pack(anchor="w")
entrada_usuario = tk.Entry(form, width=30, bg="#1E3A5F", fg="white", relief="flat")
entrada_usuario.pack(pady=5, ipady=6)

# Contraseña
tk.Label(form, text="Contraseña", bg="#0F253D", fg="white").pack(anchor="w", pady=(10,0))
entrada_clave = tk.Entry(
    form, width=30, bg="#1E3A5F",
    fg="white", show="●", relief="flat"
)
entrada_clave.pack(pady=5, ipady=6)

# Botón Ingresar
tk.Button(
    form,
    text="Ingresar",
    bg="#E85C55",
    fg="white",
    width=25,
    relief="flat",
    command=verificar_login
).pack(pady=20)

# ---------------- VENTANA DE LOS GASTOS ( el CRUD ) ----------------
def abrir_app():
    ventana = tk.Tk()
    ventana.title(" - Control de Gastos -")
    ventana.geometry("700x480")
    ventana.config(bg="#133151")
    ventana.resizable(False, False)

    # ---------------- ENCABEZADO ----------------
    header = tk.Frame(ventana, bg="#E85C55", height=60)
    header.pack(fill="x")

    label_total = tk.Label(
        header,
        text="Total: $0.00",
        bg="#E85C55",
        fg="white",
        font=("Arial", 14, "bold")
    )
    label_total.pack(side="right", padx=20)

    tk.Label(
        header,
        text="Gastos del Evento",
        bg="#E85C55",
        fg="white",
        font=("Arial", 16, "bold")
    ).pack(side="left", padx=20)

    # ---------------- CONTENEDOR ----------------
    contenedor = tk.Frame(ventana, bg="#133151")
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- FORMULARIO ----------------
    form = tk.LabelFrame(contenedor, text="AGREGAR GASTO", bg="#0F253D", fg="white")
    form.pack(side="left", fill="y", padx=10)

    tk.Label(form, text="Nombre:", bg="#0F253D", fg="white").pack(anchor="w", padx=10)
    entrada_nombre = tk.Entry(form, width=25, bg="#B3B7BD")
    entrada_nombre.pack(padx=10, pady=5)

    tk.Label(form, text="Categoría:", bg="#0F253D", fg="white").pack(anchor="w", padx=10)
    entrada_categoria = tk.Entry(form, width=25, bg="#B3B7BD")
    entrada_categoria.pack(padx=10, pady=5)

    tk.Label(form, text="Precio:", bg="#0F253D", fg="white").pack(anchor="w", padx=10)
    entrada_precio = tk.Entry(form, width=25, bg="#B3B7BD")
    entrada_precio.pack(padx=10, pady=5)

    # ---------------- TABLA ----------------
    tabla_frame = tk.Frame(contenedor, bg="#133151")
    tabla_frame.pack(side="right", fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    fieldbackground="white",
                    rowheight=25)
    style.configure("Treeview.Heading",
            background="#A09797",
            foreground="black",)

    tabla = ttk.Treeview(
        tabla_frame,
        columns=("Nombre", "Categoria", "Precio"),
        show="headings"
    )
    tabla.heading("Nombre", text="Gasto")
    tabla.heading("Categoria", text="Categoría")
    tabla.heading("Precio", text="Precio")

    tabla.column("Nombre", width=150, anchor="center")
    tabla.column("Categoria", width=150, anchor="center")
    tabla.column("Precio", width=100, anchor="center")

    tabla.pack(fill="both", expand=True, pady=10)

    # ---------------- FUNCIONES ----------------
    def limpiar():
        entrada_nombre.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)

    def calcular_total():
        total = 0
        for fila in tabla.get_children():
            total += float(tabla.item(fila)["values"][2])
        label_total.config(text=f"Total: $ {total:.2f}")

    def guardar():
        with open(ARCHIVO, "w") as f:
            for fila in tabla.get_children():
                n, c, p = tabla.item(fila)["values"]
                f.write(f"{n}|{c}|{p}\n")

    def cargar():
        nombresProductos.clear()
        categoriasProductos.clear()
        if not os.path.exists(ARCHIVO):
            return
        with open(ARCHIVO, "r") as f:
            for linea in f:
                n, c, p = linea.strip().split("|")
                tabla.insert("", "end", values=(n, c, float(p)))
                nombresProductos.append(n)
                categoriasProductos.append(c)
        calcular_total()

    def agregar_gasto():
        n = entrada_nombre.get()
        c = entrada_categoria.get()
        p = entrada_precio.get()

        senialRepetir = ""
        senial = validarSoloLetras(n, "Nombre del Producto")
        senial1 = validarSoloLetras(c, "Categoria del Producto")
        if senial != "1": senialRepetir = noRepetir(n, c)
        if senial != "1" and senialRepetir != "1" and senial1 != "1":

            if n == "" or c == "" or p == "":
                messagebox.showerror("Error", "Complete todos los campos")
                return

            if not p.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Precio inválido")
                return

            tabla.insert("", "end", values=(n, c, float(p)))
            nombresProductos.append(n)
            categoriasProductos.append(c)
            guardar()
            calcular_total()
            limpiar()

    def eliminar_gasto():
        sel = tabla.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un gasto")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este gasto?"):
            nombre_producto = tabla.item(sel)["values"][0]
            categoria_producto = tabla.item(sel)["values"][1]
            if nombre_producto in nombresProductos:
                nombresProductos.remove(nombre_producto)
            if categoria_producto in categoriasProductos:
                categoriasProductos.remove(categoria_producto)
            tabla.delete(sel)
            guardar()
            calcular_total()

    def noRepetir(nombreBuscar, categoria):
            if nombreBuscar in nombresProductos and categoria in categoriasProductos:
                messagebox.showinfo("AVISO", "El  " + nombreBuscar + "  ya existe en categoria " + categoria)
                return "1" 

    def validarSoloLetras(mensaje = "", campo = ""):
        numeros = "1234567890"
        for i in range(len(mensaje)):
            for n in range(len(numeros)):
                if mensaje[i] == numeros[n]:
                    messagebox.showerror("Error", "Solo se puden colocar letras en " + str(campo))
                    return "1"
                
    def editar_gasto():
        sel = tabla.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un gasto")
            return

        valores = tabla.item(sel)["values"]

        editar = tk.Toplevel(ventana)
        editar.title("Editar")
        editar.geometry("225x250")
        editar.config(bg="#0F253D")
        editar.grab_set()

        tk.Label(editar, text="Nombre", bg="#0F253D", fg="white").pack(pady=5)
        e_nombre = tk.Entry(editar)
        e_nombre.pack()
        e_nombre.insert(0, valores[0])

        tk.Label(editar, text="Categoría", bg="#0F253D", fg="white").pack(pady=5)
        e_categoria = tk.Entry(editar)
        e_categoria.pack()
        e_categoria.insert(0, valores[1])

        tk.Label(editar, text="Precio", bg="#0F253D", fg="white").pack(pady=5)
        e_precio = tk.Entry(editar)
        e_precio.pack()
        e_precio.insert(0, valores[2])

        def guardar_edicion():
            if not e_precio.get().replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Precio inválido", parent=editar)
                return
            tabla.item(sel, values=(
                e_nombre.get(),
                e_categoria.get(),
                float(e_precio.get())
            ))
            guardar()
            calcular_total()
            editar.destroy()

        tk.Button(
            editar, text="Guardar cambios",
            bg="#E85C55", fg="white",
            command=guardar_edicion
        ).pack(pady=15)

    # ---------------- BOTONES ----------------
    botones = tk.Frame(form, bg="#0F253D")
    botones.pack(pady=15)

    tk.Button(botones, text="Agregar", bg="#4CAF50", fg="white",
              width=15, command=agregar_gasto)\
        .grid(row=0, column=0, padx=5, pady=5)

    tk.Button(botones, text="Editar", bg="#2196F3", fg="white",
              width=15, command=editar_gasto)\
        .grid(row=0, column=1, padx=5, pady=5)

    tk.Button(botones, text="Eliminar", bg="#812d27", fg="white",
              width=32, command=eliminar_gasto)\
        .grid(row=1, column=0, columnspan=2, pady=5)

    cargar()
    ventana.mainloop()

login.mainloop()

import tkinter as tk
from tkinter import messagebox
import json

# ---------- Persistencia ----------
ARCHIVO_DATOS = "inventario.json"

# Diccionario para guardar frutas y cantidades
inventario = {}

def guardar_inventario():
    with open(ARCHIVO_DATOS, "w") as archivo:
        json.dump(inventario, archivo)

def cargar_inventario():
    global inventario
    try:
        with open(ARCHIVO_DATOS, "r") as archivo:
            inventario = json.load(archivo)
    except FileNotFoundError:
        inventario = {}

# ---------- Funciones principales ----------

def agregar_fruta():
    fruta = entrada_fruta.get().strip()
    try:
        cantidad = int(entrada_cantidad.get())
        if fruta:
            inventario[fruta] = inventario.get(fruta, 0) + cantidad
            guardar_inventario()
            print(f"Se agregó {cantidad} unidad(es) de '{fruta}'. Total: {inventario[fruta]}")
            actualizar_lista()
            limpiar_campos()
        else:
            print("⚠️ No ingresaste el nombre de la fruta.")
            messagebox.showwarning("Advertencia", "Ingrese el nombre de la fruta.")
    except ValueError:
        print("❌ La cantidad no es un número válido.")
        messagebox.showerror("Error", "Cantidad inválida.")

def eliminar_fruta():
    fruta = entrada_fruta.get().strip()
    if fruta in inventario:
        del inventario[fruta]
        guardar_inventario()
        print(f"'{fruta}' fue eliminada del inventario.")
        actualizar_lista()
        limpiar_campos()
    else:
        print(f"⚠️ La fruta '{fruta}' no está en el inventario.")
        messagebox.showinfo("Eliminar", "Fruta no encontrada.")

def editar_fruta():
    fruta = entrada_fruta.get().strip()
    try:
        cantidad = int(entrada_cantidad.get())
        if fruta in inventario:
            inventario[fruta] = cantidad
            guardar_inventario()
            print(f"Cantidad de '{fruta}' actualizada a {cantidad}.")
            actualizar_lista()
            limpiar_campos()
        else:
            print(f"⚠️ La fruta '{fruta}' no existe en el inventario.")
            messagebox.showwarning("Editar", "Fruta no encontrada.")
    except ValueError:
        print("❌ La cantidad ingresada no es válida.")
        messagebox.showerror("Error", "Cantidad inválida.")

def disminuir_fruta():
    fruta = entrada_fruta.get().strip()
    try:
        cantidad = int(entrada_cantidad.get())
        if fruta in inventario:
            if cantidad <= inventario[fruta]:
                inventario[fruta] -= cantidad
                guardar_inventario()
                print(f"Se disminuyó {cantidad} de '{fruta}'. Quedan: {inventario[fruta]}")
                actualizar_lista()
                limpiar_campos()
                if inventario[fruta] == 0:
                    print(f"ℹ️ '{fruta}' ahora tiene 0 unidades.")
                    messagebox.showinfo("Aviso", f"{fruta} ahora tiene 0 unidades.")
            else:
                print(f"⚠️ Intentaste quitar más de lo que hay de '{fruta}'.")
                messagebox.showwarning("Advertencia", "Cantidad mayor a lo disponible.")
        else:
            print(f"⚠️ La fruta '{fruta}' no está en el inventario.")
            messagebox.showinfo("Aviso", "Fruta no encontrada.")
    except ValueError:
        print("❌ La cantidad no es válida.")
        messagebox.showerror("Error", "Cantidad inválida.")

def seleccionar_fruta(event):
    seleccion = lista.curselection()
    if seleccion:
        item = lista.get(seleccion[0])
        fruta, cantidad = item.split(":")
        entrada_fruta.delete(0, tk.END)
        entrada_fruta.insert(0, fruta.strip())
        entrada_cantidad.delete(0, tk.END)
        entrada_cantidad.insert(0, cantidad.strip())
        print(f"Seleccionaste: {fruta.strip()} con {cantidad.strip()} unidades.")

def actualizar_lista():
    lista.delete(0, tk.END)
    for fruta, cantidad in inventario.items():
        lista.insert(tk.END, f"{fruta}: {cantidad}")

def limpiar_campos():
    entrada_fruta.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)

# ---------- Cargar datos antes de mostrar ventana ----------
cargar_inventario()

# ---------- Interfaz Gráfica ----------
ventana = tk.Tk()
ventana.title("🍎 Inventario de Frutas")
ventana.configure(bg="#f0f5f5")
ventana.geometry("550x500")

tk.Label(ventana, text="Fruta:", bg="#f0f5f5").pack(pady=(10,0))
entrada_fruta = tk.Entry(ventana, width=30)
entrada_fruta.pack(pady=5)

tk.Label(ventana, text="Cantidad:", bg="#f0f5f5").pack()
entrada_cantidad = tk.Entry(ventana, width=30)
entrada_cantidad.pack(pady=5)

# Botones
frame_botones = tk.Frame(ventana, bg="#f0f5f5")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Agregar", bg="#d4f4dd", command=agregar_fruta, width=10).grid(row=0, column=0, padx=5, pady=2)
tk.Button(frame_botones, text="Editar", bg="#fff3b0", command=editar_fruta, width=10).grid(row=0, column=1, padx=5, pady=2)
tk.Button(frame_botones, text="Eliminar", bg="#ffcccc", command=eliminar_fruta, width=10).grid(row=0, column=2, padx=5, pady=2)
tk.Button(frame_botones, text="Disminuir", bg="#cce5ff", command=disminuir_fruta, width=10).grid(row=1, column=1, padx=5, pady=5)

# Lista
tk.Label(ventana, text="Inventario Actual:", bg="#f0f5f5", font=("Arial", 10, "bold")).pack(pady=5)
lista = tk.Listbox(ventana, width=40, height=10)
lista.pack(pady=5)
lista.bind("<<ListboxSelect>>", seleccionar_fruta)

# Mostrar el inventario cargado
actualizar_lista()

ventana.mainloop()
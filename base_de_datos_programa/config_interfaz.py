import tkinter as tk
from tkinter import filedialog
import json
import os

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_selected)

def save_data_json(tespera, tiempo, capturas, letra, folder):
    datos = {
        "tespera": tespera,
        "tiempo": tiempo,
        "capturas": capturas,
        "letra": letra,
        "carpeta": folder
    }
    try:
        with open("config.json", "w") as file:
            json.dump(datos, file, indent=4)
        print("Configuración guardada en config.json")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

def load_data_json():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as file:
                datos = json.load(file)
            # Insertar valores en las casillas de entrada
            tiempo_entry0.insert(0, datos.get("tespera", ""))
            tiempo_entry1.insert(0, datos.get("tiempo", ""))
            capturas_entry.insert(0, datos.get("capturas", ""))
            letra_var.set(datos.get("letra", letras[0]))  # Valor por defecto si no existe
            folder_entry.insert(0, datos.get("carpeta", ""))
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

def save_values():
    tespera = tiempo_entry0.get()
    tiempo = tiempo_entry1.get()
    capturas = capturas_entry.get()
    letra = letra_var.get()
    carpeta = folder_entry.get()
    save_data_json(tespera, tiempo, capturas, letra, carpeta)
    print(f"Tiempo de espera: {tespera} segundos")
    print(f"Tiempo: {tiempo} segundos")
    print(f"Número de capturas por segundo: {capturas}")
    print(f"Letra seleccionada: {letra}")
    print(f"Carpeta para guardar imágenes: {carpeta}")
    root.destroy()  # Cierra la ventana

# Crear ventana
root = tk.Tk()
root.title("Configuración de Capturas")

# Campo para tiempo en segundos
tk.Label(root, text="Tiempo Espera (s):").grid(row=0, column=0)
tiempo_entry0 = tk.Entry(root)
tiempo_entry0.grid(row=0, column=1)

# Campo para tiempo en segundos
tk.Label(root, text="Tiempo captura (s):").grid(row=1, column=0)
tiempo_entry1 = tk.Entry(root)
tiempo_entry1.grid(row=1, column=1)

# Campo para número de capturas por segundo
tk.Label(root, text="Capturas por segundo:").grid(row=2, column=0)
capturas_entry = tk.Entry(root)
capturas_entry.grid(row=2, column=1)

# Menú desplegable para seleccionar una letra
tk.Label(root, text="Selecciona una letra:").grid(row=3, column=0)
letras = [chr(i) for i in range(65, 91)]  # Lista de letras A-Z
letra_var = tk.StringVar()
letra_var.set(letras[0])  # Valor por defecto
letra_menu = tk.OptionMenu(root, letra_var, *letras)
letra_menu.grid(row=3, column=1)

# Botón para seleccionar carpeta
tk.Label(root, text="Carpeta de imágenes:").grid(row=4, column=0)
folder_entry = tk.Entry(root)
folder_entry.grid(row=4, column=1)
folder_button = tk.Button(root, text="Seleccionar", command=select_folder)
folder_button.grid(row=4, column=2)

# Botón para guardar valores
save_button = tk.Button(root, text="Guardar", command=save_values)
save_button.grid(row=6, column=2)

# Cargar valores desde el JSON al iniciar la ventana
load_data_json()

# Ejecutar interfaz
root.mainloop()
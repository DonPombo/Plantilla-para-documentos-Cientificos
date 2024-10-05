# interfaz.py
import tkinter as tk
from tkinter import filedialog
import json
import os
from tkinter import messagebox
from logica import cargar_plantilla, validar_datos, generar_docx, convertir_a_pdf

# Ruta del archivo de configuración
CONFIG_FILE = 'config.json'

# Función para cargar los datos de configuración desde un archivo JSON
def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}

# Función para guardar la configuración del usuario en un archivo JSON
def guardar_configuracion(datos):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(datos, file, ensure_ascii=False, indent=4)

# Función para restablecer la configuración del usuario
def restablecer_configuracion():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    # Limpiar los campos de entrada personales
    entrada_nombre.delete(0, tk.END)
    entrada_apellidos.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)
    messagebox.showinfo("Restablecido", "Los datos personales han sido restablecidos.")

# Función para agregar dinámicamente una etiqueta y un campo de entrada
def agregar_campo(titulo, ventana, valor_default=""):
    tk.Label(ventana, text=titulo).pack()
    entrada = tk.Entry(ventana, width=60)
    entrada.pack()
    # Establecer un valor predeterminado si se proporciona (por ejemplo, de la configuración)
    if valor_default:
        entrada.insert(0, valor_default)
    return entrada

# Función para obtener los datos de la interfaz y generar el documento
def crear_documento():
    datos = {
        "titulo_espanol": entrada_titulo_espanol.get(),
        "titulo_ingles": entrada_titulo_ingles.get(),
        "autores": entrada_autores.get(),
        "afiliacion_1": entrada_afiliacion.get(),
        "resumen": entrada_resumen.get(),
        "palabras_clave": entrada_palabras.get(),
        "abstract": entrada_abstract.get(),
        "keywords": entrada_keywords.get(),
        "introduccion": entrada_introduccion.get(),
        "materiales_metodos": entrada_materiales_metodos.get(),
        "resultados_discusion": entrada_resultados_discusion.get(),
        "conclusiones": entrada_conclusiones.get()
    }

    # Validar los datos ingresados
    if not validar_datos(datos):
        return

    # Seleccionar la plantilla
    ruta_plantilla = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not ruta_plantilla:
        return

    plantilla = cargar_plantilla(ruta_plantilla)

    # Seleccionar la ruta de guardado para el archivo generado (.docx)
    archivo_docx = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Documentos de Word", "*.docx")])
    if not archivo_docx:
        return

    # Generar el documento .docx
    generar_docx(plantilla, datos, archivo_docx)

    # Guardar la configuración del usuario (nombre, apellidos y correo electrónico)
    config_datos = {
        "nombre": entrada_nombre.get(),
        "apellidos": entrada_apellidos.get(),
        "correo": entrada_correo.get()
    }
    guardar_configuracion(config_datos)

    # Preguntar si se desea generar un PDF
    generar_pdf = messagebox.askyesno("Generar PDF", "¿Deseas generar también un PDF del documento?")
    if generar_pdf:
        archivo_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivo PDF", "*.pdf")])
        if archivo_pdf:
            convertir_a_pdf(archivo_docx, archivo_pdf)

# Configuración de la ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Generador de Documentos .docx y PDF")
ventana.geometry("600x800")

# Cargar configuración desde el archivo JSON
config = cargar_configuracion()

# Campos de entrada de información personal
entrada_nombre = agregar_campo("Nombre", ventana, config.get("nombre", ""))
entrada_apellidos = agregar_campo("Apellidos", ventana, config.get("apellidos", ""))
entrada_correo = agregar_campo("Correo Electrónico", ventana, config.get("correo", ""))

# Campos de entrada de información del documento
entrada_titulo_espanol = agregar_campo("Título en Español", ventana)
entrada_titulo_ingles = agregar_campo("Título en Inglés", ventana)
entrada_autores = agregar_campo("Autores", ventana)
entrada_afiliacion = agregar_campo("Afiliación Institucional", ventana)
entrada_resumen = agregar_campo("Resumen", ventana)
entrada_palabras = agregar_campo("Palabras Clave", ventana)
entrada_abstract = agregar_campo("Abstract (Inglés)", ventana)
entrada_keywords = agregar_campo("Keywords (Inglés)", ventana)
entrada_introduccion = agregar_campo("Introducción", ventana)
entrada_materiales_metodos = agregar_campo("Materiales y Métodos", ventana)
entrada_resultados_discusion = agregar_campo("Resultados y Discusión", ventana)
entrada_conclusiones = agregar_campo("Conclusiones", ventana)

# Botones
tk.Button(ventana, text="Generar Documento", command=crear_documento).pack(pady=10)
tk.Button(ventana, text="Restablecer Datos Personales", command=restablecer_configuracion).pack(pady=10)

# Iniciar la aplicación
ventana.mainloop()

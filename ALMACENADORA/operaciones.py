# operaciones.py
# Aqui van las funciones que usa el programa principal
# Almacenadora de Materia Prima

import os
import csv
from datetime import datetime

# nombres de los archivos
ARCHIVO_PRODUCTOS = "productos.csv"
ARCHIVO_VENTAS = "ventas.txt"
ARCHIVO_BITACORA = "bitacora.log"


# esta funcion escribe cosas en la bitacora con la fecha
def registrar_bitacora(mensaje):
    try:
        archivo = open(ARCHIVO_BITACORA, "a", encoding="utf-8")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha}] {mensaje}\n")
        archivo.close()
    except:
        print("No se pudo escribir en la bitacora")


# esta funcion lee el archivo productos.csv
def cargar_inventario():
    inventario = []

    # si el archivo no existe lo creo con encabezados
    if not os.path.exists(ARCHIVO_PRODUCTOS):
        try:
            archivo = open(ARCHIVO_PRODUCTOS, "w", encoding="utf-8", newline="")
            escritor = csv.writer(archivo)
            escritor.writerow(["codigo", "nombre", "categoria",
                               "precio", "stock", "stock_minimo"])
            archivo.close()
            registrar_bitacora("Se creo el archivo de productos")
        except:
            print("Error al crear el archivo")
        return inventario

    # si existe lo leo
    try:
        archivo = open(ARCHIVO_PRODUCTOS, "r", encoding="utf-8")
        lector = csv.DictReader(archivo)
        for fila in lector:
            producto = {
                "codigo": fila["codigo"],
                "nombre": fila["nombre"],
                "categoria": fila["categoria"],
                "precio": float(fila["precio"]),
                "stock": int(fila["stock"]),
                "stock_minimo": int(fila["stock_minimo"])
            }
            inventario.append(producto)
        archivo.close()
        registrar_bitacora("Se cargo el inventario")
    except:
        print("Error al leer el archivo de productos")

    return inventario


# guarda el inventario en el csv
def guardar_inventario(inventario):
    try:
        archivo = open(ARCHIVO_PRODUCTOS, "w", encoding="utf-8", newline="")
        campos = ["codigo", "nombre", "categoria", "precio", "stock", "stock_minimo"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for producto in inventario:
            escritor.writerow(producto)
        archivo.close()
    except:
        print("Error al guardar inventario")


# guarda una venta en ventas.txt (se guarda como tupla)
def guardar_venta(venta):
    try:
        archivo = open(ARCHIVO_VENTAS, "a", encoding="utf-8")
        fecha, codigo, cantidad, total = venta
        archivo.write(f"{fecha},{codigo},{cantidad},{total:.2f}\n")
        archivo.close()
    except:
        print("Error al guardar la venta")


# lee todas las ventas del archivo
def cargar_ventas():
    ventas = []
    if not os.path.exists(ARCHIVO_VENTAS):
        return ventas
    try:
        archivo = open(ARCHIVO_VENTAS, "r", encoding="utf-8")
        for linea in archivo:
            partes = linea.strip().split(",")
            if len(partes) == 4:
                ventas.append((partes[0], partes[1], int(partes[2]), float(partes[3])))
        archivo.close()
    except:
        print("Error al leer ventas")
    return ventas
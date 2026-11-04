"""
Módulo de persistencia de datos (Archivos CSV y Log).
"""
import csv
from pathlib import Path
from datetime import datetime
from typing import List
from .modelos import Producto, Venta
from .inventario import Inventario
from .excepciones import ArchivoDatosError

class RepositorioCSV:
    """Maneja la lectura y escritura de productos y ventas en archivos."""

    def __init__(self, ruta_inventario: str, ruta_ventas: str):
        """Define las rutas usando pathlib."""
        self.ruta_inventario = Path(ruta_inventario)
        self.ruta_ventas = Path(ruta_ventas)

    def cargar_inventario(self) -> Inventario:
        """Carga el inventario desde el CSV. Si no existe, retorna uno vacío."""
        inventario = Inventario()
        if not self.ruta_inventario.exists():
            # Creamos la carpeta y el archivo si no existen
            self.ruta_inventario.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta_inventario, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["codigo", "nombre", "categoria", "precio", "stock", "stock_minimo"])
            return inventario

        try:
            with open(self.ruta_inventario, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    producto = Producto.desde_fila_csv(fila)
                    inventario.agregar(producto)
        except Exception as e:
            raise ArchivoDatosError(f"Error al cargar inventario: {e}")
        
        return inventario

    def guardar_inventario(self, inventario: Inventario) -> None:
        """Guarda todos los productos del inventario en el CSV."""
        try:
            with open(self.ruta_inventario, "w", encoding="utf-8", newline="") as f:
                campos = ["codigo", "nombre", "categoria", "precio", "stock", "stock_minimo"]
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                for producto in inventario:
                    writer.writerow(producto.a_diccionario())
        except Exception as e:
            raise ArchivoDatosError(f"Error al guardar inventario: {e}")

    def guardar_venta(self, venta: Venta) -> None:
        """Agrega una venta al archivo de texto en modo append."""
        try:
            with open(self.ruta_ventas, "a", encoding="utf-8") as f:
                f.write(venta.a_linea_txt())
        except Exception as e:
            raise ArchivoDatosError(f"Error al guardar venta: {e}")

    def cargar_ventas(self) -> List[Venta]:
        """Carga las ventas desde el archivo de texto."""
        ventas = []
        if not self.ruta_ventas.exists():
            return ventas
        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split(",")
                    if len(partes) == 4:
                        fecha = datetime.strptime(partes[0], "%Y-%m-%d %H:%M:%S")
                        venta = Venta(
                            fecha=fecha,
                            codigo_producto=partes[1],
                            cantidad=int(partes[2]),
                            total=float(partes[3])
                        )
                        ventas.append(venta)
        except Exception as e:
            raise ArchivoDatosError(f"Error al cargar ventas: {e}")
        return ventas


class Bitacora:
    """Registra las operaciones del sistema con fecha y hora."""

    def __init__(self, ruta_archivo: str):
        """Inicializa la bitácora."""
        self.ruta = Path(ruta_archivo)

    def registrar(self, mensaje: str) -> None:
        """Escribe un mensaje en el archivo en modo append."""
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta, "a", encoding="utf-8") as f:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{fecha}] {mensaje}\n")
        except Exception:
            # La bitácora no debería detener el programa si falla
            pass
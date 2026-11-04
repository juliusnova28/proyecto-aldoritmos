"""
Módulo de excepciones personalizadas para el sistema de inventario.
"""

class InventarioError(Exception):
    """Excepción base para todos los errores del sistema de inventario."""
    pass


class CodigoInvalidoError(InventarioError):
    """Se lanza cuando el código de un producto no cumple el formato (ej. MP001)."""
    pass


class ProductoNoEncontradoError(InventarioError):
    """Se lanza cuando se busca un producto y no existe en el inventario."""
    pass


class StockInsuficienteError(InventarioError):
    """Se lanza cuando se intenta vender más cantidad de la disponible en stock."""
    pass


class ArchivoDatosError(InventarioError):
    """Se lanza cuando hay un problema al leer o escribir los archivos CSV/TXT."""
    pass
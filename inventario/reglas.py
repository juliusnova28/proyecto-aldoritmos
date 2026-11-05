"""
Módulo de reglas de negocio usando herencia y polimorfismo.
"""
from abc import ABC, abstractmethod
from .modelos import Producto

class ReglaNegocio(ABC):
    """Clase base abstracta para las reglas del sistema."""

    @abstractmethod
    def evaluar(self, producto: Producto) -> str | None:
        """
        Evalúa la regla sobre un producto.
        Retorna un mensaje si se cumple la regla, o None si no.
        """
        pass

class SinAlerta(ReglaNegocio):
    """Regla vacía que no hace nada (útil para polimorfismo)."""

    def evaluar(self, producto: Producto) -> str | None:
        return None

class AlertaStockMinimo(ReglaNegocio):
    """Regla que verifica si el stock cayó por debajo o igual al mínimo."""

    def evaluar(self, producto: Producto) -> str | None:
        if producto.stock <= producto.stock_minimo:
            return f">>> ALERTA: {producto.nombre} tiene stock bajo ({producto.stock}). Mínimo requerido: {producto.stock_minimo}."
        return None
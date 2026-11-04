"""
Modelos de datos: Producto y Venta.
"""
from dataclasses import dataclass
from datetime import datetime
from .excepciones import CodigoInvalidoError


class Producto:
    """Representa un producto de la almacenadora con validaciones encapsuladas."""

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int, stock_minimo: int):
        """Inicializa un producto validando sus datos."""
        self.codigo = codigo  # Usa el setter para validar
        self.nombre = nombre.strip().title()
        self.categoria = categoria.strip().title()
        self.precio = precio
        self.stock = stock
        self.stock_minimo = stock_minimo

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str):
        valor = valor.strip().upper()
        if len(valor) != 5 or not valor[0:2].isalpha() or not valor[2:5].isdigit():
            raise CodigoInvalidoError(f"El código '{valor}' es inválido. Debe ser tipo MP001.")
        self._codigo = valor

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = float(valor)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = int(valor)

    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, valor: int):
        if valor < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")
        self._stock_minimo = int(valor)

    def descontar_stock(self, cantidad: int):
        """Resta la cantidad vendida al stock actual."""
        self.stock = self._stock - cantidad

    def __str__(self) -> str:
        return f"{self.codigo:<7} {self.nombre:<22} ${self.precio:>8.2f} stock: {self.stock:>4}"

    def __repr__(self) -> str:
        return f"Producto(codigo='{self.codigo}', nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"

    @classmethod
    def desde_fila_csv(cls, fila: dict) -> 'Producto':
        """Crea una instancia de Producto desde un diccionario leído del CSV."""
        return cls(
            codigo=fila["codigo"],
            nombre=fila["nombre"],
            categoria=fila["categoria"],
            precio=float(fila["precio"]),
            stock=int(fila["stock"]),
            stock_minimo=int(fila["stock_minimo"])
        )

    def a_diccionario(self) -> dict:
        """Convierte el producto a un diccionario para guardarlo en CSV."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo
        }


@dataclass(frozen=True)
class Venta:
    """Registro inmutable de una venta realizada."""
    fecha: datetime
    codigo_producto: str
    cantidad: int
    total: float

    def a_linea_txt(self) -> str:
        """Devuelve el formato de texto para guardar en ventas.txt."""
        fecha_str = self.fecha.strftime("%Y-%m-%d %H:%M:%S")
        return f"{fecha_str},{self.codigo_producto},{self.cantidad},{self.total:.2f}\n"
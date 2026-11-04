"""
Módulo de la clase Inventario.
"""
from typing import List
from .modelos import Producto
from .excepciones import ProductoNoEncontradoError

class Inventario:
    """Gestiona la colección de productos de la almacenadora."""

    def __init__(self):
        """Inicializa un inventario vacío."""
        self._productos: dict[str, Producto] = {}

    def agregar(self, producto: Producto) -> None:
        """Agrega un producto al inventario. Lanza error si el código ya existe."""
        if producto.codigo in self._productos:
            raise ValueError(f"El producto con código {producto.codigo} ya existe.")
        self._productos[producto.codigo] = producto

    def buscar(self, criterio: str) -> List[Producto]:
        """Busca por código exacto o por coincidencia parcial en el nombre."""
        criterio = criterio.strip().lower()
        resultados = []
        for prod in self._productos.values():
            if prod.codigo.lower() == criterio or criterio in prod.nombre.lower():
                resultados.append(prod)
        return resultados

    def obtener_por_codigo(self, codigo: str) -> Producto:
        """Devuelve un producto por su código o lanza ProductoNoEncontradoError."""
        codigo = codigo.strip().upper()
        if codigo not in self._productos:
            raise ProductoNoEncontradoError(f"No existe un producto con el código {codigo}.")
        return self._productos[codigo]

    def obtener_ordenados_por_nombre(self) -> List[Producto]:
        """Retorna los productos ordenados alfabéticamente por nombre."""
        return sorted(self._productos.values(), key=lambda p: p.nombre)

    def obtener_ordenados_por_precio(self) -> List[Producto]:
        """Retorna los productos ordenados por precio de mayor a menor."""
        return sorted(self._productos.values(), key=lambda p: p.precio, reverse=True)

    def obtener_categorias(self) -> set[str]:
        """Retorna un set con las categorías únicas."""
        return {prod.categoria for prod in self._productos.values()}

    def __len__(self) -> int:
        """Permite usar len(inventario)."""
        return len(self._productos)

    def __contains__(self, codigo: str) -> bool:
        """Permite usar 'MP001' in inventario."""
        return codigo.strip().upper() in self._productos

    def __iter__(self):
        """Permite iterar sobre los productos (for p in inventario)."""
        return iter(self._productos.values())
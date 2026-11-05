"""
Módulo de la interfaz de consola y coordinación del sistema.
"""
from datetime import datetime
from .inventario import Inventario
from .persistencia import RepositorioCSV, Bitacora
from .reglas import AlertaStockMinimo
from .modelos import Producto, Venta
from .reportes import ReporteVentas
from .excepciones import InventarioError

class SistemaInventario:
    """Coordina todas las clases y maneja el menú de consola."""

    def __init__(self, ruta_inventario: str):
        self.repo = RepositorioCSV(ruta_inventario, "ventas.txt")
        self.bitacora = Bitacora("bitacora.log")
        self.inventario = self.repo.cargar_inventario()
        
        # Aquí aplicamos POLIMORFISMO: el sistema usará esta regla sin saber exactamente qué subclase es
        self.regla_stock = AlertaStockMinimo()
        
        self.bitacora.registrar("Se cargó el inventario en el sistema")

    def ejecutar(self):
        """Inicia el bucle principal del menú."""
        while True:
            print("\n===== ALMACENADORA DE MATERIA PRIMA =====")
            print("1. Agregar producto")
            print("2. Buscar producto")
            print("3. Registrar venta")
            print("4. Mostrar inventario (2 criterios)")
            print("5. Reporte del día")
            print("6. Ver categorías únicas")
            print("7. Salir")
            opcion = input("Elige una opción: ")

            try:
                if opcion == "1": self._agregar_producto()
                elif opcion == "2": self._buscar_producto()
                elif opcion == "3": self._registrar_venta()
                elif opcion == "4": self._mostrar_inventario()
                elif opcion == "5": self._reporte_dia()
                elif opcion == "6": self._mostrar_categorias()
                elif opcion == "7":
                    self.repo.guardar_inventario(self.inventario)
                    self.bitacora.registrar("Se cerró el programa")
                    print("Adiós")
                    break
                else:
                    print("Opción inválida.")
            except InventarioError as e:
                # CAPTURAMOS NUESTRAS EXCEPCIONES AQUÍ
                print(f"\n[ERROR DEL SISTEMA]: {e}")
            except ValueError as e:
                print(f"\n[ERROR DE DATO]: {e}")
            except Exception as e:
                print(f"\n[ERROR INESPERADO]: {e}")

    def _agregar_producto(self):
        print("\n--- Agregar producto ---")
        codigo = input("Código (tipo MP001): ")
        nombre = input("Nombre: ")
        categoria = input("Categoría: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        minimo = int(input("Stock mínimo: "))

        nuevo = Producto(codigo, nombre, categoria, precio, stock, minimo)
        self.inventario.agregar(nuevo)
        self.repo.guardar_inventario(self.inventario)
        self.bitacora.registrar(f"Se agregó el producto {nuevo.codigo}")
        print("Producto agregado exitosamente.")

    def _buscar_producto(self):
        print("\n--- Buscar producto ---")
        criterio = input("Escribe código o parte del nombre: ")
        resultados = self.inventario.buscar(criterio)
        if not resultados:
            print("No se encontraron productos.")
            return
        for prod in resultados:
            print(prod)

    def _registrar_venta(self):
        print("\n--- Registrar venta ---")
        codigo = input("Código del producto: ")
        producto = self.inventario.obtener_por_codigo(codigo) # Lanza excepción si no existe
        
        cantidad = int(input(f"Cantidad a vender (stock: {producto.stock}): "))
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if cantidad > producto.stock:
            raise InventarioError(f"No hay suficiente stock. Solo quedan {producto.stock}.")

        total = producto.precio * cantidad
        producto.descontar_stock(cantidad)
        
        venta = Venta(datetime.now(), producto.codigo, cantidad, total)
        self.repo.guardar_venta(venta)
        self.repo.guardar_inventario(self.inventario)
        self.bitacora.registrar(f"Venta de {producto.codigo}")
        
        print(f"Venta exitosa: {cantidad} x {producto.nombre} = ${total:.2f}")

        # POLIMORFISMO EN ACCIÓN: llamamos al método evaluar() sin usar isinstance()
        alerta = self.regla_stock.evaluar(producto)
        if alerta:
            print(alerta)

    def _mostrar_inventario(self):
        if len(self.inventario) == 0:
            print("Inventario vacío.")
            return

        print("\n--- Ordenado por nombre ---")
        for prod in self.inventario.obtener_ordenados_por_nombre():
            alerta = " *** STOCK BAJO ***" if prod.stock <= prod.stock_minimo else ""
            print(f"{prod}{alerta}")

        print("\n--- Ordenado por precio (mayor a menor) ---")
        for prod in self.inventario.obtener_ordenados_por_precio():
            alerta = " *** STOCK BAJO ***" if prod.stock <= prod.stock_minimo else ""
            print(f"{prod}{alerta}")

    def _reporte_dia(self):
        ventas = self.repo.cargar_ventas()
        print(ReporteVentas.generar(ventas))

    def _mostrar_categorias(self):
        categorias = self.inventario.obtener_categorias()
        print("\n--- Categorías Únicas ---")
        for cat in sorted(categorias):
            print(f"- {cat}")
        print(f"Total: {len(categorias)} categorías.")
from inventario.app import SistemaInventario

if __name__ == "__main__":
    sistema = SistemaInventario("datos/productos.csv")
    sistema.ejecutar()
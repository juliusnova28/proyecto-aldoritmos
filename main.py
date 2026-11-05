from inventario.app import SistemaInventario

if __name__ == "__main__":
    sistema = SistemaInventario("productos.csv")
    sistema.ejecutar()
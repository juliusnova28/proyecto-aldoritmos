

import operaciones as op
from datetime import datetime


def validar_codigo(codigo):
    codigo = codigo.strip().upper()
    if len(codigo) != 5:
        return False
    if not codigo[0:2].isalpha():
        return False
    if not codigo[2:5].isdigit():
        return False
    return True



def normalizar(texto):
    return texto.strip().title()



def agregar_producto(inventario):
    print("\n--- Agregar producto ---")
    codigo = input("Codigo (tipo MP001): ")

    if not validar_codigo(codigo):
        print("El codigo esta mal, debe ser tipo MP001")
        return

    codigo = codigo.upper()

    
    for producto in inventario:
        if producto["codigo"] == codigo:
            print("Ese codigo ya existe")
            return

    try:
        nombre = normalizar(input("Nombre: "))
        categoria = normalizar(input("Categoria: "))
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        minimo = int(input("Stock minimo: "))

        nuevo = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "stock": stock,
            "stock_minimo": minimo
        }

        inventario.append(nuevo)
        op.guardar_inventario(inventario)
        op.registrar_bitacora("Se agrego el producto " + codigo)
        print("Listo, producto agregado")

    except:
        print("Error, el precio y el stock tienen que ser numeros")



def buscar_producto(inventario):
    print("\n--- Buscar producto ---")
    buscar = input("Escribe el codigo o parte del nombre: ")
    buscar = buscar.strip().lower()

    encontrados = []
    for producto in inventario:
        if producto["codigo"].lower() == buscar:
            encontrados.append(producto)
        elif buscar in producto["nombre"].lower():
            encontrados.append(producto)

    if len(encontrados) == 0:
        print("No se encontro nada")
        return

    print("")
    for producto in encontrados:
        print(producto["codigo"], "|", producto["nombre"], "| $",
              producto["precio"], "| stock:", producto["stock"])



def mostrar_inventario(inventario):
    if len(inventario) == 0:
        print("El inventario esta vacio")
        return

    
    print("\n--- Ordenado por nombre ---")
    ordenado = sorted(inventario, key=lambda x: x["nombre"])
    for producto in ordenado:
        alerta = ""
        if producto["stock"] <= producto["stock_minimo"]:
            alerta = "  *** STOCK BAJO ***"
        print(f"{producto['codigo']:<7} {producto['nombre']:<22} ${producto['precio']:>8.2f} stock: {producto['stock']:>4}{alerta}")

    
    print("\n--- Ordenado por precio (mayor a menor) ---")
    ordenado2 = sorted(inventario, key=lambda x: x["precio"], reverse=True)
    for producto in ordenado2:
        alerta = ""
        if producto["stock"] <= producto["stock_minimo"]:
            alerta = "  *** STOCK BAJO ***"
        print(f"{producto['codigo']:<7} {producto['nombre']:<22} ${producto['precio']:>8.2f} stock: {producto['stock']:>4}{alerta}")



def mostrar_categorias(inventario):
    categorias = set()
    for producto in inventario:
        categorias.add(producto["categoria"])

    print("\n--- Categorias ---")
    for categoria in sorted(categorias):
        print("-", categoria)



def registrar_venta(inventario):
    print("\n--- Registrar venta ---")
    codigo = input("Codigo del producto: ").strip().upper()

    producto = None
    for p in inventario:
        if p["codigo"] == codigo:
            producto = p
            break

    if producto == None:
        print("No existe ese producto")
        return

    try:
        cantidad = int(input("Cantidad a vender (hay " + str(producto["stock"]) + "): "))

        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0")
            return

        if cantidad > producto["stock"]:
            print("No hay suficiente stock, solo hay", producto["stock"])
            return

        # descuento el stock
        producto["stock"] = producto["stock"] - cantidad
        total = producto["precio"] * cantidad

        
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        venta = (fecha, codigo, cantidad, total)

        op.guardar_venta(venta)
        op.guardar_inventario(inventario)
        op.registrar_bitacora("Venta de " + codigo)

        print("Venta hecha:", cantidad, "x", producto["nombre"], "= $", round(total, 2))

        #REGLA DE NEGOCIO: reviso si queda con stock bajo
        if producto["stock"] <= producto["stock_minimo"]:
            print(">>> ALERTA: queda con stock bajo!")
            print("    stock actual:", producto["stock"], "| minimo:", producto["stock_minimo"])

    except:
        print("Error, la cantidad tiene que ser un numero")



def reporte_del_dia():
    print("\n--- Reporte de ventas del dia ---")
    ventas = op.cargar_ventas()
    hoy = datetime.now().strftime("%Y-%m-%d")

    ventas_hoy = []
    for venta in ventas:
        if venta[0].startswith(hoy):
            ventas_hoy.append(venta)

    if len(ventas_hoy) == 0:
        print("No hay ventas hoy")
        return

    print(f"{'Fecha':<21}{'Codigo':<9}{'Cant':>6}{'Total':>10}")
    print("-" * 46)

    total_dia = 0
    for venta in ventas_hoy:
        fecha = venta[0]
        codigo = venta[1]
        cantidad = venta[2]
        total = venta[3]
        print(f"{fecha:<21}{codigo:<9}{cantidad:>6}{total:>10.2f}")
        total_dia = total_dia + total

    print("-" * 46)
    print(f"{'Total del dia':<36}{total_dia:>10.2f}")


def menu():
    inventario = op.cargar_inventario()

    while True:
        print("\n===== ALMACENADORA DE MATERIA PRIMA =====")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Registrar venta")
        print("4. Mostrar inventario")
        print("5. Reporte del dia")
        print("6. Ver categorias")
        print("7. Salir")
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            agregar_producto(inventario)
        elif opcion == "2":
            buscar_producto(inventario)
        elif opcion == "3":
            registrar_venta(inventario)
        elif opcion == "4":
            mostrar_inventario(inventario)
        elif opcion == "5":
            reporte_del_dia()
        elif opcion == "6":
            mostrar_categorias(inventario)
        elif opcion == "7":
            op.guardar_inventario(inventario)
            op.registrar_bitacora("Se cerro el programa")
            print("Adios")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    menu()
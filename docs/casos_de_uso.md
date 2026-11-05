usecaseDiagram
    actor Vendedor
    actor Sistema as "Sistema de Archivos"
    
    package "Almacenadora de Materia Prima" {
        usecase "Agregar Producto" as UC1
        usecase "Buscar Producto" as UC2
        usecase "Registrar Venta" as UC3
        usecase "Validar Stock" as UC4
        usecase "Aplicar Alerta de Stock Mínimo" as UC5
        usecase "Mostrar Inventario" as UC6
        usecase "Generar Reporte del Día" as UC7
        usecase "Ver Categorías" as UC8
        usecase "Guardar / Cargar Datos" as UC9
    }

    Vendedor --> UC1
    Vendedor --> UC2
    Vendedor --> UC3
    Vendedor --> UC6
    Vendedor --> UC7
    Vendedor --> UC8
    
    UC3 .> UC4 : <<include>>
    UC4 <.. UC5 : <<extend>>
    
    UC1 --> UC9
    UC3 --> UC9
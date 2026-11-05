**1. ¿Qué cambió entre el Proyecto 1 y el Proyecto Final?**
En el Proyecto 1, toda la lógica estaba centralizada en funciones y diccionarios dentro de un solo archivo. En el Proyecto Final, migré a un diseño orientado a objetos. La ventaja concreta más grande fue la organización: ahora cada clase tiene una única responsabilidad, lo que hace que el código sea mucho más fácil de leer, mantener y escalar. Ya no hay variables globales ni "funciones sueltas".

**2. ¿Cómo decidí qué clases crear y qué responsabilidad tiene cada una?**
se Analico el problema y se separo las entidades de la lógica:
- `Producto` y `Venta` son mis modelos de datos.
- `Inventario` maneja la colección y búsquedas.
- `RepositorioCSV` y `Bitacora` se encargan exclusivamente de los archivos (persistencia).
- `ReporteVentas` formatea la salida.
- `SistemaInventario` es el cerebro que coordina todo y muestra el menú.

**3. ¿Dónde apliqué herencia y polimorfismo?**
Apliqué herencia en la jerarquía de excepciones (todas heredan de `InventarioError`) y en la regla de negocio. Creé una clase abstracta `ReglaNegocio` y una subclase `AlertaStockMinimo`. El polimorfismo ocurre en el método `ejecutar()` del sistema, donde se llama a `self.regla_stock.evaluar(producto)` sin importar el tipo específico de regla; esto permite agregar nuevas reglas en el futuro sin modificar el código existente (Principio Abierto/Cerrado).

**4. La parte más difícil de la refactorización y cómo se puedo resolver**
Lo más difícil fue el buscar informacion de como migrar la lógica de archivos y el manejo de errores. En el P1, si el usuario ingresaba un dato malo, el programa a veces fallaba. Lo resolvio encapsulando las validaciones en los *setters* de `Producto` (usando `@property`) y creando excepciones personalizadas. Ahora la interfaz (`app.py`) atrapa estos errores con `try/except` y muestra mensajes amigables, evitando que el programa se cierre abruptamente.

**5. Declaración de uso de herramientas de IA**
Declaro que utilicé herramientas de Inteligencia Artificial (como DeepSeek y Gemini) como apoyo para estructurar el código, comprender conceptos avanzados de POO (como los métodos especiales y el polimorfismo) y generar la sintaxis de los diagramas UML en Mermaid. Todo el código entregado ha sido revisado y comprendido por mí para poder defenderlo en la evaluación.
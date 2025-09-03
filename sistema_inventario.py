class ProductoError(Exception):
    """Excepción personalizada para errores relacionados con productos"""
    pass

class InventarioError(Exception):
    """Excepción personalizada para errores relacionados con el inventario"""
    pass

class Producto:
    
    def __init__(self, nombre, precio, cantidad):
        self._validar_nombre(nombre)
        self._validar_precio(precio)
        self._validar_cantidad(cantidad)
        
        self.nombre = nombre.strip().title()
        self.precio = float(precio)
        self.cantidad = int(cantidad)
    
    def _validar_nombre(self, nombre):
        if not isinstance(nombre, str):
            raise ProductoError("El nombre debe ser una cadena de texto")
        
        if not nombre or not nombre.strip():
            raise ProductoError("El nombre del producto no puede estar vacío")
        
        if len(nombre.strip()) < 2:
            raise ProductoError("El nombre del producto debe tener al menos 2 caracteres")
    
    def _validar_precio(self, precio):
        try:
            precio_float = float(precio)
        except (ValueError, TypeError):
            raise ProductoError("El precio debe ser un número válido")
        
        if precio_float < 0:
            raise ProductoError("El precio no puede ser negativo")
    
    def _validar_cantidad(self, cantidad):
        try:
            cantidad_int = int(cantidad)
        except (ValueError, TypeError):
            raise ProductoError("La cantidad debe ser un número entero válido")
        
        if cantidad_int < 0:
            raise ProductoError("La cantidad no puede ser negativa")
    
    def actualizar_precio(self, nuevo_precio):
        self._validar_precio(nuevo_precio)
        precio_anterior = self.precio
        self.precio = float(nuevo_precio)
        print(f"✅ Precio actualizado de ${precio_anterior:.2f} a ${self.precio:.2f}")
    
    def actualizar_cantidad(self, nueva_cantidad):
        self._validar_cantidad(nueva_cantidad)
        cantidad_anterior = self.cantidad
        self.cantidad = int(nueva_cantidad)
        print(f"✅ Cantidad actualizada de {cantidad_anterior} a {self.cantidad} unidades")
    
    def calcular_valor_total(self):
        return self.precio * self.cantidad
    
    def agregar_stock(self, cantidad_agregar):
        self._validar_cantidad(cantidad_agregar)
        if cantidad_agregar <= 0:
            raise ProductoError("La cantidad a agregar debe ser mayor a cero")
        
        self.cantidad += int(cantidad_agregar)
        print(f"✅ Se agregaron {cantidad_agregar} unidades. Stock actual: {self.cantidad}")
    
    def reducir_stock(self, cantidad_reducir):
        self._validar_cantidad(cantidad_reducir)
        cantidad_reducir = int(cantidad_reducir)
        
        if cantidad_reducir <= 0:
            raise ProductoError("La cantidad a reducir debe ser mayor a cero")
        
        if cantidad_reducir > self.cantidad:
            raise ProductoError(f"No hay suficiente stock. Disponible: {self.cantidad}, Solicitado: {cantidad_reducir}")
        
        self.cantidad -= cantidad_reducir
        print(f"✅ Se redujeron {cantidad_reducir} unidades. Stock actual: {self.cantidad}")
    
    def __str__(self):
        valor_total = self.calcular_valor_total()
        estado_stock = "⚠️  STOCK BAJO" if self.cantidad <= 5 else "✅ En stock"
        
        return (f"📦 {self.nombre}\n"
                f"   💰 Precio: ${self.precio:.2f}\n"
                f"   📊 Cantidad: {self.cantidad} unidades\n"
                f"   💵 Valor Total: ${valor_total:.2f}\n"
                f"   📈 Estado: {estado_stock}")
    
    def __repr__(self):
        return f"Producto('{self.nombre}', {self.precio}, {self.cantidad})"

class Inventario:
    
    def __init__(self):
        self.productos = []
        print("🏪 Nuevo inventario creado exitosamente")
    
    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise InventarioError("El objeto debe ser una instancia de la clase Producto")
        
        # Verificar si el producto ya existe
        producto_existente = self.buscar_producto(producto.nombre)
        if producto_existente:
            respuesta = input(f"⚠️  El producto '{producto.nombre}' ya existe. ¿Desea agregar al stock existente? (s/n): ").lower().strip()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                producto_existente.agregar_stock(producto.cantidad)
                return
            else:
                print("❌ Operación cancelada")
                return
        
        self.productos.append(producto)
        print(f"✅ Producto '{producto.nombre}' agregado al inventario exitosamente")
    
    def buscar_producto(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise InventarioError("El nombre del producto debe ser una cadena válida")
        
        nombre_buscar = nombre.strip().title()
        
        for producto in self.productos:
            if producto.nombre == nombre_buscar:
                return producto
        
        return None
    
    def buscar_productos_por_patron(self, patron):
        if not isinstance(patron, str) or not patron.strip():
            return []
        
        patron_buscar = patron.strip().lower()
        productos_encontrados = []
        
        for producto in self.productos:
            if patron_buscar in producto.nombre.lower():
                productos_encontrados.append(producto)
        
        return productos_encontrados
    
    def eliminar_producto(self, nombre):
        producto = self.buscar_producto(nombre)
        if producto:
            self.productos.remove(producto)
            print(f"✅ Producto '{nombre}' eliminado del inventario")
            return True
        else:
            print(f"❌ Producto '{nombre}' no encontrado")
            return False
    
    def calcular_valor_inventario(self):
        valor_total = sum(producto.calcular_valor_total() for producto in self.productos)
        return valor_total
    
    def listar_productos(self):
        if not self.productos:
            print("📦 El inventario está vacío")
            return
        
        print(f"\n{'='*50}")
        print(f"           📋 LISTADO DE PRODUCTOS ({len(self.productos)})")
        print(f"{'='*50}")
        
        for i, producto in enumerate(self.productos, 1):
            print(f"\n{i}. {producto}")
            print("-" * 40)
        
        valor_total = self.calcular_valor_inventario()
        print(f"\n💰 VALOR TOTAL DEL INVENTARIO: ${valor_total:.2f}")
    
    def obtener_productos_bajo_stock(self, limite=5):
        productos_bajo_stock = [p for p in self.productos if p.cantidad <= limite]
        return productos_bajo_stock
    
    def generar_reporte_inventario(self):
        print(f"\n{'='*60}")
        print(f"                📊 REPORTE DE INVENTARIO")
        print(f"{'='*60}")
        
        if not self.productos:
            print("📦 El inventario está vacío")
            return
        
        # Estadísticas generales
        total_productos = len(self.productos)
        valor_total = self.calcular_valor_inventario()
        total_unidades = sum(p.cantidad for p in self.productos)
        precio_promedio = sum(p.precio for p in self.productos) / total_productos
        
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   • Total de productos únicos: {total_productos}")
        print(f"   • Total de unidades: {total_unidades}")
        print(f"   • Valor total del inventario: ${valor_total:.2f}")
        print(f"   • Precio promedio: ${precio_promedio:.2f}")
        
        # Producto más caro y más barato
        producto_mas_caro = max(self.productos, key=lambda p: p.precio)
        producto_mas_barato = min(self.productos, key=lambda p: p.precio)
        
        print(f"\n💎 PRODUCTOS DESTACADOS:")
        print(f"   • Más caro: {producto_mas_caro.nombre} (${producto_mas_caro.precio:.2f})")
        print(f"   • Más barato: {producto_mas_barato.nombre} (${producto_mas_barato.precio:.2f})")
        
        # Productos con mayor y menor valor total
        producto_mayor_valor = max(self.productos, key=lambda p: p.calcular_valor_total())
        producto_menor_valor = min(self.productos, key=lambda p: p.calcular_valor_total())
        
        print(f"   • Mayor valor total: {producto_mayor_valor.nombre} (${producto_mayor_valor.calcular_valor_total():.2f})")
        print(f"   • Menor valor total: {producto_menor_valor.nombre} (${producto_menor_valor.calcular_valor_total():.2f})")
        
        # Productos con stock bajo
        productos_bajo_stock = self.obtener_productos_bajo_stock()
        if productos_bajo_stock:
            print(f"\n⚠️  PRODUCTOS CON STOCK BAJO ({len(productos_bajo_stock)}):")
            for producto in productos_bajo_stock:
                print(f"   • {producto.nombre}: {producto.cantidad} unidades")
        else:
            print(f"\n✅ Todos los productos tienen stock adecuado")
    
    def __len__(self):
        return len(self.productos)
    
    def __str__(self):
        if not self.productos:
            return "📦 Inventario vacío"
        
        valor_total = self.calcular_valor_inventario()
        return f"🏪 Inventario con {len(self.productos)} productos (Valor: ${valor_total:.2f})"

def solicitar_datos_producto():
    print("\n📝 AGREGAR NUEVO PRODUCTO")
    print("-" * 30)
    
    while True:
        try:
            nombre = input("Nombre del producto: ").strip()
            precio = input("Precio unitario ($): ").strip()
            cantidad = input("Cantidad inicial: ").strip()
            
            producto = Producto(nombre, precio, cantidad)
            return producto
            
        except ProductoError as e:
            print(f"❌ Error: {e}")
            print("Por favor, intente nuevamente.\n")

def menu_buscar_producto(inventario):
    print("\n🔍 BUSCAR PRODUCTO")
    print("-" * 20)
    print("1. Buscar por nombre exacto")
    print("2. Buscar por patrón")
    print("0. Volver al menú principal")
    
    while True:
        try:
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                break
            elif opcion == "1":
                nombre = input("Ingrese el nombre del producto: ").strip()
                if nombre:
                    producto = inventario.buscar_producto(nombre)
                    if producto:
                        print(f"\n✅ PRODUCTO ENCONTRADO:")
                        print(producto)
                    else:
                        print(f"❌ No se encontró el producto '{nombre}'")
                break
                
            elif opcion == "2":
                patron = input("Ingrese el patrón de búsqueda: ").strip()
                if patron:
                    productos = inventario.buscar_productos_por_patron(patron)
                    if productos:
                        print(f"\n✅ SE ENCONTRARON {len(productos)} PRODUCTO(S):")
                        for i, producto in enumerate(productos, 1):
                            print(f"\n{i}. {producto}")
                    else:
                        print(f"❌ No se encontraron productos que contengan '{patron}'")
                break
                
            else:
                print("❌ Opción no válida. Intente nuevamente.")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def menu_gestionar_stock(inventario):
    if len(inventario) == 0:
        print("❌ No hay productos en el inventario")
        return
    
    print("\n📦 GESTIONAR STOCK")
    print("-" * 20)
    
    nombre = input("Nombre del producto: ").strip()
    producto = inventario.buscar_producto(nombre)
    
    if not producto:
        print(f"❌ Producto '{nombre}' no encontrado")
        return
    
    print(f"\n📊 PRODUCTO ACTUAL:")
    print(producto)
    
    print(f"\n¿Qué desea hacer?")
    print("1. Agregar stock")
    print("2. Reducir stock")
    print("3. Actualizar precio")
    print("0. Volver")
    
    while True:
        try:
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                break
            elif opcion == "1":
                cantidad = input("Cantidad a agregar: ").strip()
                producto.agregar_stock(cantidad)
                break
            elif opcion == "2":
                cantidad = input("Cantidad a reducir: ").strip()
                producto.reducir_stock(cantidad)
                break
            elif opcion == "3":
                precio = input("Nuevo precio: ").strip()
                producto.actualizar_precio(precio)
                break
            else:
                print("❌ Opción no válida")
                
        except (ProductoError, ValueError) as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

def menu_principal():
    inventario = Inventario()
    
    # Datos de ejemplo para testing
    try:
        productos_ejemplo = [
            Producto("Laptop Dell", 899.99, 5),
            Producto("Mouse Inalámbrico", 25.50, 20),
            Producto("Teclado Mecánico", 75.00, 8),
            Producto("Monitor 24 Pulgadas", 199.99, 3),
            Producto("Auriculares Bluetooth", 45.99, 15)
        ]
        
        print("\n🔄 Cargando datos de ejemplo...")
        for producto in productos_ejemplo:
            inventario.productos.append(producto)
        print("✅ Datos de ejemplo cargados exitosamente")
        
    except Exception as e:
        print(f"⚠️  Error al cargar datos de ejemplo: {e}")
    
    while True:
        try:
            print(f"\n{'='*50}")
            print(f"           🏪 SISTEMA DE INVENTARIO")
            print(f"{'='*50}")
            print(f"Estado actual: {inventario}")
            print(f"\n📋 OPCIONES DISPONIBLES:")
            print("1. 📦 Agregar producto")
            print("2. 🔍 Buscar producto")
            print("3. 📊 Listar todos los productos")
            print("4. 📈 Generar reporte completo")
            print("5. 🔧 Gestionar stock")
            print("6. 🗑️  Eliminar producto")
            print("7. ⚠️  Ver productos con stock bajo")
            print("0. 🚪 Salir")
            
            opcion = input("\n👉 Seleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Gracias por usar el Sistema de Inventario!")
                print("🔒 Cerrando aplicación...")
                break
                
            elif opcion == "1":
                try:
                    producto = solicitar_datos_producto()
                    inventario.agregar_producto(producto)
                except ProductoError as e:
                    print(f"❌ No se pudo agregar el producto: {e}")
                    
            elif opcion == "2":
                menu_buscar_producto(inventario)
                
            elif opcion == "3":
                inventario.listar_productos()
                
            elif opcion == "4":
                inventario.generar_reporte_inventario()
                
            elif opcion == "5":
                menu_gestionar_stock(inventario)
                
            elif opcion == "6":
                if len(inventario) == 0:
                    print("❌ No hay productos para eliminar")
                else:
                    nombre = input("Nombre del producto a eliminar: ").strip()
                    if nombre:
                        inventario.eliminar_producto(nombre)
                        
            elif opcion == "7":
                productos_bajo_stock = inventario.obtener_productos_bajo_stock()
                if productos_bajo_stock:
                    print(f"\n⚠️  PRODUCTOS CON STOCK BAJO ({len(productos_bajo_stock)}):")
                    for producto in productos_bajo_stock:
                        print(f"\n{producto}")
                else:
                    print("✅ Todos los productos tienen stock adecuado")
                    
            else:
                print("❌ Opción no válida. Por favor, seleccione una opción del 0 al 7.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación interrumpida por el usuario")
            print("👋 ¡Hasta luego!")
            break
            
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("🔄 Continuando con la ejecución...")
        
        # Pausa para que el usuario pueda leer los mensajes
        input("\n⏸️  Presione Enter para continuar...")

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Inventario...")
    menu_principal()

import sqlite3

DB_PATH = 'database/app.db'

def obtener_conexion():
    """Establece la conexión con la base de datos y activa claves foráneas."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

# ==========================================
# FUNCIONES DE CLIENTES
# ==========================================

def crear_cliente(nombre, telefono, email, direccion):
    """Registra un nuevo cliente."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nombre, telefono, email, direccion)
        VALUES (?, ?, ?, ?)
    """, (nombre, telefono, email, direccion))
    conn.commit()
    id_creado = cursor.lastrowid
    conn.close()
    return id_creado

def obtener_clientes():
    """Retorna la lista de todos los clientes."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return clientes

# ==========================================
# FUNCIONES DE INVENTARIO
# ==========================================

def agregar_articulo(id_categoria, nombre, stock_total, precio_renta_dia, costo_reposicion, descripcion=""):
    """Agrega un nuevo producto/mobiliario al inventario."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventario (id_categoria, nombre, descripcion, stock_total, precio_renta_dia, costo_reposicion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_categoria, nombre, descripcion, stock_total, precio_renta_dia, costo_reposicion))
    conn.commit()
    id_articulo = cursor.lastrowid
    conn.close()
    return id_articulo

def obtener_inventario():
    """Consulta los artículos disponibles con el nombre de su categoría."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id_articulo, i.nombre, i.stock_total, i.precio_renta_dia, c.nombre AS categoria
        FROM inventario i
        JOIN categorias c ON i.id_categoria = c.id_categoria
    """)
    articulos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articulos

# ==========================================
# FUNCIONES DE PEDIDOS
# ==========================================

def crear_pedido(id_cliente, fecha_inicio, fecha_fin, direccion, total, anticipo, notas=""):
    """Registra una nueva solicitud de renta/pedido."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos (id_cliente, fecha_evento_inicio, fecha_evento_fin, direccion_evento, monto_total, monto_anticipo, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_cliente, fecha_inicio, fecha_fin, direccion, total, anticipo, notas))
    conn.commit()
    id_pedido = cursor.lastrowid
    conn.close()
    return id_pedido

def cancelar_pedido(id_pedido):
    """Cancela un pedido existente."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id_pedido = ?", (id_pedido,))
    conn.commit()
    conn.close()
    
def obtener_pedidos():
    """Retorna la lista de todos los pedidos con información del cliente."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_pedido, c.nombre AS cliente, p.fecha_evento_inicio, p.fecha_evento_fin, p.direccion_evento, p.monto_total, p.monto_anticipo, p.notas
        FROM pedidos p
        JOIN clientes c ON p.id_cliente = c.id_cliente
    """)
    pedidos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return pedidos

def editar_pedido(id_pedido, fecha_inicio=None, fecha_fin=None, direccion=None, total=None, anticipo=None, notas=None):
    """Edita los detalles de un pedido existente."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Construir la consulta de actualización dinámicamente
    campos_a_actualizar = []
    valores = []
    
    if fecha_inicio is not None:
        campos_a_actualizar.append("fecha_evento_inicio = ?")
        valores.append(fecha_inicio)
    if fecha_fin is not None:
        campos_a_actualizar.append("fecha_evento_fin = ?")
        valores.append(fecha_fin)
    if direccion is not None:
        campos_a_actualizar.append("direccion_evento = ?")
        valores.append(direccion)
    if total is not None:
        campos_a_actualizar.append("monto_total = ?")
        valores.append(total)
    if anticipo is not None:
        campos_a_actualizar.append("monto_anticipo = ?")
        valores.append(anticipo)
    if notas is not None:
        campos_a_actualizar.append("notas = ?")
        valores.append(notas)
    
    if campos_a_actualizar:
        consulta = f"UPDATE pedidos SET {', '.join(campos_a_actualizar)} WHERE id_pedido = ?"
        valores.append(id_pedido)
        cursor.execute(consulta, tuple(valores))
        conn.commit()
    
    conn.close()
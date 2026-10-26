



-- 1. TABLA DE CLIENTES
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT UNIQUE,
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- 2. TABLA DE CATEGORÍAS

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);


-- 3. TABLA DE INVENTARIO / ARTÍCULOS

CREATE TABLE IF NOT EXISTS inventario (
    id_articulo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    stock_total INTEGER NOT NULL CHECK (stock_total >= 0),
    precio_renta_dia REAL NOT NULL CHECK (precio_renta_dia >= 0),
    costo_reposicion REAL DEFAULT 0.0 CHECK (costo_reposicion >= 0),
    FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria) ON DELETE RESTRICT
);


-- 4. TABLA DE PEDIDOS / EVENTOS
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_evento_inicio DATE NOT NULL,
    fecha_evento_fin DATE NOT NULL,
    direccion_evento TEXT NOT NULL,
    monto_total REAL DEFAULT 0.0 CHECK (monto_total >= 0),
    monto_anticipo REAL DEFAULT 0.0 CHECK (monto_anticipo >= 0),
    estado TEXT DEFAULT 'pendiente' CHECK (
        estado IN ('pendiente', 'confirmado', 'entregado', 'completado', 'cancelado')
    ),
    notas TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE RESTRICT,
    CHECK (fecha_evento_fin >= fecha_evento_inicio)
);


-- 5. TABLA DETALLE DEL PEDIDO (Mobiliario Rentado)

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    id_articulo INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),
    subtotal REAL GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (id_pedido) REFERENCES pedidos (id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_articulo) REFERENCES inventario (id_articulo) ON DELETE RESTRICT
);

-- 6. TABLA DE PAGOS / ABONOS
CREATE TABLE IF NOT EXISTS pagos (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    monto REAL NOT NULL CHECK (monto > 0),
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    metodo_pago TEXT NOT NULL CHECK (
        metodo_pago IN ('efectivo', 'transferencia', 'tarjeta')
    ),
    FOREIGN KEY (id_pedido) REFERENCES pedidos (id_pedido) ON DELETE CASCADE
);

-- ÍNDICES PARA OPTIMIZAR CONSULTAS

CREATE INDEX IF NOT EXISTS idx_pedidos_fechas ON pedidos(fecha_evento_inicio, fecha_evento_fin);
CREATE INDEX IF NOT EXISTS idx_pedidos_cliente ON pedidos(id_cliente);
CREATE INDEX IF NOT EXISTS idx_inventario_categoria ON inventario(id_categoria);
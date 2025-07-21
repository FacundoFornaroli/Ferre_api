USE Ferreteriadb

CREATE TABLE Categorias (
        ID_Categoria INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL UNIQUE,
        Descripcion VARCHAR(500) NULL,
        Categoria_Padre INT NULL,
        Activo BIT NOT NULL DEFAULT 1,
        Fecha_Creacion DATETIME NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_Categorias_Padre FOREIGN KEY (Categoria_Padre) REFERENCES Categorias(ID_Categoria)
    );
GO

CREATE TABLE Unidades_de_medida (
        ID_Unidad_de_medida INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(50) NOT NULL UNIQUE,
        Abreviatura VARCHAR(10) NOT NULL,
        Activo BIT NOT NULL DEFAULT 1
    );
GO

CREATE TABLE Sucursales (
        ID_Sucursal INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL UNIQUE,
        Direccion VARCHAR(200) NOT NULL,
        Telefono VARCHAR(40) NULL,
        Email VARCHAR(120) NULL,
        Localidad VARCHAR(100) NOT NULL,
        Provincia VARCHAR(50) NOT NULL,
        Codigo_Postal VARCHAR(10) NULL,
        Horario_Apertura TIME NULL,
        Horario_Cierre TIME NULL,
        Activo BIT NOT NULL DEFAULT 1,
        Fecha_Creacion DATETIME NOT NULL DEFAULT GETDATE()
    );
GO

CREATE TABLE Usuarios (
        ID_Usuario INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Apellido VARCHAR(100) NOT NULL,
        CUIL VARCHAR(13) NULL UNIQUE,
        Rol VARCHAR(50) NOT NULL,
        Email VARCHAR(120) NOT NULL UNIQUE,
        Contraseña VARCHAR(255) NOT NULL,
        ID_Sucursal INT NULL,
        Estado BIT NOT NULL DEFAULT 1,
        Ultimo_Acceso DATETIME NULL,
        Creado_el DATETIME NOT NULL DEFAULT GETDATE(),
        Actualizado_el DATETIME NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_Usuarios_Sucursal FOREIGN KEY (ID_Sucursal) REFERENCES Sucursales(ID_Sucursal)
    );
GO

CREATE TABLE Productos (
        ID_Producto INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(150) NOT NULL,
        Descripcion TEXT NULL,
        Codigo_Barras VARCHAR(50) NULL UNIQUE,
        SKU VARCHAR(20) NULL UNIQUE,
        Marca VARCHAR(100) NULL,
        Modelo VARCHAR(100) NULL,
        Precio DECIMAL(10,2) NOT NULL,
        Costo DECIMAL(10,2) NOT NULL,
        Precio_Mayorista DECIMAL(10,2) NULL,
        ID_Categoria INT NOT NULL,
        ID_Unidad_de_medida INT NOT NULL,
        Peso DECIMAL(8,2) NULL, -- en kg
        Dimensiones VARCHAR(50) NULL, -- formato: LxAxH
        Activo BIT NOT NULL DEFAULT 1,
        Fecha_Creacion DATETIME NOT NULL DEFAULT GETDATE(),
        Fecha_Actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
        CONSTRAINT FK_Productos_Categoria FOREIGN KEY (ID_Categoria) REFERENCES Categorias(ID_Categoria),
        CONSTRAINT FK_Productos_Unidad FOREIGN KEY (ID_Unidad_de_medida) REFERENCES Unidades_de_medida(ID_Unidad_de_medida),
        CONSTRAINT CK_Productos_Precio CHECK (Precio > 0),
        CONSTRAINT CK_Productos_Costo CHECK (Costo > 0)
        );
GO

CREATE TABLE Clientes (
        ID_Cliente INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(150) NOT NULL,
        Apellido VARCHAR(150) NULL,
        CUIT_CUIL VARCHAR(13) NULL UNIQUE,
        Tipo_Cliente VARCHAR(20) NOT NULL DEFAULT 'Consumidor Final', -- 'Consumidor Final', 'Responsable Inscripto', 'Monotributista'
        Condicion_IVA VARCHAR(50) NULL, -- 'IVA Responsable Inscripto', 'IVA Responsable no Inscripto', 'IVA no Responsable', 'IVA Sujeto Exento'
        Direccion VARCHAR(200) NOT NULL,
        Localidad VARCHAR(100) NOT NULL,
        Provincia VARCHAR(50) NOT NULL,
        Codigo_Postal VARCHAR(10) NULL,
        Telefono VARCHAR(40) NOT NULL,
        Telefono_Alternativo VARCHAR(40) NULL,
        Email VARCHAR(120) NULL,
        Fecha_Nacimiento DATE NULL,
        Genero CHAR(1) NULL, -- 'M', 'F', 'O'
        Fecha_Alta DATETIME NOT NULL DEFAULT GETDATE(),
        Limite_Credito DECIMAL(10,2) NOT NULL DEFAULT 0,
        Saldo_Actual DECIMAL(10,2) NOT NULL DEFAULT 0,
        Activo BIT NOT NULL DEFAULT 1,
        Observaciones TEXT NULL
    );
GO

CREATE TABLE Proveedores (
        ID_Proveedor INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(150) NOT NULL,
        CUIT VARCHAR(13) NULL UNIQUE,
        Condicion_IVA VARCHAR(50) NULL,
        Direccion VARCHAR(200) NOT NULL,
        Localidad VARCHAR(100) NOT NULL,
        Provincia VARCHAR(50) NOT NULL,
        Codigo_Postal VARCHAR(10) NULL,
        Telefono VARCHAR(40) NOT NULL,
        Telefono_Alternativo VARCHAR(40) NULL,
        Email VARCHAR(120) NULL,
        Contacto_Persona VARCHAR(100) NULL,
        Plazo_Entrega INT NULL, -- en días
        Activo BIT NOT NULL DEFAULT 1,
        Fecha_Creacion DATETIME NOT NULL DEFAULT GETDATE(),
        Observaciones TEXT NULL
    );
GO

CREATE TABLE Inventario (
        ID_Inventario INT IDENTITY(1,1) PRIMARY KEY,
        ID_Producto INT NOT NULL,
        ID_Sucursal INT NOT NULL,
        Stock_Actual INT NOT NULL DEFAULT 0,
        Stock_Minimo INT NOT NULL DEFAULT 0,
        Stock_Maximo INT NOT NULL DEFAULT 0,
        Ubicacion VARCHAR(100) NULL, -- ubicación física en la sucursal
        Fecha_Ultimo_Movimiento DATETIME NULL,
        Activo BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_Inventario_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT FK_Inventario_Sucursal FOREIGN KEY (ID_Sucursal) REFERENCES Sucursales(ID_Sucursal),
        CONSTRAINT CK_Inventario_Stock_Minimo CHECK (Stock_Minimo >= 0),
        CONSTRAINT CK_Inventario_Stock_Maximo CHECK (Stock_Maximo >= Stock_Minimo),
        CONSTRAINT UQ_Inventario_Producto_Sucursal UNIQUE (ID_Producto, ID_Sucursal)
    );
GO

CREATE TABLE Facturas_Venta (
        ID_Factura_Venta INT IDENTITY(1,1) PRIMARY KEY,
        Numero_Factura VARCHAR(20) NULL UNIQUE,
        ID_Cliente INT NOT NULL,
        ID_Sucursal INT NOT NULL,
        Fecha DATETIME NOT NULL DEFAULT GETDATE(),
        Tipo_Factura CHAR(1) NOT NULL DEFAULT 'B', -- 'A', 'B', 'C'
        Condicion_IVA VARCHAR(50) NULL,
        Subtotal DECIMAL(10,2) NOT NULL,
        IVA DECIMAL(10,2) NOT NULL DEFAULT 0,
        Descuento DECIMAL(10,2) NOT NULL DEFAULT 0,
        Total DECIMAL(10,2) NOT NULL,
        ID_Usuario INT NOT NULL,
        Estado VARCHAR(30) NOT NULL DEFAULT 'Emitida', -- 'Emitida', 'Pagada', 'Anulada', 'Pendiente'
        Forma_Pago VARCHAR(50) NULL,
        Observaciones TEXT NULL,
        CONSTRAINT FK_FacturasVenta_Cliente FOREIGN KEY (ID_Cliente) REFERENCES Clientes(ID_Cliente),
        CONSTRAINT FK_FacturasVenta_Sucursal FOREIGN KEY (ID_Sucursal) REFERENCES Sucursales(ID_Sucursal),
        CONSTRAINT FK_FacturasVenta_Usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
        CONSTRAINT CK_FacturasVenta_Total CHECK (Total > 0),
        CONSTRAINT CK_FacturasVenta_Tipo CHECK (Tipo_Factura IN ('A', 'B', 'C'))
    );
GO

CREATE TABLE Detalles_Factura_Venta (
        ID_Detalle INT IDENTITY(1,1) PRIMARY KEY,
        ID_Factura_Venta INT NOT NULL,
        ID_Producto INT NOT NULL,
        Cantidad INT NOT NULL,
        Precio_Unitario DECIMAL(10,2) NOT NULL,
        Descuento_Unitario DECIMAL(10,2) NOT NULL DEFAULT 0,
        Subtotal DECIMAL(10,2) NOT NULL,
        CONSTRAINT FK_DetallesFactura_Factura FOREIGN KEY (ID_Factura_Venta) REFERENCES Facturas_Venta(ID_Factura_Venta) ON DELETE CASCADE,
        CONSTRAINT FK_DetallesFactura_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT CK_DetallesFactura_Cantidad CHECK (Cantidad > 0),
        CONSTRAINT CK_DetallesFactura_Precio CHECK (Precio_Unitario > 0)
    );
GO

CREATE TABLE Pagos (
        ID_Pago INT IDENTITY(1,1) PRIMARY KEY,
        ID_Factura_Venta INT NOT NULL,
        Metodo VARCHAR(30) NOT NULL, -- 'Efectivo', 'Tarjeta', 'Transferencia', 'Cheque'
        Monto DECIMAL(10,2) NOT NULL,
        Numero_Comprobante VARCHAR(50) NULL,
        Fecha DATETIME NOT NULL DEFAULT GETDATE(),
        ID_Usuario INT NOT NULL,
        Observaciones TEXT NULL,
        CONSTRAINT FK_Pagos_Factura FOREIGN KEY (ID_Factura_Venta) REFERENCES Facturas_Venta(ID_Factura_Venta),
        CONSTRAINT FK_Pagos_Usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
        CONSTRAINT CK_Pagos_Monto CHECK (Monto > 0)
    );
GO

CREATE TABLE Ordenes_Compra (
        ID_OC INT IDENTITY(1,1) PRIMARY KEY,
        Numero_OC VARCHAR(20) NULL UNIQUE,
        ID_Proveedor INT NOT NULL,
        ID_Sucursal INT NOT NULL,
        Fecha DATETIME NOT NULL DEFAULT GETDATE(),
        Fecha_Entrega_Esperada DATE NULL,
        Subtotal DECIMAL(10,2) NOT NULL,
        IVA DECIMAL(10,2) NOT NULL DEFAULT 0,
        Descuento DECIMAL(10,2) NOT NULL DEFAULT 0,
        Total DECIMAL(10,2) NOT NULL,
        ID_Usuario INT NOT NULL,
        Estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente', -- 'Pendiente', 'Aprobada', 'Recibida', 'Cancelada'
        Observaciones TEXT NULL,
        CONSTRAINT FK_OrdenesCompra_Proveedor FOREIGN KEY (ID_Proveedor) REFERENCES Proveedores(ID_Proveedor),
        CONSTRAINT FK_OrdenesCompra_Sucursal FOREIGN KEY (ID_Sucursal) REFERENCES Sucursales(ID_Sucursal),
        CONSTRAINT FK_OrdenesCompra_Usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
        CONSTRAINT CK_OrdenesCompra_Total CHECK (Total > 0)
    );
GO

CREATE TABLE Detalle_OC (
        ID_Detalle_OC INT IDENTITY(1,1) PRIMARY KEY,
        ID_OC INT NOT NULL,
        ID_Producto INT NOT NULL,
        Cantidad INT NOT NULL,
        Costo_Unitario DECIMAL(10,2) NOT NULL,
        Descuento_Unitario DECIMAL(10,2) NOT NULL DEFAULT 0,
        Subtotal DECIMAL(10,2) NOT NULL,
        CONSTRAINT FK_DetalleOC_Orden FOREIGN KEY (ID_OC) REFERENCES Ordenes_Compra(ID_OC) ON DELETE CASCADE,
        CONSTRAINT FK_DetalleOC_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT CK_DetalleOC_Cantidad CHECK (Cantidad > 0),
        CONSTRAINT CK_DetalleOC_Costo CHECK (Costo_Unitario > 0)
    );
GO

CREATE TABLE Movimientos_Inventario (
        ID_Movimiento INT IDENTITY(1,1) PRIMARY KEY,
        ID_Producto INT NOT NULL,
        ID_Sucursal INT NOT NULL,
        Fecha DATETIME NOT NULL DEFAULT GETDATE(),
        Tipo VARCHAR(15) NOT NULL, -- 'Compra', 'Venta', 'Transferencia', 'Ajuste', 'Devolucion'
        Cantidad INT NOT NULL,
        Costo_Unitario DECIMAL(10,2) NULL,
        ID_Usuario INT NOT NULL,
        ID_Referencia INT NULL, -- ID de la factura, OC, transferencia, etc.
        Tipo_Referencia VARCHAR(20) NULL, -- 'Factura', 'OC', 'Transferencia', etc.
        Observaciones TEXT NULL,
        CONSTRAINT FK_MovimientosInventario_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT FK_MovimientosInventario_Sucursal FOREIGN KEY (ID_Sucursal) REFERENCES Sucursales(ID_Sucursal),
        CONSTRAINT FK_MovimientosInventario_Usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
        CONSTRAINT CK_MovimientosInventario_Tipo CHECK (Tipo IN ('Compra', 'Venta', 'Transferencia', 'Ajuste', 'Devolucion'))
    );
GO

CREATE TABLE Garantias (
        ID_Garantia INT IDENTITY(1,1) PRIMARY KEY,
        ID_Producto INT NOT NULL,
        Tiempo_Garantia INT NOT NULL, -- en días
        Tipo_Garantia VARCHAR(50) NOT NULL, -- 'Fábrica', 'Local', 'Extendida'
        Descripcion TEXT NULL,
        Activo BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_Garantias_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto)
    );
GO

CREATE TABLE Descuentos (
        ID_Descuento INT IDENTITY(1,1) PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Descripcion TEXT NULL,
        Porcentaje DECIMAL(5,2) NOT NULL,
        Monto_Fijo DECIMAL(10,2) NULL,
        Tipo_Descuento VARCHAR(20) NOT NULL, -- 'Porcentaje', 'Monto Fijo'
        Fecha_Inicio DATE NOT NULL,
        Fecha_Fin DATE NOT NULL,
        Cantidad_Minima INT NULL,
        Cantidad_Maxima INT NULL,
        Activo BIT NOT NULL DEFAULT 1,
        CONSTRAINT CK_Descuentos_Porcentaje CHECK (Porcentaje >= 0 AND Porcentaje <= 100)
    );
GO

CREATE TABLE Productos_Descuentos (
        ID_Producto_Descuento INT IDENTITY(1,1) PRIMARY KEY,
        ID_Producto INT NOT NULL,
        ID_Descuento INT NOT NULL,
        CONSTRAINT FK_ProductosDescuentos_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT FK_ProductosDescuentos_Descuento FOREIGN KEY (ID_Descuento) REFERENCES Descuentos(ID_Descuento),
        CONSTRAINT UQ_Producto_Descuento UNIQUE (ID_Producto, ID_Descuento)
    );
GO

CREATE TABLE Devoluciones (
        ID_Devolucion INT IDENTITY(1,1) PRIMARY KEY,
        ID_Factura_Venta INT NOT NULL,
        Fecha_Devolucion DATETIME NOT NULL DEFAULT GETDATE(),
        Motivo VARCHAR(200) NOT NULL,
        Estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente', -- 'Pendiente', 'Aprobada', 'Rechazada', 'Completada'
        ID_Usuario INT NOT NULL,
        Observaciones TEXT NULL,
        CONSTRAINT FK_Devoluciones_Factura FOREIGN KEY (ID_Factura_Venta) REFERENCES Facturas_Venta(ID_Factura_Venta),
        CONSTRAINT FK_Devoluciones_Usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario)
    );
GO

CREATE TABLE Detalles_Devolucion (
        ID_Detalle_Devolucion INT IDENTITY(1,1) PRIMARY KEY,
        ID_Devolucion INT NOT NULL,
        ID_Producto INT NOT NULL,
        Cantidad INT NOT NULL,
        Motivo_Especifico VARCHAR(200) NULL,
        CONSTRAINT FK_DetallesDevolucion_Devolucion FOREIGN KEY (ID_Devolucion) REFERENCES Devoluciones(ID_Devolucion) ON DELETE CASCADE,
        CONSTRAINT FK_DetallesDevolucion_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT CK_DetallesDevolucion_Cantidad CHECK (Cantidad > 0)
    );
GO

CREATE TABLE Transferencias_Sucursales (
        ID_Transferencia INT IDENTITY(1,1) PRIMARY KEY,
        Numero_Transferencia VARCHAR(20) NULL UNIQUE,
        ID_Sucursal_Origen INT NOT NULL,
        ID_Sucursal_Destino INT NOT NULL,
        Fecha_Solicitud DATETIME NOT NULL DEFAULT GETDATE(),
        Fecha_Transferencia DATETIME NULL,
        Estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente', -- 'Pendiente', 'Aprobada', 'En Tránsito', 'Completada', 'Cancelada'
        ID_Usuario_Solicitante INT NOT NULL,
        ID_Usuario_Autorizador INT NULL,
        Observaciones TEXT NULL,
        CONSTRAINT FK_Transferencias_SucursalOrigen FOREIGN KEY (ID_Sucursal_Origen) REFERENCES Sucursales(ID_Sucursal),
        CONSTRAINT FK_Transferencias_SucursalDestino FOREIGN KEY (ID_Sucursal_Destino) REFERENCES Sucursales(ID_Sucursal),
        CONSTRAINT FK_Transferencias_UsuarioSolicitante FOREIGN KEY (ID_Usuario_Solicitante) REFERENCES Usuarios(ID_Usuario),
        CONSTRAINT FK_Transferencias_UsuarioAutorizador FOREIGN KEY (ID_Usuario_Autorizador) REFERENCES Usuarios(ID_Usuario),
        CONSTRAINT CK_Transferencias_Sucursales CHECK (ID_Sucursal_Origen != ID_Sucursal_Destino)
    );
GO

CREATE TABLE Detalles_Transferencia (
        ID_Detalle_Transferencia INT IDENTITY(1,1) PRIMARY KEY,
        ID_Transferencia INT NOT NULL,
        ID_Producto INT NOT NULL,
        Cantidad INT NOT NULL,
        Cantidad_Recibida INT NULL,
        CONSTRAINT FK_DetallesTransferencia_Transferencia FOREIGN KEY (ID_Transferencia) REFERENCES Transferencias_Sucursales(ID_Transferencia) ON DELETE CASCADE,
        CONSTRAINT FK_DetallesTransferencia_Producto FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
        CONSTRAINT CK_DetallesTransferencia_Cantidad CHECK (Cantidad > 0)
    );
GO

CREATE TABLE Auditoria_Cambios (
        ID_Auditoria INT IDENTITY(1,1) PRIMARY KEY,
        Tabla_Afectada VARCHAR(100) NOT NULL,
        ID_Registro INT NOT NULL,
        Tipo_Operacion VARCHAR(20) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
        Fecha_Operacion DATETIME NOT NULL DEFAULT GETDATE(),
        ID_Usuario INT NOT NULL,
        Datos_Anteriores NVARCHAR(MAX) NULL,
        Datos_Nuevos NVARCHAR(MAX) NULL,
        IP_Cliente VARCHAR(45) NULL,
        CONSTRAINT FK_Auditoria_Usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario)
    );
GO

-- Índices en Categorias
CREATE INDEX IX_Categorias_Padre ON Categorias(Categoria_Padre);
CREATE INDEX IX_Categorias_Activo ON Categorias(Activo);

-- Índices en Productos
CREATE INDEX IX_Productos_Categoria ON Productos(ID_Categoria);
CREATE INDEX IX_Productos_Unidad ON Productos(ID_Unidad_de_medida);
CREATE INDEX IX_Productos_CodigoBarras ON Productos(Codigo_Barras);
CREATE INDEX IX_Productos_SKU ON Productos(SKU);
CREATE INDEX IX_Productos_Marca ON Productos(Marca);
CREATE INDEX IX_Productos_Activo ON Productos(Activo);

-- Índices en Clientes
CREATE INDEX IX_Clientes_CUIT ON Clientes(CUIT_CUIL);
CREATE INDEX IX_Clientes_Tipo ON Clientes(Tipo_Cliente);
CREATE INDEX IX_Clientes_Provincia ON Clientes(Provincia);
CREATE INDEX IX_Clientes_Activo ON Clientes(Activo);

-- Índices en Proveedores
CREATE INDEX IX_Proveedores_CUIT ON Proveedores(CUIT);
CREATE INDEX IX_Proveedores_Provincia ON Proveedores(Provincia);
CREATE INDEX IX_Proveedores_Activo ON Proveedores(Activo);

-- Índices en Inventario
CREATE INDEX IX_Inventario_Producto ON Inventario(ID_Producto);
CREATE INDEX IX_Inventario_Sucursal ON Inventario(ID_Sucursal);
CREATE INDEX IX_Inventario_Stock ON Inventario(Stock_Actual, Stock_Minimo);

-- Índices en Facturas_Venta
CREATE INDEX IX_FacturasVenta_Cliente ON Facturas_Venta(ID_Cliente);
CREATE INDEX IX_FacturasVenta_Sucursal ON Facturas_Venta(ID_Sucursal);
CREATE INDEX IX_FacturasVenta_Usuario ON Facturas_Venta(ID_Usuario);
CREATE INDEX IX_FacturasVenta_Fecha ON Facturas_Venta(Fecha);
CREATE INDEX IX_FacturasVenta_Tipo ON Facturas_Venta(Tipo_Factura);
CREATE INDEX IX_FacturasVenta_Estado ON Facturas_Venta(Estado);

-- Índices en Detalles_Factura_Venta
CREATE INDEX IX_DetallesFactura_Factura ON Detalles_Factura_Venta(ID_Factura_Venta);
CREATE INDEX IX_DetallesFactura_Producto ON Detalles_Factura_Venta(ID_Producto);

-- Índices en Pagos
CREATE INDEX IX_Pagos_Factura ON Pagos(ID_Factura_Venta);
CREATE INDEX IX_Pagos_Fecha ON Pagos(Fecha);
CREATE INDEX IX_Pagos_Metodo ON Pagos(Metodo);

-- Índices en Ordenes_Compra
CREATE INDEX IX_OrdenesCompra_Proveedor ON Ordenes_Compra(ID_Proveedor);
CREATE INDEX IX_OrdenesCompra_Sucursal ON Ordenes_Compra(ID_Sucursal);
CREATE INDEX IX_OrdenesCompra_Usuario ON Ordenes_Compra(ID_Usuario);
CREATE INDEX IX_OrdenesCompra_Fecha ON Ordenes_Compra(Fecha);
CREATE INDEX IX_OrdenesCompra_Estado ON Ordenes_Compra(Estado);

-- Índices en Detalle_OC
CREATE INDEX IX_DetalleOC_Orden ON Detalle_OC(ID_OC);
CREATE INDEX IX_DetalleOC_Producto ON Detalle_OC(ID_Producto);

-- Índices en Movimientos_Inventario
CREATE INDEX IX_MovimientosInventario_Producto ON Movimientos_Inventario(ID_Producto);
CREATE INDEX IX_MovimientosInventario_Sucursal ON Movimientos_Inventario(ID_Sucursal);
CREATE INDEX IX_MovimientosInventario_Fecha ON Movimientos_Inventario(Fecha);
CREATE INDEX IX_MovimientosInventario_Usuario ON Movimientos_Inventario(ID_Usuario);
CREATE INDEX IX_MovimientosInventario_Tipo ON Movimientos_Inventario(Tipo);

-- Índices en Devoluciones
CREATE INDEX IX_Devoluciones_Factura ON Devoluciones(ID_Factura_Venta);
CREATE INDEX IX_Devoluciones_Fecha ON Devoluciones(Fecha_Devolucion);
CREATE INDEX IX_Devoluciones_Estado ON Devoluciones(Estado);

-- Índices en Transferencias_Sucursales
CREATE INDEX IX_Transferencias_Origen ON Transferencias_Sucursales(ID_Sucursal_Origen);
CREATE INDEX IX_Transferencias_Destino ON Transferencias_Sucursales(ID_Sucursal_Destino);
CREATE INDEX IX_Transferencias_Fecha ON Transferencias_Sucursales(Fecha_Solicitud);
CREATE INDEX IX_Transferencias_Estado ON Transferencias_Sucursales(Estado);

-- Índices en Auditoria_Cambios
CREATE INDEX IX_Auditoria_Tabla ON Auditoria_Cambios(Tabla_Afectada);
CREATE INDEX IX_Auditoria_Fecha ON Auditoria_Cambios(Fecha_Operacion);
CREATE INDEX IX_Auditoria_Usuario ON Auditoria_Cambios(ID_Usuario);
GO

-- =====================================================
-- 9. TRIGGERS PARA AUDITORÍA
-- =====================================================

CREATE TRIGGER TR_Productos_Auditoria
ON Productos
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ID_Usuario INT = (SELECT TOP 1 ID_Usuario FROM Usuarios WHERE Email = SYSTEM_USER);
    IF @ID_Usuario IS NULL SET @ID_Usuario = 1; -- Usuario por defecto
    
    -- Para INSERT
    IF EXISTS (SELECT * FROM inserted) AND NOT EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Nuevos)
        SELECT 'Productos', ID_Producto, 'INSERT', @ID_Usuario, 
               'Producto creado: ' + ISNULL(Nombre, 'Sin nombre') + 
               ' - Precio: $' + CAST(Precio AS VARCHAR(20)) +
               ' - Categoría: ' + CAST(ID_Categoria AS VARCHAR(10))
        FROM inserted;
    END
    
    -- Para UPDATE
    IF EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Anteriores, Datos_Nuevos)
        SELECT 'Productos', i.ID_Producto, 'UPDATE', @ID_Usuario,
               'Precio anterior: $' + CAST(d.Precio AS VARCHAR(20)) + ' - Nombre: ' + ISNULL(d.Nombre, 'Sin nombre'),
               'Precio nuevo: $' + CAST(i.Precio AS VARCHAR(20)) + ' - Nombre: ' + ISNULL(i.Nombre, 'Sin nombre')
        FROM inserted i
        INNER JOIN deleted d ON i.ID_Producto = d.ID_Producto;
    END
    
    -- Para DELETE
    IF NOT EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Anteriores)
        SELECT 'Productos', ID_Producto, 'DELETE', @ID_Usuario,
               'Producto eliminado: ' + ISNULL(Nombre, 'Sin nombre') + 
               ' - Precio: $' + CAST(Precio AS VARCHAR(20))
        FROM deleted;
    END
END
GO

-- Trigger para auditoría de cambios en Facturas_Venta (VERSIÓN SIMPLIFICADA)
CREATE TRIGGER TR_Facturas_Venta_Auditoria
ON Facturas_Venta
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ID_Usuario INT = (SELECT TOP 1 ID_Usuario FROM Usuarios WHERE Email = SYSTEM_USER);
    IF @ID_Usuario IS NULL SET @ID_Usuario = 1;
    
    -- Para INSERT
    IF EXISTS (SELECT * FROM inserted) AND NOT EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Nuevos)
        SELECT 'Facturas_Venta', ID_Factura_Venta, 'INSERT', @ID_Usuario, 
               'Factura creada: ' + ISNULL(Numero_Factura, 'Sin número') + 
               ' - Total: $' + CAST(Total AS VARCHAR(20)) +
               ' - Tipo: ' + ISNULL(Tipo_Factura, 'Sin tipo') +
               ' - Estado: ' + ISNULL(Estado, 'Sin estado')
        FROM inserted;
    END
    
    -- Para UPDATE
    IF EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Anteriores, Datos_Nuevos)
        SELECT 'Facturas_Venta', i.ID_Factura_Venta, 'UPDATE', @ID_Usuario,
               'Total anterior: $' + CAST(d.Total AS VARCHAR(20)) + ' - Estado: ' + ISNULL(d.Estado, 'Sin estado'),
               'Total nuevo: $' + CAST(i.Total AS VARCHAR(20)) + ' - Estado: ' + ISNULL(i.Estado, 'Sin estado')
        FROM inserted i
        INNER JOIN deleted d ON i.ID_Factura_Venta = d.ID_Factura_Venta;
    END
    
    -- Para DELETE
    IF NOT EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Anteriores)
        SELECT 'Facturas_Venta', ID_Factura_Venta, 'DELETE', @ID_Usuario,
               'Factura eliminada: ' + ISNULL(Numero_Factura, 'Sin número') + 
               ' - Total: $' + CAST(Total AS VARCHAR(20))
        FROM deleted;
    END
END
GO

-- Trigger para auditoría de cambios en Detalles_Factura_Venta (VERSIÓN SIMPLIFICADA)
CREATE TRIGGER TR_Detalles_Factura_Venta_Auditoria
ON Detalles_Factura_Venta
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ID_Usuario INT = (SELECT TOP 1 ID_Usuario FROM Usuarios WHERE Email = SYSTEM_USER);
    IF @ID_Usuario IS NULL SET @ID_Usuario = 1;
    
    -- Para INSERT
    IF EXISTS (SELECT * FROM inserted) AND NOT EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Nuevos)
        SELECT 'Detalles_Factura_Venta', ID_Detalle, 'INSERT', @ID_Usuario, 
               'Detalle agregado: Producto ' + CAST(ID_Producto AS VARCHAR(10)) + 
               ' - Cantidad: ' + CAST(Cantidad AS VARCHAR(10)) +
               ' - Precio: $' + CAST(Precio_Unitario AS VARCHAR(20)) +
               ' - Subtotal: $' + CAST(Subtotal AS VARCHAR(20))
        FROM inserted;
    END
    
    -- Para UPDATE
    IF EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Anteriores, Datos_Nuevos)
        SELECT 'Detalles_Factura_Venta', i.ID_Detalle, 'UPDATE', @ID_Usuario,
               'Cantidad anterior: ' + CAST(d.Cantidad AS VARCHAR(10)) + ' - Precio: $' + CAST(d.Precio_Unitario AS VARCHAR(20)),
               'Cantidad nueva: ' + CAST(i.Cantidad AS VARCHAR(10)) + ' - Precio: $' + CAST(i.Precio_Unitario AS VARCHAR(20))
        FROM inserted i
        INNER JOIN deleted d ON i.ID_Detalle = d.ID_Detalle;
    END
    
    -- Para DELETE
    IF NOT EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
    BEGIN
        INSERT INTO Auditoria_Cambios (Tabla_Afectada, ID_Registro, Tipo_Operacion, ID_Usuario, Datos_Anteriores)
        SELECT 'Detalles_Factura_Venta', ID_Detalle, 'DELETE', @ID_Usuario,
               'Detalle eliminado: Producto ' + CAST(ID_Producto AS VARCHAR(10)) + 
               ' - Cantidad: ' + CAST(Cantidad AS VARCHAR(10)) +
               ' - Subtotal: $' + CAST(Subtotal AS VARCHAR(20))
        FROM deleted;
    END
END
GO
-- =====================================================
-- 10. VISTAS ÚTILES
-- =====================================================

-- Vista para stock bajo
CREATE VIEW vw_Stock_Bajo AS
SELECT 
    p.Nombre AS Producto,
    p.Codigo_Barras,
    p.SKU,
    c.Nombre AS Categoria,
    s.Nombre AS Sucursal,
    i.Stock_Actual,
    i.Stock_Minimo,
    (i.Stock_Minimo - i.Stock_Actual) AS Cantidad_Faltante
FROM Inventario i
INNER JOIN Productos p ON i.ID_Producto = p.ID_Producto
INNER JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
INNER JOIN Sucursales s ON i.ID_Sucursal = s.ID_Sucursal
WHERE i.Stock_Actual <= i.Stock_Minimo AND p.Activo = 1 AND i.Activo = 1;
GO

-- Vista para productos más vendidos (TOP 50)
CREATE VIEW vw_Productos_Mas_Vendidos AS
SELECT TOP 50
    p.Nombre AS Producto,
    p.Codigo_Barras,
    c.Nombre AS Categoria,
    SUM(dfv.Cantidad) AS Total_Vendido,
    COUNT(DISTINCT fv.ID_Factura_Venta) AS Cantidad_Facturas
FROM Productos p
INNER JOIN Detalles_Factura_Venta dfv ON p.ID_Producto = dfv.ID_Producto
INNER JOIN Facturas_Venta fv ON dfv.ID_Factura_Venta = fv.ID_Factura_Venta
INNER JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
WHERE fv.Estado != 'Anulada'
GROUP BY p.ID_Producto, p.Nombre, p.Codigo_Barras, c.Nombre
ORDER BY Total_Vendido DESC;
GO

-- Vista para resumen de ventas por sucursal
CREATE VIEW vw_Resumen_Ventas_Sucursal AS
SELECT 
    s.Nombre AS Sucursal,
    COUNT(fv.ID_Factura_Venta) AS Cantidad_Facturas,
    SUM(fv.Total) AS Total_Ventas,
    AVG(fv.Total) AS Promedio_Factura,
    MIN(fv.Fecha) AS Primera_Venta,
    MAX(fv.Fecha) AS Ultima_Venta
FROM Sucursales s
LEFT JOIN Facturas_Venta fv ON s.ID_Sucursal = fv.ID_Sucursal
WHERE fv.Estado != 'Anulada' OR fv.Estado IS NULL
GROUP BY s.ID_Sucursal, s.Nombre;
GO

-- Vista para clientes más frecuentes (TOP 30)
CREATE VIEW vw_Clientes_Mas_Frecuentes AS
SELECT TOP 30
    c.Nombre + ' ' + c.Apellido AS Cliente,
    c.CUIT_CUIL,
    c.Tipo_Cliente,
    COUNT(fv.ID_Factura_Venta) AS Cantidad_Compras,
    SUM(fv.Total) AS Total_Gastado,
    AVG(fv.Total) AS Promedio_Compra
FROM Clientes c
INNER JOIN Facturas_Venta fv ON c.ID_Cliente = fv.ID_Cliente
WHERE fv.Estado != 'Anulada'
GROUP BY c.ID_Cliente, c.Nombre, c.Apellido, c.CUIT_CUIL, c.Tipo_Cliente
ORDER BY Total_Gastado DESC;
GO

-- Vista para stock crítico por sucursal
CREATE VIEW vw_Stock_Critico_Sucursal AS
SELECT 
    s.Nombre AS Sucursal,
    p.Nombre AS Producto,
    p.Codigo_Barras,
    i.Stock_Actual,
    i.Stock_Minimo,
    (i.Stock_Minimo - i.Stock_Actual) AS Cantidad_Faltante,
    c.Nombre AS Categoria
FROM Inventario i
INNER JOIN Productos p ON i.ID_Producto = p.ID_Producto
INNER JOIN Sucursales s ON i.ID_Sucursal = s.ID_Sucursal
INNER JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
WHERE i.Stock_Actual < i.Stock_Minimo 
  AND p.Activo = 1 
  AND i.Activo = 1;
GO

-- Vista para ventas por mes
CREATE VIEW vw_Ventas_Por_Mes AS
SELECT 
    YEAR(fv.Fecha) AS Año,
    MONTH(fv.Fecha) AS Mes,
    DATENAME(MONTH, fv.Fecha) AS Nombre_Mes,
    COUNT(fv.ID_Factura_Venta) AS Cantidad_Facturas,
    SUM(fv.Total) AS Total_Ventas,
    AVG(fv.Total) AS Promedio_Factura
FROM Facturas_Venta fv
WHERE fv.Estado != 'Anulada'
GROUP BY YEAR(fv.Fecha), MONTH(fv.Fecha), DATENAME(MONTH, fv.Fecha);
GO

-- Vista para productos sin stock
CREATE VIEW vw_Productos_Sin_Stock AS
SELECT 
    p.Nombre AS Producto,
    p.Codigo_Barras,
    p.SKU,
    c.Nombre AS Categoria,
    s.Nombre AS Sucursal
FROM Productos p
INNER JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
CROSS JOIN Sucursales s
LEFT JOIN Inventario i ON p.ID_Producto = i.ID_Producto AND s.ID_Sucursal = i.ID_Sucursal
WHERE (i.ID_Producto IS NULL OR i.Stock_Actual = 0)
  AND p.Activo = 1
  AND s.Activo = 1;
GO

-- Vista para facturas pendientes de pago
CREATE VIEW vw_Facturas_Pendientes AS
SELECT 
    fv.ID_Factura_Venta,
    fv.Numero_Factura,
    fv.Fecha,
    c.Nombre + ' ' + c.Apellido AS Cliente,
    c.CUIT_CUIL,
    s.Nombre AS Sucursal,
    fv.Total,
    fv.Estado,
    DATEDIFF(DAY, fv.Fecha, GETDATE()) AS Dias_Pendiente
FROM Facturas_Venta fv
INNER JOIN Clientes c ON fv.ID_Cliente = c.ID_Cliente
INNER JOIN Sucursales s ON fv.ID_Sucursal = fv.ID_Sucursal
WHERE fv.Estado IN ('Emitida', 'Pendiente');
GO

-- Vista para resumen de categorías más vendidas
CREATE VIEW vw_Categorias_Mas_Vendidas AS
SELECT TOP 20
    c.Nombre AS Categoria,
    COUNT(DISTINCT fv.ID_Factura_Venta) AS Cantidad_Facturas,
    SUM(dfv.Cantidad) AS Total_Unidades_Vendidas,
    SUM(dfv.Subtotal) AS Total_Ventas_Categoria
FROM Categorias c
INNER JOIN Productos p ON c.ID_Categoria = p.ID_Categoria
INNER JOIN Detalles_Factura_Venta dfv ON p.ID_Producto = dfv.ID_Producto
INNER JOIN Facturas_Venta fv ON dfv.ID_Factura_Venta = fv.ID_Factura_Venta
WHERE fv.Estado != 'Anulada'
GROUP BY c.ID_Categoria, c.Nombre
ORDER BY Total_Ventas_Categoria DESC;
GO

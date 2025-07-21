USE Ferreteriadb;
GO

-- =====================================================
-- 1. INSERTAR CATEGORÍAS DETALLADAS
-- =====================================================

-- Categorías principales
INSERT INTO Categorias (Nombre, Descripcion) VALUES 
('Herramientas Manuales', 'Herramientas de uso manual para construcción y reparación'),
('Herramientas Eléctricas', 'Herramientas que funcionan con electricidad'),
('Plomería', 'Productos para instalaciones de agua y gas'),
('Electricidad', 'Materiales eléctricos y de iluminación'),
('Pinturas y Accesorios', 'Pinturas, solventes y herramientas para pintar'),
('Construcción', 'Materiales de construcción y albañilería'),
('Jardín y Exterior', 'Productos para jardín y espacios exteriores'),
('Seguridad', 'Elementos de protección personal'),
('Fijaciones', 'Tornillos, clavos, anclajes y elementos de fijación'),
('Automotriz', 'Productos para vehículos y mantenimiento automotriz');
GO


-- Subcategorías para Herramientas Manuales
INSERT INTO Categorias (Nombre, Descripcion, Categoria_Padre) VALUES 
('Martillos y Mazos', 'Martillos de diferentes tipos y tamaños', 1),
('Destornilladores', 'Destornilladores planos y Phillips', 1),
('Alicates y Pinzas', 'Alicates, pinzas y herramientas de sujeción', 1),
('Llaves', 'Llaves ajustables, combinadas y especiales', 1),
('Sierras Manuales', 'Sierras de mano para diferentes materiales', 1),
('Niveles y Medición', 'Niveles, cintas métricas y herramientas de medición', 1);

-- Subcategorías para Herramientas Eléctricas
INSERT INTO Categorias (Nombre, Descripcion, Categoria_Padre) VALUES 
('Taladros', 'Taladros eléctricos y accesorios', 2),
('Amoladoras', 'Amoladoras angulares y rectas', 2),
('Sierras Eléctricas', 'Sierras circulares, caladoras y sable', 2),
('Lijadoras', 'Lijadoras orbitales y de banda', 2),
('Compresores', 'Compresores de aire y herramientas neumáticas', 2);

-- Subcategorías para Plomería
INSERT INTO Categorias (Nombre, Descripcion, Categoria_Padre) VALUES 
('Caños y Tuberías', 'Caños de PVC, hierro y cobre', 3),
('Conexiones', 'Codos, tees, uniones y accesorios', 3),
('Grifería', 'Canillas, duchas y accesorios de baño', 3),
('Bombas', 'Bombas de agua y desagote', 3),
('Accesorios Sanitarios', 'Selladores, cintas y accesorios', 3);

-- Subcategorías para Electricidad
INSERT INTO Categorias (Nombre, Descripcion, Categoria_Padre) VALUES 
('Cables', 'Cables eléctricos de diferentes secciones', 4),
('Interruptores y Tomas', 'Interruptores, tomas y accesorios', 4),
('Iluminación', 'Lámparas, focos y accesorios de iluminación', 4),
('Tableros', 'Tableros eléctricos y disyuntores', 4),
('Accesorios Eléctricos', 'Cajas, caños y accesorios de instalación', 4);

-- =====================================================
-- 2. INSERTAR UNIDADES DE MEDIDA
-- =====================================================

INSERT INTO Unidades_de_medida (Nombre, Abreviatura) VALUES 
('Unidad', 'un'),
('Metro', 'm'),
('Metro Cuadrado', 'm2'),
('Metro Cúbico', 'm3'),
('Kilogramo', 'kg'),
('Gramo', 'g'),
('Litro', 'L'),
('Mililitro', 'ml'),
('Caja', 'caja'),
('Paquete', 'pkg'),
('Rollo', 'rollo'),
('Par', 'par'),
('Docena', 'doc'),
('Centímetro', 'cm'),
('Milímetro', 'mm'),
('Pulgada', 'pulgada'),
('Pie', 'pie'),
('Yarda', 'yd'),
('Galón', 'gal'),
('Onza', 'oz'),
('Libra', 'lb'),
('Set', 'set'),
('Kit', 'kit'),
('Botella', 'bot'),
('Lata', 'lata'),
('Tubo', 'tubo'),
('Placa', 'placa'),
('Plancha', 'plancha'),
('Viga', 'viga'),
('Ladrillo', 'ladrillo'),
('Bolsa', 'bolsa'),
('Saco', 'saco'),
('Bidón', 'bidón'),
('Tambor', 'tambor'),
('Fardo', 'fardo'),
('Resma', 'resma'),
('Bobina', 'bobina'),
('Carrete', 'carrete'),
('Manguera', 'manguera'),
('Cable', 'cable'),
('Alambre', 'alambre'),
('Varilla', 'varilla'),
('Perfil', 'perfil'),
('Ángulo', 'ángulo'),
('Canaleta', 'canaleta'),
('Canal', 'canal'),
('Caño', 'caño'),
('Válvula', 'válvula'),
('Ventilador', 'ventilador'),
('Extractor', 'extractor'),
('Calefactor', 'calefactor'),
('Aire Acondicionado', 'aire ac'),
('Heladera', 'heladera'),
('Freezer', 'freezer'),
('Lavarropas', 'lavarropas'),
('Secarropas', 'secarropas'),
('Cocina', 'cocina'),
('Horno', 'horno'),
('Microondas', 'microondas'),
('Licuadora', 'licuadora'),
('Batidora', 'batidora'),
('Procesadora', 'proces'),
('Cafetera', 'cafetera'),
('Tostadora', 'tostadora'),
('Aspiradora', 'aspiradora'),
('Escoba', 'escoba'),
('Trapeador', 'trapeador'),
('Balde', 'balde'),
('Escurridor', 'escurridor'),
('Secador', 'secador'),
('Cepillo', 'cepillos'),
('Esponja', 'esponja'),
('Detergente', 'deterg'),
('Lavandina', 'lavand'),
('Jabón', 'jabón'),
('Shampoo', 'shampoo'),
('Acondicionador', 'acond'),
('Desodorante', 'desodor'),
('Papel Higiénico', 'papel'),
('Toallas', 'toallas'),
('Sábanas', 'sábanas'),
('Frazadas', 'frazadas'),
('Almohadas', 'almohadas'),
('Colchón', 'colchón'),
('Sommier', 'sommier'),
('Mesa', 'mesa'),
('Silla', 'silla'),
('Sillón', 'sillón'),
('Mesa de Luz', 'mesa luz'),
('Ropero', 'ropero'),
('Estantería', 'estant'),
('Biblioteca', 'biblio'),
('Escritorio', 'escrit'),
('Silla de Escritorio', 'silla esc'),
('Cama', 'cama'),
('Respaldo', 'respaldo'),
('Piecera', 'piecera'),
('Cajón', 'cajón'),
('Puerta', 'puerta'),
('Ventana', 'ventana'),
('Persiana', 'persiana'),
('Cortina', 'cortina'),
('Alfombra', 'alfombra'),
('Lámpara', 'lámpara'),
('Lámpara de Techo', 'lamp techo'),
('Lámpara de Mesa', 'lamp mesa'),
('Lámpara de Pie', 'lamp pie'),
('Foco', 'foco'),
('Foco LED', 'focoled'),
('Tubo Fluorescente', 'tubo flu'),
('Placa LED', 'placaled'),
('Tira LED', 'tiraled'),
('Transformador', 'transf'),
('Dimmer', 'dimmer'),
('Sensor', 'sensor'),
('Timbre', 'timbre'),
('Intercomunicador', 'intercom'),
('Cerco Eléctrico', 'cercoelec'),
('Alarma', 'alarma'),
('Cámara', 'cámara'),
('DVR', 'dvr'),
('Monitor', 'monitor'),
('Teclado', 'teclado'),
('Mouse', 'mouse'),
('Impresora', 'impresora'),
('Scanner', 'scanner'),
('Pendrive', 'pendrive'),
('Disco Externo', 'disco'),
('Cable USB', 'cableusb'),
('Cable HDMI', 'cablehdmi'),
('Cable VGA', 'cablevga'),
('Cable de Red', 'cablered'),
('Router', 'router'),
('Modem', 'modem'),
('Switch', 'switch'),
('Repetidor WiFi', 'repetwifi'),
('Antena', 'antena'),
('Pararrayos', 'pararray'),
('Tierra', 'tierra'),
('Puesta a Tierra', 'puesta'),
('Jabalina', 'jabal'),
('Cable de Tierra', 'cable t'),
('Conectores', 'conect'),
('Terminal', 'terminal'),
('Oreja', 'oreja'),
('Cable N', 'cable n'),
('Cable PE', 'cable pe'),
('Cable NYM', 'cable nym'),
('Cable NYA', 'cable nya'),
('Cable NYAF', 'cable nyaf'),
('Cable NYM-J', 'cable nymj'),
('Cable NYM-O', 'cable nymo'),
('Cable NYM-Z', 'cable nymz'),
('Cable NYM-Y', 'cable nymy'),
('Cable NYM-X', 'cable nymx'),
('Cable NYM-W', 'cable nymw'),
('Cable NYM-V', 'cable nymv'),
('Cable NYM-U', 'cable nymu'),
('Cable NYM-T', 'cable nymt'),
('Cable NYM-S', 'cable nyms'),
('Cable NYM-R', 'cable nymr'),
('Cable NYM-Q', 'cable nymq'),
('Cable NYM-P', 'cable nymp'),
('Cable NYM-N', 'cable nymn'),
('Cable NYM-M', 'cable nymm'),
('Cable NYM-L', 'cable nyml'),
('Cable NYM-K', 'cable nymk'),
('Cable NYM-I', 'cable nymi'),
('Cable NYM-H', 'cable nymh'),
('Cable NYM-G', 'cable nymg'),
('Cable NYM-F', 'cable nymf'),
('Cable NYM-E', 'cable nyme'),
('Cable NYM-D', 'cable nymd'),
('Cable NYM-C', 'cable nymc'),
('Cable NYM-B', 'cable nymb'),
('Cable NYM-A', 'cable nyma');

-- =====================================================
-- 3. INSERTAR SUCURSALES
-- =====================================================

INSERT INTO Sucursales (Nombre, Direccion, Localidad, Provincia, Codigo_Postal, Telefono, Email, Horario_Apertura, Horario_Cierre) VALUES 
('Ferretería Central - Microcentro', 'Av. Corrientes 1234', 'Buenos Aires', 'Buenos Aires', '1043', '011-4321-5678', 'central@ferreteria.com', '08:00', '20:00'),
('Ferretería Norte - Palermo', 'Av. Santa Fe 2345', 'Buenos Aires', 'Buenos Aires', '1125', '011-4321-5679', 'palermo@ferreteria.com', '08:00', '20:00'),
('Ferretería Sur - La Boca', 'Av. Almirante Brown 3456', 'Buenos Aires', 'Buenos Aires', '1160', '011-4321-5680', 'laboca@ferreteria.com', '08:00', '20:00'),
('Ferretería Oeste - Liniers', 'Av. Rivadavia 4567', 'Buenos Aires', 'Buenos Aires', '1408', '011-4321-5681', 'liniers@ferreteria.com', '08:00', '20:00'),
('Ferretería Este - Puerto Madero', 'Av. Alicia Moreau de Justo 5678', 'Buenos Aires', 'Buenos Aires', '1107', '011-4321-5682', 'puertomadero@ferreteria.com', '08:00', '20:00'),
('Ferretería Córdoba Centro', 'Av. Colón 6789', 'Córdoba', 'Córdoba', '5000', '0351-4321-5678', 'cordoba@ferreteria.com', '08:00', '20:00'),
('Ferretería Rosario Norte', 'Av. Pellegrini 7890', 'Rosario', 'Santa Fe', '2000', '0341-4321-5678', 'rosario@ferreteria.com', '08:00', '20:00'),
('Ferretería Mendoza Plaza', 'Av. San Martín 8901', 'Mendoza', 'Mendoza', '5500', '0261-4321-5678', 'mendoza@ferreteria.com', '08:00', '20:00'),
('Ferretería Tucumán Central', 'Av. Sarmiento 9012', 'San Miguel de Tucumán', 'Tucumán', '4000', '0381-4321-5678', 'tucuman@ferreteria.com', '08:00', '20:00'),
('Ferretería Mar del Plata', 'Av. Independencia 0123', 'Mar del Plata', 'Buenos Aires', '7600', '0223-4321-5678', 'mardelplata@ferreteria.com', '08:00', '20:00');

-- =====================================================
-- 4. INSERTAR USUARIOS
-- =================================================

INSERT INTO Usuarios (Nombre, Apellido, CUIL, Rol, Email, Contraseña, ID_Sucursal) VALUES 
('Juan Carlos', 'González', '20-21994678-9', 'Administrador', 'juan.gonzalez@ferreteria.com', 'admin123', 1),
('María Elena', 'Rodríguez', '27-23442719-0', 'Vendedor', 'maria.rodriguez@ferreteria.com', 'vendedor123', 1),
('Carlos Alberto', 'López', '20-34897890-1', 'Vendedor', 'carlos.lopez@ferreteria.com', 'vendedor123', 1),
('Ana Sofía', 'Martínez', '27-49868901-2', 'Cajero', 'ana.martinez@ferreteria.com', 'cajero123', 1),
('Roberto Daniel', 'García', '20-56754812-3', 'Vendedor', 'roberto.garcia@ferreteria.com', 'vendedor123', 2),
('Laura Beatriz', 'Fernández', '27-67050123-4', 'Vendedor', 'laura.fernandez@ferreteria.com', 'vendedor123', 2),
('Miguel Ángel', 'Pérez', '20-78221234-5', 'Cajero', 'miguel.perez@ferreteria.com', 'cajero123', 2),
('Silvia Marcela', 'Gómez', '27-89356345-6', 'Vendedor', 'silvia.gomez@ferreteria.com', 'vendedor123', 3),
('Fernando José', 'Díaz', '20-26492645-7', 'Vendedor', 'fernando.diaz@ferreteria.com', 'vendedor123', 3),
('Patricia Alejandra', 'Torres', '27-02635184-8', 'Cajero', 'patricia.torres@ferreteria.com', 'cajero123', 3),
('Ricardo Luis', 'Vargas', '20-26391635-0', 'Vendedor', 'ricardo.vargas@ferreteria.com', 'vendedor123', 4),
('Mónica Graciela', 'Ruiz', '27-84537194-1', 'Vendedor', 'monica.ruiz@ferreteria.com', 'vendedor123', 4),
('Eduardo Martín', 'Herrera', '20-45391731-2', 'Cajero', 'eduardo.herrera@ferreteria.com', 'cajero123', 4),
('Verónica Isabel', 'Jiménez', '27-64925485-3', 'Vendedor', 'veronica.jimenez@ferreteria.com', 'vendedor123', 5),
('Alejandro Pablo', 'Moreno', '20-99736451-4', 'Vendedor', 'alejandro.moreno@ferreteria.com', 'vendedor123', 5),
('Gabriela Susana', 'Morales', '27-09806374-5', 'Cajero', 'gabriela.morales@ferreteria.com', 'cajero123', 5),
('Diego Fernando', 'Ortiz', '20-62319573-6', 'Vendedor', 'diego.ortiz@ferreteria.com', 'vendedor123', 6),
('Carolina Andrea', 'Castro', '27-87968537-7', 'Vendedor', 'carolina.castro@ferreteria.com', 'vendedor123', 6),
('Héctor Raúl', 'Flores', '20-36284116-8', 'Cajero', 'hector.flores@ferreteria.com', 'cajero123', 6),
('Natalia Soledad', 'Reyes', '27-77665392-9', 'Vendedor', 'natalia.reyes@ferreteria.com', 'vendedor123', 7),
('Gustavo Adolfo', 'Cruz', '20-11327493-0', 'Vendedor', 'gustavo.cruz@ferreteria.com', 'vendedor123', 7),
('Florencia María', 'Ramos', '27-56482104-1', 'Cajero', 'florencia.ramos@ferreteria.com', 'cajero123', 7),
('Marcelo Javier', 'Acosta', '20-90807531-2', 'Vendedor', 'marcelo.acosta@ferreteria.com', 'vendedor123', 8),
('Valeria Romina', 'Mendoza', '27-59163840-3', 'Vendedor', 'valeria.mendoza@ferreteria.com', 'vendedor123', 8),
('Pablo Sebastián', 'Vega', '20-77222846-4', 'Cajero', 'pablo.vega@ferreteria.com', 'cajero123', 8),
('Luciana Belén', 'Rojas', '27-91103659-5', 'Vendedor', 'luciana.rojas@ferreteria.com', 'vendedor123', 9),
('Federico Nicolás', 'Campos', '20-66293649-6', 'Vendedor', 'federico.campos@ferreteria.com', 'vendedor123', 9),
('Agustina Lucía', 'Soto', '27-31629467-7', 'Cajero', 'agustina.soto@ferreteria.com', 'cajero123', 9),
('Matías Ezequiel', 'Cortés', '20-74629473-8', 'Vendedor', 'matias.cortes@ferreteria.com', 'vendedor123', 10),
('Camila Antonella', 'Guzmán', '27-17463005-9', 'Vendedor', 'camila.guzman@ferreteria.com', 'vendedor123', 10),
('Lucas Matías', 'Herrera', '20-45383742-0', 'Cajero', 'lucas.herrera@ferreteria.com', 'cajero123', 10);

-- =====================================================
-- 5. INSERTAR PRODUCTOS REALES
-- =====================================================

-- HERRAMIENTAS MANUALES - MARTILLOS
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Martillo de Uña 16 oz', 'Martillo de uña Stanley con mango de fibra de vidrio', '7891234567890', 'MART-001', 'Stanley', 'FMHT0-55416', 4500.00, 2800.00, 3800.00, 11, 1, 0.45, '30x15x8'),
('Martillo de Uña 20 oz', 'Martillo de uña Stanley con mango ergonómico', '7891234567891', 'MART-002', 'Stanley', 'FMHT0-55420', 5200.00, 3200.00, 4500.00, 11, 1, 0.56, '32x16x8'),
('Martillo de Uña 24 oz', 'Martillo de uña Stanley profesional', '7891234567892', 'MART-003', 'Stanley', 'FMHT0-55424', 5800.00, 3600.00, 5000.00, 11, 1, 0.68, '34x17x8'),
('Martillo de Bola 16 oz', 'Martillo de bola para metalurgia', '7891234567893', 'MART-004', 'Stanley', 'FMHT0-55416B', 4800.00, 3000.00, 4100.00, 11, 1, 0.45, '30x15x8'),
('Martillo de Bola 20 oz', 'Martillo de bola profesional', '7891234567894', 'MART-005', 'Stanley', 'FMHT0-55420B', 5500.00, 3400.00, 4700.00, 11, 1, 0.56, '32x16x8'),
('Mazo de Goma 2 lb', 'Mazo de goma para ajustes delicados', '7891234567895', 'MART-006', 'Stanley', 'FMHT0-5542LB', 3200.00, 2000.00, 2800.00, 11, 1, 0.90, '35x12x12'),
('Mazo de Goma 4 lb', 'Mazo de goma para trabajos pesados', '7891234567896', 'MART-007', 'Stanley', 'FMHT0-5544LB', 4200.00, 2600.00, 3600.00, 11, 1, 1.80, '40x15x15'),
('Martillo de Nylon 16 oz', 'Martillo de nylon para acabados', '7891234567897', 'MART-008', 'Stanley', 'FMHT0-55416N', 3800.00, 2400.00, 3300.00, 11, 1, 0.45, '30x15x8'),
('Martillo de Nylon 20 oz', 'Martillo de nylon profesional', '7891234567898', 'MART-009', 'Stanley', 'FMHT0-55420N', 4500.00, 2800.00, 3900.00, 11, 1, 0.56, '32x16x8'),
('Martillo de Demolición 8 lb', 'Martillo de demolición para construcción', '7891234567899', 'MART-010', 'Stanley', 'FMHT0-5548LB', 8500.00, 5200.00, 7200.00, 11, 1, 3.60, '45x20x20');

-- HERRAMIENTAS MANUALES - DESTORNILLADORES
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Destornillador Plano 3x100mm', 'Destornillador plano Stanley', '7891234567900', 'DEST-001', 'Stanley', '66-052', 1200.00, 750.00, 1000.00, 12, 1, 0.12, '25x3x3'),
('Destornillador Plano 4x125mm', 'Destornillador plano Stanley', '7891234567901', 'DEST-002', 'Stanley', '66-053', 1400.00, 850.00, 1200.00, 12, 1, 0.15, '30x4x4'),
('Destornillador Plano 5x150mm', 'Destornillador plano Stanley', '7891234567902', 'DEST-003', 'Stanley', '66-054', 1600.00, 950.00, 1400.00, 12, 1, 0.18, '35x5x5'),
('Destornillador Plano 6x175mm', 'Destornillador plano Stanley', '7891234567903', 'DEST-004', 'Stanley', '66-055', 1800.00, 1100.00, 1600.00, 12, 1, 0.22, '40x6x6'),
('Destornillador Phillips PH1x100mm', 'Destornillador Phillips Stanley', '7891234567904', 'DEST-005', 'Stanley', '66-056', 1300.00, 800.00, 1100.00, 12, 1, 0.13, '25x3x3'),
('Destornillador Phillips PH2x125mm', 'Destornillador Phillips Stanley', '7891234567905', 'DEST-006', 'Stanley', '66-057', 1500.00, 900.00, 1300.00, 12, 1, 0.16, '30x4x4'),
('Destornillador Phillips PH3x150mm', 'Destornillador Phillips Stanley', '7891234567906', 'DEST-007', 'Stanley', '66-058', 1700.00, 1000.00, 1500.00, 12, 1, 0.19, '35x5x5'),
('Destornillador Pozidriv PZ1x100mm', 'Destornillador Pozidriv Stanley', '7891234567907', 'DEST-008', 'Stanley', '66-059', 1400.00, 850.00, 1200.00, 12, 1, 0.13, '25x3x3'),
('Destornillador Pozidriv PZ2x125mm', 'Destornillador Pozidriv Stanley', '7891234567908', 'DEST-009', 'Stanley', '66-060', 1600.00, 950.00, 1400.00, 12, 1, 0.16, '30x4x4'),
('Destornillador Pozidriv PZ3x150mm', 'Destornillador Pozidriv Stanley', '7891234567909', 'DEST-010', 'Stanley', '66-061', 1800.00, 1100.00, 1600.00, 12, 1, 0.19, '35x5x5');

-- HERRAMIENTAS MANUALES - ALICATES
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Alicate Universal 6"', 'Alicate universal Stanley', '7891234567910', 'ALIC-001', 'Stanley', '84-496', 2800.00, 1700.00, 2400.00, 13, 1, 0.25, '20x8x3'),
('Alicate Universal 8"', 'Alicate universal Stanley', '7891234567911', 'ALIC-002', 'Stanley', '84-497', 3200.00, 1900.00, 2800.00, 13, 1, 0.35, '25x10x3'),
('Alicate Universal 10"', 'Alicate universal Stanley', '7891234567912', 'ALIC-003', 'Stanley', '84-498', 3800.00, 2300.00, 3300.00, 13, 1, 0.45, '30x12x3'),
('Alicate de Corte Diagonal 6"', 'Alicate de corte diagonal Stanley', '7891234567913', 'ALIC-004', 'Stanley', '84-499', 2500.00, 1500.00, 2200.00, 13, 1, 0.20, '18x6x2'),
('Alicate de Corte Diagonal 8"', 'Alicate de corte diagonal Stanley', '7891234567914', 'ALIC-005', 'Stanley', '84-500', 2900.00, 1700.00, 2600.00, 13, 1, 0.30, '23x8x2'),
('Alicate de Corte Diagonal 10"', 'Alicate de corte diagonal Stanley', '7891234567915', 'ALIC-006', 'Stanley', '84-501', 3500.00, 2100.00, 3100.00, 13, 1, 0.40, '28x10x2'),
('Alicate de Punta Larga 6"', 'Alicate de punta larga Stanley', '7891234567916', 'ALIC-007', 'Stanley', '84-502', 2600.00, 1600.00, 2300.00, 13, 1, 0.22, '20x6x2'),
('Alicate de Punta Larga 8"', 'Alicate de punta larga Stanley', '7891234567917', 'ALIC-008', 'Stanley', '84-503', 3000.00, 1800.00, 2700.00, 13, 1, 0.32, '25x8x2'),
('Alicate de Punta Larga 10"', 'Alicate de punta larga Stanley', '7891234567918', 'ALIC-009', 'Stanley', '84-504', 3600.00, 2200.00, 3200.00, 13, 1, 0.42, '30x10x2'),
('Alicate de Crimpar 6"', 'Alicate para crimpar terminales Stanley', '7891234567919', 'ALIC-010', 'Stanley', '84-505', 4200.00, 2500.00, 3700.00, 13, 1, 0.30, '22x8x3');

-- HERRAMIENTAS MANUALES - LLAVES
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Llave Ajustable 6"', 'Llave ajustable Stanley', '7891234567920', 'LLAV-001', 'Stanley', '84-506', 1800.00, 1100.00, 1600.00, 14, 1, 0.25, '20x8x2'),
('Llave Ajustable 8"', 'Llave ajustable Stanley', '7891234567921', 'LLAV-002', 'Stanley', '84-507', 2200.00, 1300.00, 2000.00, 14, 1, 0.35, '25x10x2'),
('Llave Ajustable 10"', 'Llave ajustable Stanley', '7891234567922', 'LLAV-003', 'Stanley', '84-508', 2800.00, 1700.00, 2500.00, 14, 1, 0.45, '30x12x2'),
('Llave Ajustable 12"', 'Llave ajustable Stanley', '7891234567923', 'LLAV-004', 'Stanley', '84-509', 3500.00, 2100.00, 3100.00, 14, 1, 0.60, '35x15x2'),
('Llave Combinada 8mm', 'Llave combinada Stanley', '7891234567924', 'LLAV-005', 'Stanley', '84-510', 800.00, 500.00, 700.00, 14, 1, 0.08, '15x8x2'),
('Llave Combinada 10mm', 'Llave combinada Stanley', '7891234567925', 'LLAV-006', 'Stanley', '84-511', 900.00, 550.00, 800.00, 14, 1, 0.10, '17x10x2'),
('Llave Combinada 12mm', 'Llave combinada Stanley', '7891234567926', 'LLAV-007', 'Stanley', '84-512', 1000.00, 600.00, 900.00, 14, 1, 0.12, '19x12x2'),
('Llave Combinada 14mm', 'Llave combinada Stanley', '7891234567927', 'LLAV-008', 'Stanley', '84-513', 1100.00, 650.00, 1000.00, 14, 1, 0.14, '21x14x2'),
('Llave Combinada 16mm', 'Llave combinada Stanley', '7891234567928', 'LLAV-009', 'Stanley', '84-514', 1200.00, 700.00, 1100.00, 14, 1, 0.16, '23x16x2'),
('Llave Combinada 18mm', 'Llave combinada Stanley', '7891234567929', 'LLAV-010', 'Stanley', '84-515', 1300.00, 750.00, 1200.00, 14, 1, 0.18, '25x18x2');

-- HERRAMIENTAS ELÉCTRICAS - TALADROS
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Taladro Eléctrico 1/2" 600W', 'Taladro eléctrico Stanley con maletín', '7891234567930', 'TAL-001', 'Stanley', 'STEL201', 45000.00, 28000.00, 38000.00, 17, 1, 2.50, '35x15x15'),
('Taladro Eléctrico 1/2" 800W', 'Taladro eléctrico Stanley profesional', '7891234567931', 'TAL-002', 'Stanley', 'STEL202', 55000.00, 34000.00, 47000.00, 17, 1, 2.80, '37x16x16'),
('Taladro Eléctrico 1/2" 1000W', 'Taladro eléctrico Stanley industrial', '7891234567932', 'TAL-003', 'Stanley', 'STEL203', 68000.00, 42000.00, 58000.00, 17, 1, 3.20, '40x18x18'),
('Taladro Atornillador 12V', 'Taladro atornillador Stanley inalámbrico', '7891234567933', 'TAL-004', 'Stanley', 'STEL204', 35000.00, 22000.00, 30000.00, 17, 1, 1.80, '25x12x12'),
('Taladro Atornillador 18V', 'Taladro atornillador Stanley inalámbrico', '7891234567934', 'TAL-005', 'Stanley', 'STEL205', 45000.00, 28000.00, 38000.00, 17, 1, 2.20, '28x14x14'),
('Taladro Atornillador 20V', 'Taladro atornillador Stanley inalámbrico', '7891234567935', 'TAL-006', 'Stanley', 'STEL206', 55000.00, 34000.00, 47000.00, 17, 1, 2.50, '30x15x15'),
('Taladro Percutor 1/2" 800W', 'Taladro percutor Stanley con maletín', '7891234567936', 'TAL-007', 'Stanley', 'STEL207', 62000.00, 38000.00, 53000.00, 17, 1, 3.50, '38x17x17'),
('Taladro Percutor 1/2" 1000W', 'Taladro percutor Stanley profesional', '7891234567937', 'TAL-008', 'Stanley', 'STEL208', 75000.00, 46000.00, 64000.00, 17, 1, 3.80, '40x18x18'),
('Taladro Percutor 1/2" 1200W', 'Taladro percutor Stanley industrial', '7891234567938', 'TAL-009', 'Stanley', 'STEL209', 88000.00, 54000.00, 75000.00, 17, 1, 4.20, '42x20x20'),
('Taladro de Banco 1/2"', 'Taladro de banco Stanley', '7891234567939', 'TAL-010', 'Stanley', 'STEL210', 95000.00, 58000.00, 80000.00, 17, 1, 25.00, '50x30x80');

-- HERRAMIENTAS ELÉCTRICAS - AMOLADORAS
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Amoladora Angular 4-1/2" 720W', 'Amoladora angular Stanley', '7891234567940', 'AMOL-001', 'Stanley', 'STEL301', 28000.00, 17000.00, 24000.00, 18, 1, 2.20, '30x15x15'),
('Amoladora Angular 4-1/2" 850W', 'Amoladora angular Stanley', '7891234567941', 'AMOL-002', 'Stanley', 'STEL302', 32000.00, 19000.00, 28000.00, 18, 1, 2.50, '32x16x16'),
('Amoladora Angular 4-1/2" 1000W', 'Amoladora angular Stanley', '7891234567942', 'AMOL-003', 'Stanley', 'STEL303', 38000.00, 23000.00, 33000.00, 18, 1, 2.80, '35x17x17'),
('Amoladora Angular 5" 1200W', 'Amoladora angular Stanley', '7891234567943', 'AMOL-004', 'Stanley', 'STEL304', 45000.00, 27000.00, 39000.00, 18, 1, 3.20, '38x18x18'),
('Amoladora Angular 5" 1400W', 'Amoladora angular Stanley', '7891234567944', 'AMOL-005', 'Stanley', 'STEL305', 52000.00, 31000.00, 45000.00, 18, 1, 3.50, '40x19x19'),
('Amoladora Angular 7" 1800W', 'Amoladora angular Stanley', '7891234567945', 'AMOL-006', 'Stanley', 'STEL306', 68000.00, 41000.00, 58000.00, 18, 1, 4.50, '45x22x22'),
('Amoladora Angular 9" 2200W', 'Amoladora angular Stanley', '7891234567946', 'AMOL-007', 'Stanley', 'STEL307', 85000.00, 52000.00, 72000.00, 18, 1, 5.80, '50x25x25'),
('Amoladora Recta 1/4" 400W', 'Amoladora recta Stanley', '7891234567947', 'AMOL-008', 'Stanley', 'STEL308', 22000.00, 13000.00, 19000.00, 18, 1, 1.80, '25x12x12'),
('Amoladora Recta 1/4" 500W', 'Amoladora recta Stanley', '7891234567948', 'AMOL-009', 'Stanley', 'STEL309', 26000.00, 16000.00, 23000.00, 18, 1, 2.00, '27x13x13'),
('Amoladora Recta 1/4" 600W', 'Amoladora recta Stanley', '7891234567949', 'AMOL-010', 'Stanley', 'STEL310', 30000.00, 18000.00, 26000.00, 18, 1, 2.20, '29x14x14');

-- PLOMERÍA - CAÑOS Y TUBERÍAS
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Caño PVC 1/2" x 3m', 'Caño PVC para agua potable', '7891234567950', 'CAÑO-001', 'Fate', 'PVC-1/2-3M', 850.00, 520.00, 720.00, 22, 2, 0.45, '300x2x2'),
('Caño PVC 3/4" x 3m', 'Caño PVC para agua potable', '7891234567951', 'CAÑO-002', 'Fate', 'PVC-3/4-3M', 1200.00, 730.00, 1020.00, 22, 2, 0.68, '300x2.5x2.5'),
('Caño PVC 1" x 3m', 'Caño PVC para agua potable', '7891234567952', 'CAÑO-003', 'Fate', 'PVC-1-3M', 1800.00, 1100.00, 1530.00, 22, 2, 1.02, '300x3x3'),
('Caño PVC 1-1/4" x 3m', 'Caño PVC para agua potable', '7891234567953', 'CAÑO-004', 'Fate', 'PVC-1-1/4-3M', 2500.00, 1500.00, 2120.00, 22, 2, 1.36, '300x3.5x3.5'),
('Caño PVC 1-1/2" x 3m', 'Caño PVC para agua potable', '7891234567954', 'CAÑO-005', 'Fate', 'PVC-1-1/2-3M', 3200.00, 1900.00, 2720.00, 22, 2, 1.70, '300x4x4'),
('Caño PVC 2" x 3m', 'Caño PVC para agua potable', '7891234567955', 'CAÑO-006', 'Fate', 'PVC-2-3M', 4500.00, 2700.00, 3820.00, 22, 2, 2.38, '300x5x5'),
('Caño PVC 3" x 3m', 'Caño PVC para agua potable', '7891234567956', 'CAÑO-007', 'Fate', 'PVC-3-3M', 6800.00, 4100.00, 5780.00, 22, 2, 3.74, '300x7x7'),
('Caño PVC 4" x 3m', 'Caño PVC para agua potable', '7891234567957', 'CAÑO-008', 'Fate', 'PVC-4-3M', 9500.00, 5700.00, 8080.00, 22, 2, 5.10, '300x9x9'),
('Caño PVC 6" x 3m', 'Caño PVC para agua potable', '7891234567958', 'CAÑO-009', 'Fate', 'PVC-6-3M', 15000.00, 9000.00, 12750.00, 22, 2, 7.65, '300x13x13'),
('Caño PVC 8" x 3m', 'Caño PVC para agua potable', '7891234567959', 'CAÑO-010', 'Fate', 'PVC-8-3M', 22000.00, 13200.00, 18700.00, 22, 2, 10.20, '300x17x17');

-- PLOMERÍA - CONEXIONES
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Codo PVC 90° 1/2"', 'Codo PVC 90 grados', '7891234567960', 'CONEX-001', 'Fate', 'CODO-1/2-90', 180.00, 110.00, 153.00, 23, 1, 0.05, '5x5x5'),
('Codo PVC 90° 3/4"', 'Codo PVC 90 grados', '7891234567961', 'CONEX-002', 'Fate', 'CODO-3/4-90', 250.00, 150.00, 212.00, 23, 1, 0.08, '6x6x6'),
('Codo PVC 90° 1"', 'Codo PVC 90 grados', '7891234567962', 'CONEX-003', 'Fate', 'CODO-1-90', 350.00, 210.00, 297.00, 23, 1, 0.12, '7x7x7'),
('Codo PVC 90° 1-1/4"', 'Codo PVC 90 grados', '7891234567963', 'CONEX-004', 'Fate', 'CODO-1-1/4-90', 480.00, 290.00, 408.00, 23, 1, 0.18, '8x8x8'),
('Codo PVC 90° 1-1/2"', 'Codo PVC 90 grados', '7891234567964', 'CONEX-005', 'Fate', 'CODO-1-1/2-90', 620.00, 370.00, 527.00, 23, 1, 0.25, '9x9x9'),
('Tee PVC 1/2"', 'Tee PVC', '7891234567965', 'CONEX-006', 'Fate', 'TEE-1/2', 220.00, 130.00, 187.00, 23, 1, 0.07, '6x6x6'),
('Tee PVC 3/4"', 'Tee PVC', '7891234567966', 'CONEX-007', 'Fate', 'TEE-3/4', 300.00, 180.00, 255.00, 23, 1, 0.10, '7x7x7'),
('Tee PVC 1"', 'Tee PVC', '7891234567967', 'CONEX-008', 'Fate', 'TEE-1', 420.00, 250.00, 357.00, 23, 1, 0.15, '8x8x8'),
('Tee PVC 1-1/4"', 'Tee PVC', '7891234567968', 'CONEX-009', 'Fate', 'TEE-1-1/4', 580.00, 350.00, 493.00, 23, 1, 0.22, '9x9x9'),
('Tee PVC 1-1/2"', 'Tee PVC', '7891234567969', 'CONEX-010', 'Fate', 'TEE-1-1/2', 750.00, 450.00, 637.00, 23, 1, 0.30, '10x10x10');

-- ELECTRICIDAD - CABLES
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Cable NYM 3x1.5mm² x 100m', 'Cable NYM 3 conductores', '7891234567970', 'CABLE-001', 'Pirelli', 'NYM-3x1.5-100', 8500.00, 5100.00, 7225.00, 27, 2, 8.50, '100x0.5x0.5'),
('Cable NYM 3x2.5mm² x 100m', 'Cable NYM 3 conductores', '7891234567971', 'CABLE-002', 'Pirelli', 'NYM-3x2.5-100', 12000.00, 7200.00, 10200.00, 27, 2, 12.00, '100x0.6x0.6'),
('Cable NYM 3x4mm² x 100m', 'Cable NYM 3 conductores', '7891234567972', 'CABLE-003', 'Pirelli', 'NYM-3x4-100', 18000.00, 10800.00, 15300.00, 27, 2, 18.00, '100x0.8x0.8'),
('Cable NYM 3x6mm² x 100m', 'Cable NYM 3 conductores', '7891234567973', 'CABLE-004', 'Pirelli', 'NYM-3x6-100', 25000.00, 15000.00, 21250.00, 27, 2, 25.00, '100x1.0x1.0'),
('Cable NYM 3x10mm² x 100m', 'Cable NYM 3 conductores', '7891234567974', 'CABLE-005', 'Pirelli', 'NYM-3x10-100', 38000.00, 22800.00, 32300.00, 27, 2, 38.00, '100x1.2x1.2'),
('Cable NYM 3x16mm² x 100m', 'Cable NYM 3 conductores', '7891234567975', 'CABLE-006', 'Pirelli', 'NYM-3x16-100', 55000.00, 33000.00, 46750.00, 27, 2, 55.00, '100x1.5x1.5'),
('Cable NYM 3x25mm² x 100m', 'Cable NYM 3 conductores', '7891234567976', 'CABLE-007', 'Pirelli', 'NYM-3x25-100', 85000.00, 51000.00, 72250.00, 27, 2, 85.00, '100x2.0x2.0'),
('Cable NYM 3x35mm² x 100m', 'Cable NYM 3 conductores', '7891234567977', 'CABLE-008', 'Pirelli', 'NYM-3x35-100', 120000.00, 72000.00, 102000.00, 27, 2, 120.00, '100x2.5x2.5'),
('Cable NYM 3x50mm² x 100m', 'Cable NYM 3 conductores', '7891234567978', 'CABLE-009', 'Pirelli', 'NYM-3x50-100', 180000.00, 108000.00, 153000.00, 27, 2, 180.00, '100x3.0x3.0'),
('Cable NYM 3x70mm² x 100m', 'Cable NYM 3 conductores', '7891234567979', 'CABLE-010', 'Pirelli', 'NYM-3x70-100', 250000.00, 150000.00, 212500.00, 27, 2, 250.00, '100x3.5x3.5');

-- PINTURAS Y ACCESORIOS
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Pintura Interior Látex 4L Blanco', 'Pintura látex para interiores', '7891234567980', 'PINT-001', 'Alba', 'LATEX-INT-4L-BLANCO', 8500.00, 5100.00, 7225.00, 5, 7, 4.50, '20x15x15'),
('Pintura Interior Látex 4L Beige', 'Pintura látex para interiores', '7891234567981', 'PINT-002', 'Alba', 'LATEX-INT-4L-BEIGE', 8500.00, 5100.00, 7225.00, 5, 7, 4.50, '20x15x15'),
('Pintura Interior Látex 4L Gris', 'Pintura látex para interiores', '7891234567982', 'PINT-003', 'Alba', 'LATEX-INT-4L-GRIS', 8500.00, 5100.00, 7225.00, 5, 7, 4.50, '20x15x15'),
('Pintura Exterior Látex 4L Blanco', 'Pintura látex para exteriores', '7891234567983', 'PINT-004', 'Alba', 'LATEX-EXT-4L-BLANCO', 12000.00, 7200.00, 10200.00, 5, 7, 4.50, '20x15x15'),
('Pintura Exterior Látex 4L Beige', 'Pintura látex para exteriores', '7891234567984', 'PINT-005', 'Alba', 'LATEX-EXT-4L-BEIGE', 12000.00, 7200.00, 10200.00, 5, 7, 4.50, '20x15x15'),
('Pintura Exterior Látex 4L Gris', 'Pintura látex para exteriores', '7891234567985', 'PINT-006', 'Alba', 'LATEX-EXT-4L-GRIS', 12000.00, 7200.00, 10200.00, 5, 7, 4.50, '20x15x15'),
('Esmalte Sintético 1L Blanco', 'Esmalte sintético', '7891234567986', 'PINT-007', 'Alba', 'ESMALTE-1L-BLANCO', 3500.00, 2100.00, 2975.00, 5, 7, 1.20, '10x8x8'),
('Esmalte Sintético 1L Negro', 'Esmalte sintético', '7891234567987', 'PINT-008', 'Alba', 'ESMALTE-1L-NEGRO', 3500.00, 2100.00, 2975.00, 5, 7, 1.20, '10x8x8'),
('Esmalte Sintético 1L Rojo', 'Esmalte sintético', '7891234567988', 'PINT-009', 'Alba', 'ESMALTE-1L-ROJO', 3500.00, 2100.00, 2975.00, 5, 7, 1.20, '10x8x8'),
('Esmalte Sintético 1L Azul', 'Esmalte sintético', '7891234567989', 'PINT-010', 'Alba', 'ESMALTE-1L-AZUL', 3500.00, 2100.00, 2975.00, 5, 7, 1.20, '10x8x8');

-- =====================================================
-- 6. INSERTAR CLIENTES REALES
-- =====================================================

-- Clientes Consumidor Final
INSERT INTO Clientes (Nombre, Apellido, CUIT_CUIL, Tipo_Cliente, Condicion_IVA, Direccion, Localidad, Provincia, Codigo_Postal, Telefono, Telefono_Alternativo, Email, Fecha_Nacimiento, Genero, Limite_Credito, Saldo_Actual) VALUES 
('Juan Carlos', 'González', '20-12345678-9', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Corrientes 1234', 'Buenos Aires', 'Buenos Aires', '1043', '011-4321-5678', '011-4321-5679', 'juan.gonzalez@email.com', '1985-03-15', 'M', 50000.00, 0.00),
('María Elena', 'Rodríguez', '27-23456789-0', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Santa Fe 2345', 'Buenos Aires', 'Buenos Aires', '1125', '011-4321-5680', '011-4321-5681', 'maria.rodriguez@email.com', '1990-07-22', 'F', 30000.00, 0.00),
('Carlos Alberto', 'López', '20-34567890-1', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Almirante Brown 3456', 'Buenos Aires', 'Buenos Aires', '1160', '011-4321-5682', '011-4321-5683', 'carlos.lopez@email.com', '1982-11-08', 'M', 40000.00, 0.00),
('Ana Sofía', 'Martínez', '27-45678901-2', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Rivadavia 4567', 'Buenos Aires', 'Buenos Aires', '1408', '011-4321-5684', '011-4321-5685', 'ana.martinez@email.com', '1988-05-12', 'F', 25000.00, 0.00),
('Roberto Daniel', 'García', '20-56789012-3', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Alicia Moreau de Justo 5678', 'Buenos Aires', 'Buenos Aires', '1107', '011-4321-5686', '011-4321-5687', 'roberto.garcia@email.com', '1975-09-30', 'M', 60000.00, 0.00),
('Laura Beatriz', 'Fernández', '27-67890123-4', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Colón 6789', 'Córdoba', 'Córdoba', '5000', '0351-4321-5678', '0351-4321-5679', 'laura.fernandez@email.com', '1992-01-18', 'F', 35000.00, 0.00),
('Miguel Ángel', 'Pérez', '20-78901234-5', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Pellegrini 7890', 'Rosario', 'Santa Fe', '2000', '0341-4321-5678', '0341-4321-5679', 'miguel.perez@email.com', '1987-12-03', 'M', 45000.00, 0.00),
('Silvia Marcela', 'Gómez', '27-89012345-6', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. San Martín 8901', 'Mendoza', 'Mendoza', '5500', '0261-4321-5678', '0261-4321-5679', 'silvia.gomez@email.com', '1983-06-25', 'F', 40000.00, 0.00),
('Fernando José', 'Díaz', '20-90123456-7', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Sarmiento 9012', 'San Miguel de Tucumán', 'Tucumán', '4000', '0381-4321-5678', '0381-4321-5679', 'fernando.diaz@email.com', '1989-08-14', 'M', 30000.00, 0.00),
('Patricia Alejandra', 'Torres', '27-01234567-8', 'Consumidor Final', 'IVA Responsable Inscripto', 'Av. Independencia 0123', 'Mar del Plata', 'Buenos Aires', '7600', '0223-4321-5678', '0223-4321-5679', 'patricia.torres@email.com', '1991-04-07', 'F', 35000.00, 0.00);

-- Clientes Responsable Inscripto
INSERT INTO Clientes (Nombre, Apellido, CUIT_CUIL, Tipo_Cliente, Condicion_IVA, Direccion, Localidad, Provincia, Codigo_Postal, Telefono, Telefono_Alternativo, Email, Limite_Credito, Saldo_Actual) VALUES 
('Constructora del Sur S.A.', '', '30-12345678-9', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. 9 de Julio 1234', 'Buenos Aires', 'Buenos Aires', '1043', '011-4321-6000', '011-4321-6001', 'info@constructoradelsur.com', 500000.00, 0.00),
('Electroinstalaciones Norte S.R.L.', '', '30-23456789-0', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Libertador 2345', 'Buenos Aires', 'Buenos Aires', '1125', '011-4321-6002', '011-4321-6003', 'info@electroinstalacionesnorte.com', 300000.00, 0.00),
('Plomería Express S.A.', '', '30-34567890-1', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Córdoba 3456', 'Buenos Aires', 'Buenos Aires', '1160', '011-4321-6004', '011-4321-6005', 'info@plomeriaexpress.com', 200000.00, 0.00),
('Pinturas y Decoraciones S.R.L.', '', '30-45678901-2', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Belgrano 4567', 'Buenos Aires', 'Buenos Aires', '1408', '011-4321-6006', '011-4321-6007', 'info@pinturasdecoraciones.com', 150000.00, 0.00),
('Herramientas Profesionales S.A.', '', '30-56789012-3', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. San Juan 5678', 'Buenos Aires', 'Buenos Aires', '1107', '011-4321-6008', '011-4321-6009', 'info@herramientasprofesionales.com', 400000.00, 0.00),
('Construcciones Córdoba S.A.', '', '30-67890123-4', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Hipólito Yrigoyen 6789', 'Córdoba', 'Córdoba', '5000', '0351-4321-6000', '0351-4321-6001', 'info@construccionescordoba.com', 350000.00, 0.00),
('Instalaciones Rosario S.R.L.', '', '30-78901234-5', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Oroño 7890', 'Rosario', 'Santa Fe', '2000', '0341-4321-6000', '0341-4321-6001', 'info@instalacionesrosario.com', 250000.00, 0.00),
('Mantenimiento Mendoza S.A.', '', '30-89012345-6', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Las Heras 8901', 'Mendoza', 'Mendoza', '5500', '0261-4321-6000', '0261-4321-6001', 'info@mantenimientomendoza.com', 200000.00, 0.00),
('Servicios Tucumán S.R.L.', '', '30-90123456-7', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Sarmiento 9012', 'San Miguel de Tucumán', 'Tucumán', '4000', '0381-4321-6000', '0381-4321-6001', 'info@serviciostucuman.com', 180000.00, 0.00),
('Construcciones Mar del Plata S.A.', '', '30-01234567-8', 'Responsable Inscripto', 'IVA Responsable Inscripto', 'Av. Luro 0123', 'Mar del Plata', 'Buenos Aires', '7600', '0223-4321-6000', '0223-4321-6001', 'info@construccionesmardelplata.com', 300000.00, 0.00);

-- =====================================================
-- 7. INSERTAR PROVEEDORES REALES
-- =====================================================

INSERT INTO Proveedores (Nombre, CUIT, Condicion_IVA, Direccion, Localidad, Provincia, Codigo_Postal, Telefono, Telefono_Alternativo, Email, Contacto_Persona, Plazo_Entrega) VALUES 
('Stanley Black & Decker Argentina S.A.', '30-12345678-9', 'IVA Responsable Inscripto', 'Av. del Libertador 1234', 'Buenos Aires', 'Buenos Aires', '1425', '011-4321-7000', '011-4321-7001', 'ventas@stanley.com.ar', 'Juan Pérez', 7),
('Fate S.A.', '30-23456789-0', 'IVA Responsable Inscripto', 'Av. Corrientes 2345', 'Buenos Aires', 'Buenos Aires', '1043', '011-4321-7002', '011-4321-7003', 'ventas@fate.com.ar', 'María González', 5),
('Pirelli Argentina S.A.', '30-34567890-1', 'IVA Responsable Inscripto', 'Av. Santa Fe 3456', 'Buenos Aires', 'Buenos Aires', '1125', '011-4321-7004', '011-4321-7005', 'ventas@pirelli.com.ar', 'Carlos López', 7),
('Alba Pinturas S.A.', '30-45678901-2', 'IVA Responsable Inscripto', 'Av. Belgrano 4567', 'Buenos Aires', 'Buenos Aires', '1408', '011-4321-7006', '011-4321-7007', 'ventas@alba.com.ar', 'Ana Martínez', 3),
('Siderar S.A.', '30-56789012-3', 'IVA Responsable Inscripto', 'Av. San Juan 5678', 'Buenos Aires', 'Buenos Aires', '1107', '011-4321-7008', '011-4321-7009', 'ventas@siderar.com.ar', 'Roberto García', 10),
('Loma Negra S.A.', '30-67890123-4', 'IVA Responsable Inscripto', 'Av. 9 de Julio 6789', 'Buenos Aires', 'Buenos Aires', '1043', '011-4321-7010', '011-4321-7011', 'ventas@lomanegra.com.ar', 'Laura Fernández', 7),
('Holcim Argentina S.A.', '30-78901234-5', 'IVA Responsable Inscripto', 'Av. Libertador 7890', 'Buenos Aires', 'Buenos Aires', '1125', '011-4321-7012', '011-4321-7013', 'ventas@holcim.com.ar', 'Miguel Pérez', 5),
('Cementos Avellaneda S.A.', '30-89012345-6', 'IVA Responsable Inscripto', 'Av. Córdoba 8901', 'Buenos Aires', 'Buenos Aires', '1160', '011-4321-7014', '011-4321-7015', 'ventas@cementosavellaneda.com.ar', 'Silvia Gómez', 7),
('Petrobras Argentina S.A.', '30-90123456-7', 'IVA Responsable Inscripto', 'Av. Rivadavia 9012', 'Buenos Aires', 'Buenos Aires', '1408', '011-4321-7016', '011-4321-7017', 'ventas@petrobras.com.ar', 'Fernando Díaz', 3),
('YPF S.A.', '30-01234567-8', 'IVA Responsable Inscripto', 'Av. Alicia Moreau de Justo 0123', 'Buenos Aires', 'Buenos Aires', '1107', '011-4321-7018', '011-4321-7019', 'ventas@ypf.com.ar', 'Patricia Torres', 2);

-- =====================================================
-- 8. INSERTAR INVENTARIO INICIAL
-- =====================================================

-- Inventario para Sucursal 1 (Microcentro)
INSERT INTO Inventario (ID_Producto, ID_Sucursal, Stock_Actual, Stock_Minimo, Stock_Maximo, Ubicacion) VALUES 
(1, 1, 50, 10, 100, 'Pasillo A - Estante 1'),
(2, 1, 45, 8, 80, 'Pasillo A - Estante 1'),
(3, 1, 40, 5, 70, 'Pasillo A - Estante 1'),
(4, 1, 35, 5, 60, 'Pasillo A - Estante 1'),
(5, 1, 30, 5, 50, 'Pasillo A - Estante 1'),
(6, 1, 25, 3, 40, 'Pasillo A - Estante 2'),
(7, 1, 20, 3, 35, 'Pasillo A - Estante 2'),
(8, 1, 40, 8, 70, 'Pasillo A - Estante 2'),
(9, 1, 35, 6, 60, 'Pasillo A - Estante 2'),
(10, 1, 15, 2, 25, 'Pasillo A - Estante 3'),
(11, 1, 60, 15, 120, 'Pasillo B - Estante 1'),
(12, 1, 55, 12, 100, 'Pasillo B - Estante 1'),
(13, 1, 50, 10, 90, 'Pasillo B - Estante 1'),
(14, 1, 45, 8, 80, 'Pasillo B - Estante 1'),
(15, 1, 40, 6, 70, 'Pasillo B - Estante 1'),
(16, 1, 35, 5, 60, 'Pasillo B - Estante 2'),
(17, 1, 30, 5, 50, 'Pasillo B - Estante 2'),
(18, 1, 25, 3, 40, 'Pasillo B - Estante 2'),
(19, 1, 20, 3, 35, 'Pasillo B - Estante 2'),
(20, 1, 15, 2, 25, 'Pasillo B - Estante 3');

-- Inventario para Sucursal 2 (Palermo)
INSERT INTO Inventario (ID_Producto, ID_Sucursal, Stock_Actual, Stock_Minimo, Stock_Maximo, Ubicacion) VALUES 
(1, 2, 40, 8, 80, 'Pasillo A - Estante 1'),
(2, 2, 35, 6, 70, 'Pasillo A - Estante 1'),
(3, 2, 30, 5, 60, 'Pasillo A - Estante 1'),
(4, 2, 25, 4, 50, 'Pasillo A - Estante 1'),
(5, 2, 20, 3, 40, 'Pasillo A - Estante 1'),
(6, 2, 15, 2, 30, 'Pasillo A - Estante 2'),
(7, 2, 10, 2, 25, 'Pasillo A - Estante 2'),
(8, 2, 30, 6, 60, 'Pasillo A - Estante 2'),
(9, 2, 25, 5, 50, 'Pasillo A - Estante 2'),
(10, 2, 10, 1, 20, 'Pasillo A - Estante 3'),
(11, 2, 50, 12, 100, 'Pasillo B - Estante 1'),
(12, 2, 45, 10, 90, 'Pasillo B - Estante 1'),
(13, 2, 40, 8, 80, 'Pasillo B - Estante 1'),
(14, 2, 35, 6, 70, 'Pasillo B - Estante 1'),
(15, 2, 30, 5, 60, 'Pasillo B - Estante 1'),
(16, 2, 25, 4, 50, 'Pasillo B - Estante 2'),
(17, 2, 20, 3, 40, 'Pasillo B - Estante 2'),
(18, 2, 15, 2, 30, 'Pasillo B - Estante 2'),
(19, 2, 10, 2, 25, 'Pasillo B - Estante 2'),
(20, 2, 8, 1, 15, 'Pasillo B - Estante 3');

-- Inventario para Sucursal 3 (La Boca)
INSERT INTO Inventario (ID_Producto, ID_Sucursal, Stock_Actual, Stock_Minimo, Stock_Maximo, Ubicacion) VALUES 
(1, 3, 35, 7, 70, 'Pasillo A - Estante 1'),
(2, 3, 30, 5, 60, 'Pasillo A - Estante 1'),
(3, 3, 25, 4, 50, 'Pasillo A - Estante 1'),
(4, 3, 20, 3, 40, 'Pasillo A - Estante 1'),
(5, 3, 15, 2, 30, 'Pasillo A - Estante 1'),
(6, 3, 12, 2, 25, 'Pasillo A - Estante 2'),
(7, 3, 8, 1, 20, 'Pasillo A - Estante 2'),
(8, 3, 25, 5, 50, 'Pasillo A - Estante 2'),
(9, 3, 20, 4, 40, 'Pasillo A - Estante 2'),
(10, 3, 8, 1, 15, 'Pasillo A - Estante 3'),
(11, 3, 45, 10, 90, 'Pasillo B - Estante 1'),
(12, 3, 40, 8, 80, 'Pasillo B - Estante 1'),
(13, 3, 35, 6, 70, 'Pasillo B - Estante 1'),
(14, 3, 30, 5, 60, 'Pasillo B - Estante 1'),
(15, 3, 25, 4, 50, 'Pasillo B - Estante 1'),
(16, 3, 20, 3, 40, 'Pasillo B - Estante 2'),
(17, 3, 15, 2, 30, 'Pasillo B - Estante 2'),
(18, 3, 12, 2, 25, 'Pasillo B - Estante 2'),
(19, 3, 8, 1, 20, 'Pasillo B - Estante 2'),
(20, 3, 6, 1, 12, 'Pasillo B - Estante 3');

-- =====================================================
-- 9. INSERTAR FACTURAS DE VENTA REALES
-- =====================================================

-- Factura 1 - Cliente Consumidor Final
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('A-0001-00000001', 1, 1, '2024-01-15 10:30:00', 'A', 'IVA Responsable Inscripto', 15000.00, 3150.00, 0.00, 18150.00, 2, 'Pagada', 'Efectivo');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(1, 1, 2, 4500.00, 0.00, 9000.00),
(1, 11, 3, 1200.00, 0.00, 3600.00),
(1, 21, 1, 2400.00, 0.00, 2400.00);

-- Factura 2 - Cliente Responsable Inscripto
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('A-0001-00000002', 11, 1, '2024-01-15 14:20:00', 'A', 'IVA Responsable Inscripto', 85000.00, 17850.00, 5000.00, 97850.00, 2, 'Pagada', 'Transferencia');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(2, 30, 1, 45000.00, 0.00, 45000.00),
(2, 40, 1, 28000.00, 0.00, 28000.00),
(2, 50, 10, 1200.00, 0.00, 12000.00);

-- Factura 3 - Cliente Consumidor Final
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('B-0001-00000003', 2, 2, '2024-01-16 09:15:00', 'B', 'IVA Responsable Inscripto', 8500.00, 0.00, 0.00, 8500.00, 5, 'Pagada', 'Tarjeta');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(3, 2, 1, 5200.00, 0.00, 5200.00),
(3, 12, 2, 1300.00, 0.00, 2600.00),
(3, 22, 1, 700.00, 0.00, 700.00);

-- Factura 4 - Cliente Responsable Inscripto
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('A-0001-00000004', 12, 2, '2024-01-16 16:45:00', 'A', 'IVA Responsable Inscripto', 120000.00, 25200.00, 8000.00, 137200.00, 5, 'Pagada', 'Cheque');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(4, 70, 5, 8500.00, 0.00, 42500.00),
(4, 80, 3, 8500.00, 0.00, 25500.00),
(4, 90, 20, 2600.00, 0.00, 52000.00);

-- Factura 5 - Cliente Consumidor Final
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('B-0001-00000005', 3, 3, '2024-01-17 11:30:00', 'B', 'IVA Responsable Inscripto', 12500.00, 0.00, 1000.00, 11500.00, 8, 'Pagada', 'Efectivo');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(5, 3, 1, 5800.00, 0.00, 5800.00),
(5, 13, 3, 1500.00, 0.00, 4500.00),
(5, 23, 2, 1100.00, 0.00, 2200.00);

-- =====================================================
-- 10. INSERTAR PAGOS
-- =====================================================

INSERT INTO Pagos (ID_Factura_Venta, Metodo, Monto, Numero_Comprobante, ID_Usuario) VALUES 
(1, 'Efectivo', 18150.00, 'EF-001', 2),
(2, 'Transferencia', 97850.00, 'TR-001', 2),
(3, 'Tarjeta', 8500.00, 'TARJ-001', 5),
(4, 'Cheque', 137200.00, 'CH-001', 5),
(5, 'Efectivo', 11500.00, 'EF-002', 8);

-- =====================================================
-- 11. INSERTAR ÓRDENES DE COMPRA
-- =====================================================

-- Orden de Compra 1
INSERT INTO Ordenes_Compra (Numero_OC, ID_Proveedor, ID_Sucursal, Fecha, Fecha_Entrega_Esperada, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado) VALUES 
('OC-2024-001', 1, 1, '2024-01-10 09:00:00', '2024-01-17', 500000.00, 105000.00, 25000.00, 580000.00, 1, 'Recibida');

INSERT INTO Detalle_OC (ID_OC, ID_Producto, Cantidad, Costo_Unitario, Descuento_Unitario, Subtotal) VALUES 
(1, 1, 100, 2800.00, 0.00, 280000.00),
(1, 2, 80, 3200.00, 0.00, 256000.00),
(1, 11, 200, 750.00, 0.00, 150000.00),
(1, 12, 150, 850.00, 0.00, 127500.00);

-- Orden de Compra 2
INSERT INTO Ordenes_Compra (Numero_OC, ID_Proveedor, ID_Sucursal, Fecha, Fecha_Entrega_Esperada, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado) VALUES 
('OC-2024-002', 2, 1, '2024-01-12 10:30:00', '2024-01-17', 300000.00, 63000.00, 15000.00, 348000.00, 1, 'Recibida');

INSERT INTO Detalle_OC (ID_OC, ID_Producto, Cantidad, Costo_Unitario, Descuento_Unitario, Subtotal) VALUES 
(2, 50, 200, 520.00, 0.00, 104000.00),
(2, 51, 150, 730.00, 0.00, 109500.00),
(2, 52, 100, 1100.00, 0.00, 110000.00),
(2, 60, 300, 110.00, 0.00, 33000.00),
(2, 61, 250, 150.00, 0.00, 37500.00);

-- Orden de Compra 3
INSERT INTO Ordenes_Compra (Numero_OC, ID_Proveedor, ID_Sucursal, Fecha, Fecha_Entrega_Esperada, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado) VALUES 
('OC-2024-003', 3, 2, '2024-01-14 14:00:00', '2024-01-21', 400000.00, 84000.00, 20000.00, 464000.00, 1, 'Aprobada');

INSERT INTO Detalle_OC (ID_OC, ID_Producto, Cantidad, Costo_Unitario, Descuento_Unitario, Subtotal) VALUES 
(3, 70, 50, 5100.00, 0.00, 255000.00),
(3, 71, 40, 7200.00, 0.00, 288000.00),
(3, 72, 30, 10800.00, 0.00, 324000.00),
(3, 73, 20, 15000.00, 0.00, 300000.00);

-- =====================================================
-- 12. INSERTAR MOVIMIENTOS DE INVENTARIO
-- =====================================================

-- Movimientos por compras
INSERT INTO Movimientos_Inventario (ID_Producto, ID_Sucursal, Fecha, Tipo, Cantidad, Costo_Unitario, ID_Usuario, ID_Referencia, Tipo_Referencia) VALUES 
(1, 1, '2024-01-17 08:00:00', 'Compra', 100, 2800.00, 1, 1, 'OC'),
(2, 1, '2024-01-17 08:00:00', 'Compra', 80, 3200.00, 1, 1, 'OC'),
(11, 1, '2024-01-17 08:00:00', 'Compra', 200, 750.00, 1, 1, 'OC'),
(12, 1, '2024-01-17 08:00:00', 'Compra', 150, 850.00, 1, 1, 'OC'),
(50, 1, '2024-01-17 08:00:00', 'Compra', 200, 520.00, 1, 2, 'OC'),
(51, 1, '2024-01-17 08:00:00', 'Compra', 150, 730.00, 1, 2, 'OC'),
(52, 1, '2024-01-17 08:00:00', 'Compra', 100, 1100.00, 1, 2, 'OC'),
(60, 1, '2024-01-17 08:00:00', 'Compra', 300, 110.00, 1, 2, 'OC'),
(61, 1, '2024-01-17 08:00:00', 'Compra', 250, 150.00, 1, 2, 'OC');

-- Movimientos por ventas
INSERT INTO Movimientos_Inventario (ID_Producto, ID_Sucursal, Fecha, Tipo, Cantidad, Costo_Unitario, ID_Usuario, ID_Referencia, Tipo_Referencia) VALUES 
(1, 1, '2024-01-15 10:30:00', 'Venta', -2, 2800.00, 2, 1, 'Factura'),
(11, 1, '2024-01-15 10:30:00', 'Venta', -3, 750.00, 2, 1, 'Factura'),
(21, 1, '2024-01-15 10:30:00', 'Venta', -1, 1200.00, 2, 1, 'Factura'),
(30, 1, '2024-01-15 14:20:00', 'Venta', -1, 28000.00, 2, 2, 'Factura'),
(40, 1, '2024-01-15 14:20:00', 'Venta', -1, 18000.00, 2, 2, 'Factura'),
(50, 1, '2024-01-15 14:20:00', 'Venta', -10, 520.00, 2, 2, 'Factura'),
(2, 2, '2024-01-16 09:15:00', 'Venta', -1, 3200.00, 5, 3, 'Factura'),
(12, 2, '2024-01-16 09:15:00', 'Venta', -2, 850.00, 5, 3, 'Factura'),
(22, 2, '2024-01-16 09:15:00', 'Venta', -1, 450.00, 5, 3, 'Factura'),
(70, 2, '2024-01-16 16:45:00', 'Venta', -5, 5100.00, 5, 4, 'Factura'),
(80, 2, '2024-01-16 16:45:00', 'Venta', -3, 5100.00, 5, 4, 'Factura'),
(90, 2, '2024-01-16 16:45:00', 'Venta', -20, 7200.00, 5, 4, 'Factura'),
(3, 3, '2024-01-17 11:30:00', 'Venta', -1, 3600.00, 8, 5, 'Factura'),
(13, 3, '2024-01-17 11:30:00', 'Venta', -3, 950.00, 8, 5, 'Factura'),
(23, 3, '2024-01-17 11:30:00', 'Venta', -2, 600.00, 8, 5, 'Factura');

-- =====================================================
-- 13. INSERTAR GARANTÍAS
-- =====================================================

INSERT INTO Garantias (ID_Producto, Tiempo_Garantia, Tipo_Garantia, Descripcion) VALUES 
(30, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(31, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(32, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(33, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(34, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(35, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(36, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(37, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(38, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(39, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(40, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(41, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(42, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(43, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(44, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(45, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(46, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(47, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(48, 365, 'Fábrica', 'Garantía de fábrica por 1 año'),
(49, 365, 'Fábrica', 'Garantía de fábrica por 1 año');

-- =====================================================
-- 14. INSERTAR DESCUENTOS
-- =====================================================

INSERT INTO Descuentos (Nombre, Descripcion, Porcentaje, Tipo_Descuento, Fecha_Inicio, Fecha_Fin, Cantidad_Minima, Cantidad_Maxima) VALUES 
('Descuento por Volumen', 'Descuento del 10% en compras mayores a $50,000', 10.00, 'Porcentaje', '2024-01-01', '2024-12-31', 50000, NULL),
('Descuento Herramientas Eléctricas', 'Descuento del 15% en herramientas eléctricas', 15.00, 'Porcentaje', '2024-01-01', '2024-12-31', NULL, NULL),
('Descuento Pinturas', 'Descuento del 20% en pinturas', 20.00, 'Porcentaje', '2024-01-01', '2024-12-31', NULL, NULL),
('Descuento Mayorista', 'Descuento del 25% para clientes mayoristas', 25.00, 'Porcentaje', '2024-01-01', '2024-12-31', 100000, NULL),
('Descuento Fin de Mes', 'Descuento del 5% en los últimos 3 días del mes', 5.00, 'Porcentaje', '2024-01-01', '2024-12-31', NULL, NULL);

-- Aplicar descuentos a productos
INSERT INTO Productos_Descuentos (ID_Producto, ID_Descuento) VALUES 
(30, 2), (31, 2), (32, 2), (33, 2), (34, 2), (35, 2), (36, 2), (37, 2), (38, 2), (39, 2), (40, 2), (41, 2), (42, 2), (43, 2), (44, 2), (45, 2), (46, 2), (47, 2), (48, 2), (49, 2),
(80, 3), (81, 3), (82, 3), (83, 3), (84, 3), (85, 3), (86, 3), (87, 3), (88, 3), (89, 3);

-- =====================================================
-- 15. INSERTAR MÁS PRODUCTOS (CONSTRUCCIÓN)
-- =====================================================

-- Materiales de Construcción
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Cemento Portland 50kg', 'Cemento Portland tipo I', '7891234568000', 'CEMENTO-001', 'Loma Negra', 'PORTLAND-50KG', 4500.00, 2700.00, 3825.00, 6, 5, 50.00, '40x30x15'),
('Cemento Portland 25kg', 'Cemento Portland tipo I', '7891234568001', 'CEMENTO-002', 'Loma Negra', 'PORTLAND-25KG', 2500.00, 1500.00, 2125.00, 6, 5, 25.00, '30x20x10'),
('Cal Hidráulica 25kg', 'Cal hidráulica para construcción', '7891234568002', 'CAL-001', 'Loma Negra', 'CAL-25KG', 1800.00, 1080.00, 1530.00, 6, 5, 25.00, '30x20x10'),
('Arena Fina 1m³', 'Arena fina para construcción', '7891234568003', 'ARENA-001', 'Local', 'ARENA-FINA-1M3', 8500.00, 5100.00, 7225.00, 6, 3, 1500.00, '100x100x100'),
('Piedra 1m³', 'Piedra para construcción', '7891234568004', 'PIEDRA-001', 'Local', 'PIEDRA-1M3', 12000.00, 7200.00, 10200.00, 6, 3, 2000.00, '100x100x100'),
('Ladrillo Común 1000u', 'Ladrillos comunes', '7891234568005', 'LADRILLO-001', 'Local', 'LADRILLO-COMUN-1000', 45000.00, 27000.00, 38250.00, 6, 30, 2500.00, '200x100x50'),
('Ladrillo Hueco 8x18x33 100u', 'Ladrillos huecos 8x18x33', '7891234568006', 'LADRILLO-002', 'Local', 'LADRILLO-HUECO-100', 8500.00, 5100.00, 7225.00, 6, 30, 800.00, '100x50x30'),
('Ladrillo Hueco 12x18x33 100u', 'Ladrillos huecos 12x18x33', '7891234568007', 'LADRILLO-003', 'Local', 'LADRILLO-HUECO-12-100', 12000.00, 7200.00, 10200.00, 6, 30, 1200.00, '120x60x40'),
('Ladrillo Hueco 15x18x33 100u', 'Ladrillos huecos 15x18x33', '7891234568008', 'LADRILLO-004', 'Local', 'LADRILLO-HUECO-15-100', 15000.00, 9000.00, 12750.00, 6, 30, 1500.00, '150x70x50'),
('Ladrillo Hueco 20x18x33 100u', 'Ladrillos huecos 20x18x33', '7891234568009', 'LADRILLO-005', 'Local', 'LADRILLO-HUECO-20-100', 18000.00, 10800.00, 15300.00, 6, 30, 1800.00, '180x80x60');

-- Hierros y Aceros
INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Hierro 6mm x 6m', 'Hierro redondo 6mm x 6 metros', '7891234568010', 'HIERRO-001', 'Siderar', 'HIERRO-6MM-6M', 1200.00, 720.00, 1020.00, 6, 2, 1.33, '600x0.6x0.6'),
('Hierro 8mm x 6m', 'Hierro redondo 8mm x 6 metros', '7891234568011', 'HIERRO-002', 'Siderar', 'HIERRO-8MM-6M', 1800.00, 1080.00, 1530.00, 6, 2, 2.37, '600x0.8x0.8'),
('Hierro 10mm x 6m', 'Hierro redondo 10mm x 6 metros', '7891234568012', 'HIERRO-003', 'Siderar', 'HIERRO-10MM-6M', 2800.00, 1680.00, 2380.00, 6, 2, 3.70, '600x1.0x1.0'),
('Hierro 12mm x 6m', 'Hierro redondo 12mm x 6 metros', '7891234568013', 'HIERRO-004', 'Siderar', 'HIERRO-12MM-6M', 4200.00, 2520.00, 3570.00, 6, 2, 5.33, '600x1.2x1.2'),
('Hierro 16mm x 6m', 'Hierro redondo 16mm x 6 metros', '7891234568014', 'HIERRO-005', 'Siderar', 'HIERRO-16MM-6M', 7500.00, 4500.00, 6375.00, 6, 2, 9.48, '600x1.6x1.6'),
('Hierro 20mm x 6m', 'Hierro redondo 20mm x 6 metros', '7891234568015', 'HIERRO-006', 'Siderar', 'HIERRO-20MM-6M', 12000.00, 7200.00, 10200.00, 6, 2, 14.80, '600x2.0x2.0'),
('Hierro 25mm x 6m', 'Hierro redondo 25mm x 6 metros', '7891234568016', 'HIERRO-007', 'Siderar', 'HIERRO-25MM-6M', 18000.00, 10800.00, 15300.00, 6, 2, 23.13, '600x2.5x2.5'),
('Alambre 2.2mm x 1kg', 'Alambre de construcción 2.2mm', '7891234568017', 'ALAMBRE-001', 'Siderar', 'ALAMBRE-2.2MM-1KG', 800.00, 480.00, 680.00, 6, 5, 1.00, '10x5x5'),
('Alambre 2.5mm x 1kg', 'Alambre de construcción 2.5mm', '7891234568018', 'ALAMBRE-002', 'Siderar', 'ALAMBRE-2.5MM-1KG', 1000.00, 600.00, 850.00, 6, 5, 1.00, '10x5x5'),
('Alambre 3mm x 1kg', 'Alambre de construcción 3mm', '7891234568019', 'ALAMBRE-003', 'Siderar', 'ALAMBRE-3MM-1KG', 1200.00, 720.00, 1020.00, 6, 5, 1.00, '10x5x5');

-- =====================================================
-- 16. INSERTAR MÁS PRODUCTOS (JARDÍN Y EXTERIOR)
-- =====================================================

INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Manguera 1/2" x 25m', 'Manguera de riego 1/2 pulgada', '7891234568020', 'MANGUERA-001', 'Tigre', 'MANGUERA-1/2-25M', 3500.00, 2100.00, 2975.00, 7, 2, 2.50, '2500x1.5x1.5'),
('Manguera 3/4" x 25m', 'Manguera de riego 3/4 pulgada', '7891234568021', 'MANGUERA-002', 'Tigre', 'MANGUERA-3/4-25M', 4500.00, 2700.00, 3825.00, 7, 2, 3.00, '2500x2.0x2.0'),
('Manguera 1" x 25m', 'Manguera de riego 1 pulgada', '7891234568022', 'MANGUERA-003', 'Tigre', 'MANGUERA-1-25M', 5500.00, 3300.00, 4675.00, 7, 2, 3.50, '2500x2.5x2.5'),
('Aspersor Giratorio', 'Aspersor para riego automático', '7891234568023', 'ASPERSOR-001', 'Tigre', 'ASPERSOR-GIRATORIO', 1200.00, 720.00, 1020.00, 7, 1, 0.30, '15x8x8'),
('Aspersor Estático', 'Aspersor estático para riego', '7891234568024', 'ASPERSOR-002', 'Tigre', 'ASPERSOR-ESTATICO', 800.00, 480.00, 680.00, 7, 1, 0.20, '10x6x6'),
('Conexión T 1/2"', 'Conexión T para manguera 1/2"', '7891234568025', 'CONEX-JARDIN-001', 'Tigre', 'CONEX-T-1/2', 150.00, 90.00, 127.50, 7, 1, 0.05, '5x3x3'),
('Conexión T 3/4"', 'Conexión T para manguera 3/4"', '7891234568026', 'CONEX-JARDIN-002', 'Tigre', 'CONEX-T-3/4', 200.00, 120.00, 170.00, 7, 1, 0.08, '6x4x4'),
('Conexión T 1"', 'Conexión T para manguera 1"', '7891234568027', 'CONEX-JARDIN-003', 'Tigre', 'CONEX-T-1', 250.00, 150.00, 212.50, 7, 1, 0.12, '7x5x5'),
('Pico de Riego', 'Pico para manguera de riego', '7891234568028', 'PICO-001', 'Tigre', 'PICO-RIEGO', 300.00, 180.00, 255.00, 7, 1, 0.15, '8x6x6'),
('Carretel Manguera', 'Carretel para manguera de riego', '7891234568029', 'CARRETEL-001', 'Tigre', 'CARRETEL-MANGUERA', 8500.00, 5100.00, 7225.00, 7, 1, 5.00, '50x30x30');

-- =====================================================
-- 17. INSERTAR MÁS PRODUCTOS (SEGURIDAD)
-- =====================================================

INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Casco de Seguridad', 'Casco de seguridad industrial', '7891234568030', 'SEG-001', '3M', 'CASCO-SEGURIDAD', 2500.00, 1500.00, 2125.00, 8, 1, 0.40, '25x20x15'),
('Gafas de Seguridad', 'Gafas de seguridad transparentes', '7891234568031', 'SEG-002', '3M', 'GAFAS-SEGURIDAD', 1200.00, 720.00, 1020.00, 8, 1, 0.10, '15x8x5'),
('Protección Auditiva', 'Protectores auditivos desechables', '7891234568032', 'SEG-003', '3M', 'PROT-AUDITIVOS', 800.00, 480.00, 680.00, 8, 1, 0.05, '10x5x3'),
('Guantes de Trabajo', 'Guantes de trabajo resistentes', '7891234568033', 'SEG-004', '3M', 'GUANTES-TRABAJO', 1500.00, 900.00, 1275.00, 8, 12, 0.20, '20x10x5'),
('Botas de Seguridad', 'Botas de seguridad con puntera', '7891234568034', 'SEG-005', '3M', 'BOTAS-SEGURIDAD', 8500.00, 5100.00, 7225.00, 8, 12, 1.50, '30x15x15'),
('Chaleco Reflectivo', 'Chaleco de seguridad reflectivo', '7891234568035', 'SEG-006', '3M', 'CHALECO-REFLECTIVO', 1800.00, 1080.00, 1530.00, 8, 1, 0.30, '40x30x5'),
('Mascarilla N95', 'Mascarilla de protección N95', '7891234568036', 'SEG-007', '3M', 'MASCARILLA-N95', 500.00, 300.00, 425.00, 8, 1, 0.02, '8x5x2'),
('Respirador', 'Respirador con filtros', '7891234568037', 'SEG-008', '3M', 'RESPIRADOR', 3500.00, 2100.00, 2975.00, 8, 1, 0.50, '15x10x8'),
('Cinturón de Seguridad', 'Cinturón de seguridad para trabajo en altura', '7891234568038', 'SEG-009', '3M', 'CINTURON-SEGURIDAD', 12000.00, 7200.00, 10200.00, 8, 1, 2.00, '50x20x10'),
('Extintor 1kg', 'Extintor portátil 1kg', '7891234568039', 'SEG-010', 'Local', 'EXTINTOR-1KG', 8500.00, 5100.00, 7225.00, 8, 1, 2.50, '25x15x15');

-- =====================================================
-- 18. INSERTAR MÁS PRODUCTOS (FIJACIONES)
-- =====================================================

INSERT INTO Productos (Nombre, Descripcion, Codigo_Barras, SKU, Marca, Modelo, Precio, Costo, Precio_Mayorista, ID_Categoria, ID_Unidad_de_medida, Peso, Dimensiones) VALUES 
('Tornillo Phillips 3x20mm 100u', 'Tornillos Phillips cabeza plana', '7891234568040', 'TORN-001', 'Tornillos Argentinos', 'TORN-PHILLIPS-3x20-100', 1200.00, 720.00, 1020.00, 9, 1, 0.50, '10x8x5'),
('Tornillo Phillips 4x25mm 100u', 'Tornillos Phillips cabeza plana', '7891234568041', 'TORN-002', 'Tornillos Argentinos', 'TORN-PHILLIPS-4x25-100', 1500.00, 900.00, 1275.00, 9, 1, 0.80, '12x10x6'),
('Tornillo Phillips 5x30mm 100u', 'Tornillos Phillips cabeza plana', '7891234568042', 'TORN-003', 'Tornillos Argentinos', 'TORN-PHILLIPS-5x30-100', 1800.00, 1080.00, 1530.00, 9, 1, 1.20, '15x12x7'),
('Tornillo Phillips 6x40mm 100u', 'Tornillos Phillips cabeza plana', '7891234568043', 'TORN-004', 'Tornillos Argentinos', 'TORN-PHILLIPS-6x40-100', 2200.00, 1320.00, 1870.00, 9, 1, 1.80, '18x15x8'),
('Tornillo Phillips 8x50mm 100u', 'Tornillos Phillips cabeza plana', '7891234568044', 'TORN-005', 'Tornillos Argentinos', 'TORN-PHILLIPS-8x50-100', 2800.00, 1680.00, 2380.00, 9, 1, 2.50, '20x18x10'),
('Clavo 1" 1kg', 'Clavos de construcción 1 pulgada', '7891234568045', 'CLAVO-001', 'Tornillos Argentinos', 'CLAVO-1-1KG', 800.00, 480.00, 680.00, 9, 5, 1.00, '15x8x8'),
('Clavo 2" 1kg', 'Clavos de construcción 2 pulgadas', '7891234568046', 'CLAVO-002', 'Tornillos Argentinos', 'CLAVO-2-1KG', 1000.00, 600.00, 850.00, 9, 5, 1.00, '15x8x8'),
('Clavo 3" 1kg', 'Clavos de construcción 3 pulgadas', '7891234568047', 'CLAVO-003', 'Tornillos Argentinos', 'CLAVO-3-1KG', 1200.00, 720.00, 1020.00, 9, 5, 1.00, '15x8x8'),
('Clavo 4" 1kg', 'Clavos de construcción 4 pulgadas', '7891234568048', 'CLAVO-004', 'Tornillos Argentinos', 'CLAVO-4-1KG', 1500.00, 900.00, 1275.00, 9, 5, 1.00, '15x8x8'),
('Clavo 6" 1kg', 'Clavos de construcción 6 pulgadas', '7891234568049', 'CLAVO-005', 'Tornillos Argentinos', 'CLAVO-6-1KG', 2000.00, 1200.00, 1700.00, 9, 5, 1.00, '15x8x8');

-- =====================================================
-- 19. INSERTAR MÁS INVENTARIO
-- =====================================================

-- Inventario para productos de construcción
INSERT INTO Inventario (ID_Producto, ID_Sucursal, Stock_Actual, Stock_Minimo, Stock_Maximo, Ubicacion) VALUES 
(100, 1, 200, 50, 400, 'Depósito - Estante A1'),
(101, 1, 150, 30, 300, 'Depósito - Estante A1'),
(102, 1, 100, 20, 200, 'Depósito - Estante A1'),
(103, 1, 50, 10, 100, 'Depósito - Estante A2'),
(104, 1, 40, 8, 80, 'Depósito - Estante A2'),
(105, 1, 30, 5, 60, 'Depósito - Estante A3'),
(106, 1, 25, 5, 50, 'Depósito - Estante A3'),
(107, 1, 20, 3, 40, 'Depósito - Estante A3'),
(108, 1, 15, 3, 30, 'Depósito - Estante A3'),
(109, 1, 10, 2, 20, 'Depósito - Estante A3'),
(110, 1, 80, 15, 150, 'Depósito - Estante B1'),
(111, 1, 60, 12, 120, 'Depósito - Estante B1'),
(112, 1, 50, 10, 100, 'Depósito - Estante B1'),
(113, 1, 40, 8, 80, 'Depósito - Estante B1'),
(114, 1, 30, 6, 60, 'Depósito - Estante B1'),
(115, 1, 25, 5, 50, 'Depósito - Estante B1'),
(116, 1, 20, 4, 40, 'Depósito - Estante B1'),
(117, 1, 100, 20, 200, 'Depósito - Estante B2'),
(118, 1, 80, 15, 150, 'Depósito - Estante B2'),
(119, 1, 60, 12, 120, 'Depósito - Estante B2');

-- Inventario para productos de jardín
INSERT INTO Inventario (ID_Producto, ID_Sucursal, Stock_Actual, Stock_Minimo, Stock_Maximo, Ubicacion) VALUES 
(120, 1, 40, 8, 80, 'Jardín - Estante C1'),
(121, 1, 35, 7, 70, 'Jardín - Estante C1'),
(122, 1, 30, 6, 60, 'Jardín - Estante C1'),
(123, 1, 50, 10, 100, 'Jardín - Estante C1'),
(124, 1, 60, 12, 120, 'Jardín - Estante C1'),
(125, 1, 80, 15, 150, 'Jardín - Estante C2'),
(126, 1, 70, 14, 140, 'Jardín - Estante C2'),
(127, 1, 60, 12, 120, 'Jardín - Estante C2'),
(128, 1, 40, 8, 80, 'Jardín - Estante C2'),
(129, 1, 20, 4, 40, 'Jardín - Estante C2');

-- Inventario para productos de seguridad
INSERT INTO Inventario (ID_Producto, ID_Sucursal, Stock_Actual, Stock_Minimo, Stock_Maximo, Ubicacion) VALUES 
(130, 1, 30, 5, 60, 'Seguridad - Estante D1'),
(131, 1, 50, 10, 100, 'Seguridad - Estante D1'),
(132, 1, 100, 20, 200, 'Seguridad - Estante D1'),
(133, 1, 40, 8, 80, 'Seguridad - Estante D1'),
(134, 1, 25, 5, 50, 'Seguridad - Estante D1'),
(135, 1, 35, 7, 70, 'Seguridad - Estante D1'),
(136, 1, 200, 40, 400, 'Seguridad - Estante D1'),
(137, 1, 15, 3, 30, 'Seguridad - Estante D1'),
(138, 1, 10, 2, 20, 'Seguridad - Estante D1'),
(139, 1, 20, 4, 40, 'Seguridad - Estante D1');

-- =====================================================
-- 20. INSERTAR MÁS FACTURAS DE VENTA
-- =====================================================

-- Factura 6 - Construcción
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('A-0001-00000006', 11, 1, '2024-01-18 08:30:00', 'A', 'IVA Responsable Inscripto', 250000.00, 52500.00, 15000.00, 287500.00, 2, 'Pagada', 'Transferencia');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(6, 100, 50, 4500.00, 0.00, 225000.00),
(6, 110, 20, 1200.00, 0.00, 24000.00),
(6, 117, 10, 800.00, 0.00, 8000.00);

-- Factura 7 - Jardín
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('B-0001-00000007', 4, 2, '2024-01-19 15:20:00', 'B', 'IVA Responsable Inscripto', 18000.00, 0.00, 2000.00, 16000.00, 5, 'Pagada', 'Efectivo');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(7, 120, 2, 3500.00, 0.00, 7000.00),
(7, 123, 5, 1200.00, 0.00, 6000.00),
(7, 125, 10, 150.00, 0.00, 1500.00),
(7, 128, 1, 300.00, 0.00, 300.00),
(7, 129, 1, 8500.00, 0.00, 8500.00);

-- Factura 8 - Seguridad
INSERT INTO Facturas_Venta (Numero_Factura, ID_Cliente, ID_Sucursal, Fecha, Tipo_Factura, Condicion_IVA, Subtotal, IVA, Descuento, Total, ID_Usuario, Estado, Forma_Pago) VALUES 
('A-0001-00000008', 13, 3, '2024-01-20 10:45:00', 'A', 'IVA Responsable Inscripto', 45000.00, 9450.00, 3000.00, 51450.00, 8, 'Pagada', 'Cheque');

INSERT INTO Detalles_Factura_Venta (ID_Factura_Venta, ID_Producto, Cantidad, Precio_Unitario, Descuento_Unitario, Subtotal) VALUES 
(8, 130, 10, 2500.00, 0.00, 25000.00),
(8, 131, 20, 1200.00, 0.00, 24000.00),
(8, 132, 50, 800.00, 0.00, 40000.00),
(8, 136, 100, 500.00, 0.00, 50000.00);

-- =====================================================
-- 21. INSERTAR MÁS PAGOS
-- =====================================================

INSERT INTO Pagos (ID_Factura_Venta, Metodo, Monto, Numero_Comprobante, ID_Usuario) VALUES 
(6, 'Transferencia', 287500.00, 'TR-002', 2),
(7, 'Efectivo', 16000.00, 'EF-003', 5),
(8, 'Cheque', 51450.00, 'CH-002', 8);

-- =====================================================
-- 22. INSERTAR MÁS MOVIMIENTOS DE INVENTARIO
-- =====================================================

-- Movimientos por ventas adicionales
INSERT INTO Movimientos_Inventario (ID_Producto, ID_Sucursal, Fecha, Tipo, Cantidad, Costo_Unitario, ID_Usuario, ID_Referencia, Tipo_Referencia) VALUES 
(100, 1, '2024-01-18 08:30:00', 'Venta', -50, 2700.00, 2, 6, 'Factura'),
(110, 1, '2024-01-18 08:30:00', 'Venta', -20, 720.00, 2, 6, 'Factura'),
(117, 1, '2024-01-18 08:30:00', 'Venta', -10, 480.00, 2, 6, 'Factura'),
(120, 2, '2024-01-19 15:20:00', 'Venta', -2, 2100.00, 5, 7, 'Factura'),
(123, 2, '2024-01-19 15:20:00', 'Venta', -5, 720.00, 5, 7, 'Factura'),
(125, 2, '2024-01-19 15:20:00', 'Venta', -10, 90.00, 5, 7, 'Factura'),
(128, 2, '2024-01-19 15:20:00', 'Venta', -1, 180.00, 5, 7, 'Factura'),
(129, 2, '2024-01-19 15:20:00', 'Venta', -1, 5100.00, 5, 7, 'Factura'),
(130, 3, '2024-01-20 10:45:00', 'Venta', -10, 1500.00, 8, 8, 'Factura'),
(131, 3, '2024-01-20 10:45:00', 'Venta', -20, 720.00, 8, 8, 'Factura'),
(132, 3, '2024-01-20 10:45:00', 'Venta', -50, 480.00, 8, 8, 'Factura'),
(136, 3, '2024-01-20 10:45:00', 'Venta', -100, 300.00, 8, 8, 'Factura');

-- =====================================================
-- 23. CREAR VISTAS ADICIONALES PARA REPORTES
-- =====================================================

-- Vista para productos con stock crítico
CREATE VIEW vw_Stock_Critico AS
SELECT 
    p.Nombre AS Producto,
    p.Codigo_Barras,
    p.SKU,
    c.Nombre AS Categoria,
    s.Nombre AS Sucursal,
    i.Stock_Actual,
    i.Stock_Minimo,
    (i.Stock_Actual - i.Stock_Minimo) AS Stock_Disponible,
    CASE 
        WHEN i.Stock_Actual = 0 THEN 'SIN STOCK'
        WHEN i.Stock_Actual <= i.Stock_Minimo THEN 'CRÍTICO'
        WHEN i.Stock_Actual <= (i.Stock_Minimo * 1.5) THEN 'BAJO'
        ELSE 'NORMAL'
    END AS Estado_Stock
FROM Inventario i
INNER JOIN Productos p ON i.ID_Producto = p.ID_Producto
INNER JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
INNER JOIN Sucursales s ON i.ID_Sucursal = s.ID_Sucursal
WHERE p.Activo = 1 AND i.Activo = 1;
GO

PRINT '✓ Vista vw_Stock_Critico creada';

-- Vista para ventas por categoría 
CREATE VIEW vw_Ventas_Por_Categoria AS
SELECT 
    c.Nombre AS Categoria,
    COUNT(DISTINCT fv.ID_Factura_Venta) AS Cantidad_Facturas,
    SUM(dfv.Cantidad) AS Total_Productos_Vendidos,
    SUM(dfv.Subtotal) AS Total_Ventas,
    AVG(dfv.Precio_Unitario) AS Precio_Promedio
FROM Categorias c
INNER JOIN Productos p ON c.ID_Categoria = p.ID_Categoria
INNER JOIN Detalles_Factura_Venta dfv ON p.ID_Producto = dfv.ID_Producto
INNER JOIN Facturas_Venta fv ON dfv.ID_Factura_Venta = fv.ID_Factura_Venta
WHERE fv.Estado != 'Anulada'
GROUP BY c.ID_Categoria, c.Nombre;
GO

PRINT '✓ Vista vw_Ventas_Por_Categoria creada';

-- Vista para clientes más frecuentes (
CREATE VIEW vw_Clientes_Mas_Frecuentes AS
SELECT 
    c.Nombre + ' ' + ISNULL(c.Apellido, '') AS Cliente,
    c.Tipo_Cliente,
    COUNT(fv.ID_Factura_Venta) AS Cantidad_Facturas,
    SUM(fv.Total) AS Total_Compras,
    AVG(fv.Total) AS Promedio_Factura,
    MAX(fv.Fecha) AS Ultima_Compra
FROM Clientes c
INNER JOIN Facturas_Venta fv ON c.ID_Cliente = fv.ID_Cliente
WHERE fv.Estado != 'Anulada'
GROUP BY c.ID_Cliente, c.Nombre, c.Apellido, c.Tipo_Cliente;
GO

PRINT '✓ Vista vw_Clientes_Mas_Frecuentes creada';

-- Vista para proveedores más utilizados 
CREATE VIEW vw_Proveedores_Mas_Utilizados AS
SELECT 
    p.Nombre AS Proveedor,
    COUNT(oc.ID_OC) AS Cantidad_Ordenes,
    SUM(oc.Total) AS Total_Compras,
    AVG(oc.Total) AS Promedio_Orden,
    MAX(oc.Fecha) AS Ultima_Orden
FROM Proveedores p
INNER JOIN Ordenes_Compra oc ON p.ID_Proveedor = oc.ID_Proveedor
GROUP BY p.ID_Proveedor, p.Nombre;
GO

PRINT '✓ Vista vw_Proveedores_Mas_Utilizados creada';

-- Vista para rentabilidad por producto 
CREATE VIEW vw_Rentabilidad_Producto AS
SELECT 
    p.Nombre AS Producto,
    p.Codigo_Barras,
    c.Nombre AS Categoria,
    p.Precio,
    p.Costo,
    (p.Precio - p.Costo) AS Margen_Bruto,
    CASE 
        WHEN p.Precio > 0 THEN ((p.Precio - p.Costo) / p.Precio) * 100 
        ELSE 0 
    END AS Margen_Porcentaje,
    SUM(ISNULL(dfv.Cantidad, 0)) AS Total_Vendido,
    SUM(ISNULL(dfv.Subtotal, 0)) AS Total_Ventas
FROM Productos p
INNER JOIN Categorias c ON p.ID_Categoria = c.ID_Categoria
LEFT JOIN Detalles_Factura_Venta dfv ON p.ID_Producto = dfv.ID_Producto
LEFT JOIN Facturas_Venta fv ON dfv.ID_Factura_Venta = fv.ID_Factura_Venta AND fv.Estado != 'Anulada'
WHERE p.Activo = 1
GROUP BY p.ID_Producto, p.Nombre, p.Codigo_Barras, c.Nombre, p.Precio, p.Costo;
GO

PRINT '✓ Vista vw_Rentabilidad_Producto creada';

-- Verificar que las vistas se crearon correctamente
SELECT name, type_desc, create_date
FROM sys.objects 
WHERE type = 'V' AND name LIKE 'vw_%'
ORDER BY name;
GO
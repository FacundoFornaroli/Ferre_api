-- Script para crear/actualizar usuario administrador
-- Ejecutar este script directamente en SQL Server Management Studio

USE Ferreteriadb;

-- Verificar si el usuario administrador ya existe
IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE Email = 'juan.gonzalez@ferreteria.com')
BEGIN
    -- Crear nuevo usuario administrador
    INSERT INTO Usuarios (
        Nombre, 
        Apellido, 
        Rol, 
        Email, 
        Contraseña, 
        Estado, 
        Creado_el, 
        Actualizado_el
    ) VALUES (
        'Juan',
        'González',
        'admin',
        'juan.gonzalez@ferreteria.com',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqQKqK', -- admin123 hasheado
        1,
        GETDATE(),
        GETDATE()
    );
    
    PRINT 'Usuario administrador creado exitosamente';
END
ELSE
BEGIN
    -- Actualizar usuario administrador existente
    UPDATE Usuarios 
    SET 
        Contraseña = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqQKqK', -- admin123 hasheado
        Rol = 'admin',
        Actualizado_el = GETDATE()
    WHERE Email = 'juan.gonzalez@ferreteria.com';
    
    PRINT 'Usuario administrador actualizado exitosamente';
END

PRINT 'Credenciales de administrador:';
PRINT 'Email: juan.gonzalez@ferreteria.com';
PRINT 'Contraseña: admin123'; 
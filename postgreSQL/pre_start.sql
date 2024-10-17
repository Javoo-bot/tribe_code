-- Crear tabla Template
CREATE TABLE IF NOT EXISTS template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Client
CREATE TABLE IF NOT EXISTS client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    company_name TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Insertar datos en la tabla Template
INSERT INTO template (name, content, description)
VALUES ('Plantilla de Bienvenida', 'Bienvenido a nuestra plataforma', 'Plantilla estándar de bienvenida');

-- Insertar datos en la tabla Client
INSERT INTO client (name, email, phone, address, company_name, is_active, notes)
VALUES ('Juan Pérez', 'juan.perez@example.com', '+1234567890', 'Calle Falsa 123', 'Empresa S.A.', 1, 'Cliente regular');

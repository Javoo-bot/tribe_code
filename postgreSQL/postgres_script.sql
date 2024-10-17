BEGIN;

CREATE TABLE template (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO template (id, name, content, description, created_at, updated_at)
VALUES (1, 'Plantilla de Bienvenida', 'Bienvenido a nuestra plataforma', 'Plantilla estándar de bienvenida', '2024-10-17 09:50:45', '2024-10-17 09:50:45');

CREATE TABLE client (
    id SERIAL PRIMARY KEY,
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

INSERT INTO client (id, name, email, phone, address, company_name, registration_date, is_active, notes, created_at, updated_at)
VALUES (1, 'Juan Pérez', 'juan.perez@example.com', '+1234567890', 'Calle Falsa 123', 'Empresa S.A.', '2024-10-17 09:50:49', TRUE, 'Cliente regular', '2024-10-17 09:50:49', '2024-10-17 09:50:49');

COMMIT;

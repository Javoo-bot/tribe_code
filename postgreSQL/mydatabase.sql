PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO template VALUES(1,'Plantilla de Bienvenida','Bienvenido a nuestra plataforma','Plantilla estándar de bienvenida','2024-10-17 09:50:45','2024-10-17 09:50:45');
CREATE TABLE client (
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
INSERT INTO client VALUES(1,'Juan Pérez','juan.perez@example.com','+1234567890','Calle Falsa 123','Empresa S.A.','2024-10-17 09:50:49',1,'Cliente regular','2024-10-17 09:50:49','2024-10-17 09:50:49');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('template',1);
INSERT INTO sqlite_sequence VALUES('client',1);
COMMIT;

CREATE DATABASE taskly;

USE taskly;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active'
);

INSERT INTO tasks (task, status)
VALUES
('Complete Python assignment', 'active'),
('Study Java', 'completed');
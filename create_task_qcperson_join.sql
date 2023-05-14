CREATE DATABASE qc_database;

USE qc_database;

CREATE TABLE qc_persons (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    is_busy BOOLEAN DEFAULT FALSE,
    current_task INT DEFAULT NULL
);
      
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    status ENUM('pending', 'in progress', 'completed') DEFAULT 'pending' NOT NULL,
    assigned_to INT DEFAULT NULL,
    FOREIGN KEY (assigned_to) REFERENCES qc_persons(id)
);

SELECT qc_persons.id, qc_persons.name, qc_persons.is_busy, tasks.id as task_id, tasks.task_name
FROM qc_persons
LEFT JOIN tasks ON qc_persons.current_task = tasks.id

INSERT INTO tasks (id, task_name, status, assigned_to) VALUES 
(1, 'Review article A', 'pending', NULL),
(2, 'Proofread report B', 'pending', NULL),
(3, 'Copyedit manuscript C', 'pending', NULL),
(4, 'Fact-check document D', 'pending', NULL),
(5, 'Verify data E', 'pending', NULL);

-- Data for the qc_person table
INSERT INTO qc_persons (id, name, is_busy, current_task) VALUES 
(1, 'John Doe', FALSE, NULL),
(2, 'Jane Smith', FALSE, NULL),
(3, 'Bob Johnson', FALSE, NULL),
(4, 'Samantha Lee', FLASE, NULL),
(5, 'David Kim', FALSE, NULL);

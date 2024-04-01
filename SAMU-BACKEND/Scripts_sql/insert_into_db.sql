INSERT INTO users (name, username, email, password, is_staff, is_superuser, is_active)
VALUES
  ('Maria Santos', 'maria_santos', 'maria@email.com', 'senha456', TRUE, TRUE, TRUE),
  ('João Silva', 'joao_silva', 'joao@email.com', 'senha123', FALSE, FALSE, TRUE),
  ('Carlos Oliveira', 'carlos_oliveira', 'carlos@email.com', 'senha789', FALSE, TRUE, TRUE),
  ('Ana Ferreira', 'ana_ferreira', 'ana@email.com', 'senha987', TRUE, FALSE, TRUE),
  ('Paulo Sousa', 'paulo_sousa', 'paulo@email.com', 'senha654', FALSE, FALSE, TRUE),
  ('Pedro Rocha', 'pedro_rocha', 'pedro@email.com', 'senha567', TRUE, FALSE, TRUE),
  ('Rafael Lima', 'rafael_lima', 'rafael@email.com', 'senha1234', TRUE, FALSE, TRUE),
  ('Isabela Santos', 'isabela_santos', 'isabela@email.com', 'senha5678', FALSE, FALSE, TRUE);

INSERT INTO groups (name)
VALUES
	('supervisor'),
	('doctor');
	
INSERT INTO tokens (hashed_token, created, user_id)
VALUES
  (E'\\x0123456789AAAAEF', '2023-09-17 14:00:00', 1),
  (E'\\xabcdef0123456789', '2023-09-17 15:30:00', 2),
  (E'\\xfedcba9876543210', '2023-09-18 11:45:00', 3),
  (E'\\x0123456789ABADEF', '2023-09-19 08:30:00', 4),
  (E'\\x0123456789ABFDEF', '2023-09-19 10:00:00', 5),
  (E'\\xabcdef01234567F9', '2023-09-19 11:30:00', 6),
  (E'\\x9876543210ADCDEF', '2023-09-19 12:45:00', 7);

INSERT INTO user_groups (user_id, group_id)
VALUES
	(1, 1),
	(2, 1),
	(3, 2),
	(4, 2),
	(5, 2),
	(6, 2);

INSERT INTO request_status (name) 
VALUES
	('in_progress'),
	('success'),
	('failed');

INSERT INTO request_types (name) 
VALUES
	('create_user'),
	('delete_user'),
	('get_user'),
	('update_user'),
	('list_user'),
	('login_user'),
	('logout_user'),
	('create_material'),
	('delete_material'),
	('get_material'),
	('update_material'),
	('list_material'),
	('create_medicine'),
	('delete_medicine'),
	('get_medicine'),
	('update_medicine'),
	('list_medicine'),
	('create_equipment'),
	('delete_equipment'),
	('get_equipment'),
	('update_equipment'),
	('list_equipment'),
	('create_vehicle'),
	('delete_vehicle');
   
   
INSERT INTO requests (created_at, status_id, type_id, user_id)
VALUES
    ('2023-09-17 10:00:00', 1, 8, 1),
    ('2023-09-18 11:30:00', 2, 13, 2),
    ('2023-09-19 14:45:00', 3, 18, 3),
    ('2023-09-20 16:20:00', 1, 8, 4),
    ('2023-09-21 09:15:00', 2, 13, 5),
    ('2023-09-22 12:30:00', 3, 18, 6),
    ('2023-09-23 08:10:00', 1, 8, 7),
    ('2023-09-24 13:40:00', 2, 13, 8),
    ('2023-09-25 15:25:00', 3, 18, 8),
    ('2023-09-26 17:55:00', 1, 8, 8),
    ('2023-09-27 10:00:00', 1, 8, 1),
    ('2023-09-28 11:30:00', 2, 13, 2),
    ('2023-09-29 14:45:00', 3, 18, 3),
    ('2023-09-30 16:20:00', 1, 8, 4),
    ('2023-10-01 09:15:00', 2, 13, 5),
	('2023-09-17 10:00:00', 1, 1, 1),
    ('2023-09-18 11:30:00', 2, 1, 1),
    ('2023-09-19 14:45:00', 3, 1, 1),
    ('2023-09-20 16:20:00', 1, 1, 1),
    ('2023-09-21 09:15:00', 2, 1, 1),
    ('2023-09-22 12:30:00', 3, 1, 1),
    ('2023-09-23 08:10:00', 1, 1, 1),
    ('2023-09-24 13:40:00', 2, 1, 1);

INSERT INTO vehicles (available) 
VALUES
	(TRUE),
   	(TRUE),
   	(TRUE),
   	(TRUE),
   	(TRUE);	

INSERT INTO items (type) 
VALUES
   (1),
   (2),
   (3),
   (4),
   (5),
   (6), 
   (7),
   (8),
   (9),
   (10),
   (11),
   (12),
   (13),
   (14),
   (15);
   
INSERT INTO materials (id, name, description, batch_code, allocable, expiration_date)
VALUES
    (1, 'Luvas Cirúrgicas Estéreis', 'Luvas cirúrgicas estéreis descartáveis, tamanho médio', '1234', TRUE, '2023-12-31'),
    (2, 'Álcool Isopropílico 70%', 'Solução alcoólica a 70%, frasco de 500ml', '5678', FALSE, '2023-11-15'),
    (3, 'Máscaras N95', 'Máscaras de proteção respiratória N95, pacote com 10 unidades', '9012', TRUE, '2024-02-28'),
    (4, 'Seringas Descartáveis', 'Seringas descartáveis de 10ml, pacote com 100 unidades', '3456', TRUE, '2023-10-20'),
    (5, 'Gaze Estéril', 'Gaze estéril 10x10cm, pacote com 100 unidades', '7890', FALSE, '2023-09-01');
   		
INSERT INTO medicines (id, name, measurement_unit, presentation, batch_code, concentration, therapeutic_class)
VALUES
    (6, 'Paracetamol', 1, 2, '7891', '10mg/ml', 'Analgésico'),
    (7, 'Amoxicilina', 2, 1, '2356', '5mg/ml', 'Antibiótico'),
    (8, 'Ibuprofeno', 1, 3, '4768', '20mg/ml', 'Anti-inflamatório'),
    (9, 'Omeprazol', 3, 1, '1234', '15mg/ml', 'Inibidor de Ácido Gástrico'),
    (10, 'Atorvastatina', 2, 2, '5643', '8mg/ml', 'Estatina');
   
INSERT INTO equipments (id, name, description, patrimony, allocable, available, warranty_expire) VALUES
    (11, 'Monitor Cardíaco', 'Monitor cardíaco para medição de sinais vitais', 'Patri001', TRUE, TRUE, '2024-06-30'),
    (12, 'Desfibrilador', 'Desfibrilador para ressuscitação cardiopulmonar', 'Patri002', TRUE, FALSE, '2023-11-15'),
    (13, 'Bomba de Infusão', 'Bomba de infusão para administração de medicamentos', 'Patri003', FALSE, TRUE, NULL),
    (14, 'Ventilador Pulmonar', 'Ventilador pulmonar para suporte à respiração', 'Patri004', TRUE, TRUE, '2025-02-18'),
    (15, 'Ressonância Magnética', 'Equipamento de ressonância magnética', 'Patri005', TRUE, TRUE, '2024-09-10');
   
INSERT INTO entries (item_id, date, quantity, available_quantity, vehicle_id, reason) VALUES
    (1, '2023-09-17', 100, 100, 1, 1),
    (2, '2023-09-18', 50, 50, 2, 2),
    (3, '2023-09-19', 75, 75, 3, 1),
    (4, '2023-09-20', 60, 60, 4, 3),
    (5, '2023-09-21', 90, 90, 5, 2),
    (6, '2023-09-22', 110, 110, 1, 1),
    (7, '2023-09-23', 30, 30, 2, 2),
    (8, '2023-09-24', 45, 45, 3, 1),
    (9, '2023-09-25', 70, 70, 4, 3),
    (10, '2023-09-26', 80, 80, 5, 2),
   	(11, '2023-09-27', 1, 1, 1, 1),
    (12, '2023-09-28', 1, 1, 2, 2),
    (13, '2023-09-29', 1, 1, 3, 1),
    (14, '2023-09-30', 1, 1, 4, 3),
    (15, '2023-10-01', 1, 1, 5, 2);
   
INSERT INTO outputs (entry_id, quantity, date, reason)
VALUES
    (7, 20, '2023-09-22', 4),
    (3, 30, '2023-09-23', 3),
    (5, 40, '2023-09-24', 4),
    (9, 15, '2023-09-25', 2),
    (2, 25, '2023-09-26', 1);
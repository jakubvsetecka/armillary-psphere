USE myapp;

-- Insert dummy data into OSOBA table
INSERT INTO OSOBA (JMENO_OSOBA, PRIJMENI_OSOBA) VALUES
('Jan', 'Novák'),
('Marie', 'Svobodová'),
('Petr', 'Dvořák'),
('Eva', 'Černá'),
('Jiří', 'Procházka');

-- Insert dummy data into POSLANEC table
INSERT INTO POSLANEC (ID_OSOBA) VALUES
(1),
(2),
(3),
(4),
(5);

-- Insert dummy data into HLASOVANI table
INSERT INTO HLASOVANI (VYSLEDEK_HLASOVANI, NAZEV_HLASOVANI, DATUM_HLASOVANI, URL_HLASOVANI) VALUES
('Schváleno', 'Hlasování o rozpočtu', '2023-06-01', 'http://example.com/hlasovani/1'),
('Zamítnuto', 'Hlasování o novém zákonu', '2023-06-02', 'http://example.com/hlasovani/2'),
('Schváleno', 'Hlasování o daňové reformě', '2023-06-03', 'http://example.com/hlasovani/3'),
('Zamítnuto', 'Hlasování o reformě školství', '2023-06-04', 'http://example.com/hlasovani/4'),
('Schváleno', 'Hlasování o důchodové reformě', '2023-06-05', 'http://example.com/hlasovani/5');

-- Insert dummy data into POSLANEC_HLASOVANI table
INSERT INTO POSLANEC_HLASOVANI (ID_POSLANEC, ID_HLASOVANI, VYSLEDEK) VALUES
(1, 1, 'Pro'),
(1, 2, 'Proti'),
(2, 1, 'Pro'),
(2, 3, 'Pro'),
(3, 2, 'Proti'),
(3, 4, 'Proti'),
(4, 3, 'Pro'),
(4, 5, 'Pro'),
(5, 4, 'Proti'),
(5, 5, 'Pro');

-- Insert dummy data into TISKY table
INSERT INTO TISKY (NAZEV_TISK) VALUES
('Návrh zákona o rozpočtu'),
('Návrh nového zákona'),
('Návrh daňové reformy'),
('Návrh reformy školství'),
('Návrh důchodové reformy');

-- Insert dummy data into HIST table
INSERT INTO HIST (ID_TISK, ID_HLASOVANI) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

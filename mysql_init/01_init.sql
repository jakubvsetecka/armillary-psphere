USE myapp;

-- Create tables based on your schema
CREATE TABLE typ_organu (
    id_typ_org INT PRIMARY KEY,
    typ_id_typ_org INT,
    nazev_typ_org_cz VARCHAR(255),
    nazev_typ_org_en VARCHAR(255),
    typ_org_obecny INT,
    priorita INT,
    FOREIGN KEY (typ_id_typ_org) REFERENCES typ_organu(id_typ_org),
    FOREIGN KEY (typ_org_obecny) REFERENCES typ_organu(id_typ_org)
);

CREATE TABLE typ_funkce (
    id_typ_funkce INT PRIMARY KEY,
    id_typ_org INT,
    typ_funkce_cz VARCHAR(255),
    typ_funkce_en VARCHAR(255),
    priorita INT,
    typ_funkce_obecny INT,
    FOREIGN KEY (id_typ_org) REFERENCES typ_organu(id_typ_org)
);

-- Add more CREATE TABLE statements for other tables in your schema

-- You can also add INSERT statements to populate tables with initial data
INSERT INTO typ_organu (id_typ_org, nazev_typ_org_cz, nazev_typ_org_en, priorita) 
VALUES (1, 'Poslanecká sněmovna', 'Chamber of Deputies', 1);

-- Add more INSERT statements as needed

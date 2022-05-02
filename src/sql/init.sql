DROP TABLE IF EXISTS animaux;
DROP TABLE IF EXISTS familles;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS animaux_types;
DROP TABLE IF EXISTS velages;
DROP TABLE IF EXISTS animaux_velages;
DROP TABLE IF EXISTS complications;
DROP TABLE IF EXISTS velages_complications;

CREATE TABLE animaux (
	id int PRIMARY KEY NOT NULL,
	famille_id int NOT NULL,
	sexe text NOT NULL,
	presence int NOT NULL,
	apprivoise int NOT NULL,
	mort_ne int NOT NULL,
	decede int NOT NULL,
	FOREIGN KEY(famille_id) REFERENCES familles(id)
);

CREATE TABLE familles (
	id int PRIMARY KEY NOT NULL,
	nom text NOT NULL
);

CREATE TABLE types (
	id int PRIMARY KEY NOT NULL,
	type text NOT NULL
);

CREATE TABLE animaux_types (
	animal_id int NOT NULL,
	type_id int NOT NULL,
	pourcentage real NOT NULL,
	PRIMARY KEY(animal_id, type_id),
	FOREIGN KEY(animal_id) REFERENCES animaux(id),
	FOREIGN KEY(type_id) REFERENCES types(id)
);

CREATE TABLE velages (
	id int PRIMARY KEY NOT NULL,
	mere_id int NOT NULL,
	pere_id int NOT NULL,
	date text NOT NULL,
	FOREIGN KEY(mere_id) REFERENCES animaux(id),
	FOREIGN KEY(pere_id) REFERENCES animaux(id)
);

CREATE TABLE animaux_velages (
	animal_id int NOT NULL,
	velage_id int NOT NULL,
	PRIMARY KEY(animal_id, velage_id),
	FOREIGN KEY(animal_id) REFERENCES animaux(id),
	FOREIGN KEY(velage_id) REFERENCES velages(id)
);

CREATE TABLE complications (
	id int PRIMARY KEY NOT NULL,
	complication text NOT NULL
);

CREATE TABLE velages_complications (
	velage_id int NOT NULL,
	complication_id int NOT NULL,
	PRIMARY KEY(velage_id, complication_id),
	FOREIGN KEY(velage_id) REFERENCES velages(id),
	FOREIGN KEY(complication_id) REFERENCES complications(id)
);

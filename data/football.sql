DROP TABLE IF EXISTS football_table, users, league_table, schedule;

CREATE TABLE football_table (
    id SERIAL PRIMARY KEY,
    team_name character varying(255) NOT NULL,
    player_1 character varying(255) NOT NULL,
    player_2 character varying(255) NOT NULL,
    player_3 character varying(255) NOT NULL,
    team_rating int NOT NULL,
    position character varying(255) DEFAULT 'in'
    );

INSERT INTO football_table VALUES
    (1,'Real Madrid','Jovic','Hazard','Kubo',88),
    (2,'Barcelona','Messi','Suarez','Coutinho',90),
    (3,'Atletico Madrid','Griezmann','Morata','Saul',87),
    (4,'Liverpool','Salah','Firmino','Mané',93),
    (5,'Manchester City','Agüero','Sterling','Sane',91),
    (6,'Tottenham','Kane','Son','Lucas',86),
    (7,'Juventus','Dybala','Ronaldo','Mandzukic',89),
    (8,'Bayern München','Lewandowski','Gnabry','Goretzka',85),
    (9,'Dortmund','Alcacer','Reus','Sancho',84),
    (10,'PSG','Neymar','Cavani','Mbappe',90),
    (11,'Manchester United','Pogba','Lukaku','Rashford',80),
    (12,'Arsenal','Aubameyang','Lacazette','Mkhitaryan',78),
    (13,'Chelsea','Pedro','Loftus-Cheek','Higuain',82),
    (14,'Lyon','Dembele','Depay','Fekir',75),
    (15,'Napoli','Milik','Mertens','Insigne',76),
    (16,'Ajax','Tadic','Huntelaar','Ziyech',82),
    (17,'Fc Porto','Soares','Marega','Brahimi',73),
    (18,'Benfica','Seferovic','Silva','Joao',70),
    (19,'Inter','Icardi','Perisic','Nainggolan',77),
    (20,'PSV','de Jong','Lozano','Bergwijn',72),
    (21,'Young Boys','Hoaru','Fassnacht','Assale',65),
    (22,'Basel','Ajeti','van Wolfswinkel','Zuffi',68),
    (23,'Sevilla','Ben Yedder','Sarabia','Morales',82),
    (24,'Valencia','Parejo','Rodrigo','Mina',83);

SELECT pg_catalog.setval('football_table_id_seq', 24, true);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username varchar(200) NOT NULL,
    password varchar(500) NOT NULL
    );

CREATE TABLE league_table (
    user_id int NOT NULL,
    team_name character varying(255) NOT NULL,
    played int DEFAULT 0,
    won int DEFAULT 0,
    drawn int DEFAULT 0,
    lost int DEFAULT 0,
    gf int DEFAULT 0,
    ga int DEFAULT 0,
    gd int DEFAULT 0,
    points int DEFAULT 0
    );

CREATE TABLE schedule (
    user_id INT NOT NULL,
    home character varying(255) NOT NULL,
    away character varying(255) NOT NULL,
    played character varying(255) NOT NULL DEFAULT 'no',
    home_goals int DEFAULT NULL,
    away_goals int DEFAULT NULL,
    scorers character varying(255) DEFAULT NULL,
    last character varying(255) DEFAULT 'notlast'
    );
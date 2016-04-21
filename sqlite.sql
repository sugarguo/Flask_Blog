CREATE TABLE articles (
	id INTEGER NOT NULL, 
	title VARCHAR(255), 
	body TEXT, 
	timestamp DATETIME, 
	tags TEXT, 
	packet_id INTEGER, 
	show INTEGER, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_articles_title ON articles (title);
CREATE INDEX ix_articles_packet_id ON articles (packet_id);
CREATE INDEX ix_articles_timestamp ON articles (timestamp);
CREATE TABLE packets (
	id INTEGER NOT NULL, 
	packet_name VARCHAR(255), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_packets_packet_name ON packets (packet_name);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(64), 
	password_hash VARCHAR(128), 
	email VARCHAR(128), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE TABLE "sites" (
	id INTEGER NOT NULL, 
	site_name VARCHAR(255), 
	site_domain VARCHAR(255), 
	site_email VARCHAR(255), 
	site_time DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (site_name), 
	UNIQUE (site_domain), 
	UNIQUE (site_email)
);

DROP DATABASE IF EXISTS codem;
DROP USER IF EXISTS 'codem'@'localhost';
CREATE DATABASE codem;
CREATE USER 'codem'@'localhost' IDENTIFIED BY 'YELLOWSUBMARINE';
GRANT ALL PRIVILEGES ON codem.* TO 'codem'@'localhost';

USE codem;

DROP TABLE IF EXISTS users, events, attendance;

CREATE TABLE users
(
	uniqname varchar(10) PRIMARY KEY,
	admin bool DEFAULT false,
	joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events
(
	eventID int PRIMARY KEY AUTO_INCREMENT,
	name varchar(100) NOT NULL,
	host varchar(100) NOT NULL,
	datetime DATETIME NOT NULL,
	location varchar(100) NOT NULL,
	description varchar(2000) NOT NULL,
	accessCode varchar(10) NOT NULL,
    open bool NOT NULL DEFAULT 0,
	points DEC(3,2) NOT NULL,
	semester CHAR(5) NOT NULL,
	lastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE attendance
(
	attID int PRIMARY KEY AUTO_INCREMENT,
	uniqname varchar(10),
	eventID int,
	logTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (uniqname) REFERENCES users(uniqname),
	FOREIGN KEY (eventID) REFERENCES events(eventID)
);
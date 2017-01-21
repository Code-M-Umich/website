USE codeM;

DROP TABLE IF EXISTS users, events, attendance;

CREATE TABLE users
(
	uniqname varchar(10) PRIMARY KEY,
	admin bool DEFAULT false
);

CREATE TABLE events
(
	eventid int PRIMARY KEY AUTO_INCREMENT,
	name varchar(100) NOT NULL,
	host varchar(100) NOT NULL,
	datetime varchar(100) NOT NULL,
	location varchar(100) NOT NULL,
	description varchar(2000) NOT NULL,
	access varchar(10) NOT NULL,
    open bool NOT NULL DEFAULT 0,
	points DEC(3,2) NOT NULL
);

CREATE TABLE attendance
(
	attid int PRIMARY KEY AUTO_INCREMENT,
	uniqname varchar(10),
	event int,
	FOREIGN KEY (uniqname) REFERENCES WINTER2017_users(uniqname),
	FOREIGN KEY (event) REFERENCES WINTER2017_events(eventid)
);
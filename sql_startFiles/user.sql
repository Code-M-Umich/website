CREATE USER 'website'@'localhost' IDENTIFIED BY '<password>'
GRANT SELECT,INSERT,UPDATE ON codem.users TO 'website'@'localhost';
GRANT SELECT,INSERT,UPDATE ON codem.events TO 'website'@'localhost';
GRANT SELECT,INSERT,UPDATE ON codem.attendance TO 'website'@'localhost';
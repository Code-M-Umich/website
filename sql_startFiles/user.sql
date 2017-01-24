CREATE USER 'website'@'localhost' IDENTIFIED BY '<password>'
GRANT SELECT,INSERT,UPDATE,DELETE ON codem.users TO 'website'@'localhost';
GRANT SELECT,INSERT,UPDATE,DELETE ON codem.events TO 'website'@'localhost';
GRANT SELECT,INSERT,UPDATE,DELETE ON codem.attendance TO 'website'@'localhost';
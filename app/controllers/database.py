import pymysql
from app import config

#database stuff
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "codem"
MYSQL_PASSWORD = "YELLOWSUBMARINE"
MYSQL_DB = "codem"

def openDBConnection():
	connectOpts = {
		'host' : MYSQL_HOST, 
		'port' : MYSQL_PORT, 
		'user' : MYSQL_USER, 
		'passwd' : MYSQL_PASSWORD, 
		'db' : MYSQL_DB
	}
	# fix for local mysql using path for unix_socket
	if config.args.socket:
		connectOpts['unix_socket'] = config.args.socket
	conn = pymysql.connect(**connectOpts)
	cur = conn.cursor()
	return conn, cur

def closeDBConnection(conn,cur):
	if conn:
		conn.close()
	if cur:
		cur.close()

def DBCommit(conn):
	conn.commit()
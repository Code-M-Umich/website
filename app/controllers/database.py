import pymysql

conn = None
cur = None

#database stuff
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "codem"
MYSQL_PASSWORD = "YELLOWSUBMARINE"
MYSQL_DB = "codem"

def openDBConnection():
	global conn,cur
	conn = pymysql.connect( host=MYSQL_HOST, port=MYSQL_PORT, 
		user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB)
	cur = conn.cursor()
	return cur

def closeDBConnection():
	global conn, cur
	if conn:
		conn.close()
	if cur:
		cur.close()

def DBCommit():
	conn.commit()
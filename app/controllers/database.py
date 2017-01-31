from app import app, config
import pymysql

conn = None
cur = None

# MySQL
def openDBConnection():
	global conn,cur
	conn = pymysql.connect(
		host=app.config["MYSQL_HOST"], port=app.config["MYSQL_PORT"], 
		user=app.config["MYSQL_USER"], passwd=app.config["MYSQL_PASSWORD"],
		db=app.config["MYSQL_DB"])
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
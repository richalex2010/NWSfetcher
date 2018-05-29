import MySQLdb

db=MySQLdb.connect(host="db739889303.db.1and1.com",db="db739889303",user="dbo739889303",passwd="cga8aJsEuawrvwbU04TY!",port=3306)
cur=db.cursor()
cur.execute("SHOW TABLES")
print(cur.fetchall())
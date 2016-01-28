import MySQLdb

def connection():

    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "heybaberiba",
                           db = "pythonprogramming")

    c = conn.cursor()

    return c, conn

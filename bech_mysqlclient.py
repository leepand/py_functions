from __future__ import print_function
import time

def query_10k(cur):
    t = time.time()
    for _ in range(10000):
        cur.execute("SELECT 1,2,3,4,5")
        res = cur.fetchall()
        assert len(res) == 1
        assert res[0] == (1,2,3,4,5)
    return time.time() - t


def mysql_connector_python():
    import mysql.connector
    conn = mysql.connector.connect(user='root', host='localhost')
    print("MySQL Connector/Python:", query_10k(conn.cursor()), "[sec]")


def mysqlclient():
    ## 安装：pip install mysqlclient 或 pip install git+https://github.com/PyMySQL/mysqlclient-python.git
    import MySQLdb
    conn = MySQLdb.connect(user='root', host='localhost')
    print("mysqlclient:", query_10k(conn.cursor()), "[sec]")


def pymysql():
    import pymysql
    conn = pymysql.connect(user='root', host='localhost')
    print("PyMySQL:", query_10k(conn.cursor()), "[sec]")
#https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python
#https://gist.github.com/methane/90ec97dda7fa9c7c4ef1
for _ in range(10):  # for PyPy warmup
    mysql_connector_python()
    mysqlclient()
    pymysql()

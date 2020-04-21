# -*- coding: utf-8 -*- 

import mysql.connector as mysql
import sys
#reload(sys)
#考虑注释是中文
#sys.setdefaultencoding('utf8')

conn = mysql.connect(host='localhost',user='root',password='',database='information_schema')
cursor = conn.cursor()
cursor.execute("select table_name from information_schema.tables where table_schema='Arthur_manage' and table_type='base table'")
tables = cursor.fetchall()

markdown_table_header = """### %s 
字段名 | 字段类型 | 默认值 | 注解
---- | ---- | ---- | ---- 
"""
markdown_table_row = """%s | %s | %s | %s
"""
#保存输出结果
f = open('markdown.out','w')

for table in tables:
    cursor.execute("select COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,COLUMN_COMMENT from information_schema.COLUMNS where table_schema='Arthur_manage' and table_name='%s'"% table)
    tmp_table = cursor.fetchall()
    p = markdown_table_header % table;
    for col in tmp_table:
        p += markdown_table_row % col
    #print p
    f.writelines(p)
f.close()


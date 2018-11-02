# -*- coding: UTF-8 -*- 
"""
我将数据库连接相关的一些用户名/密码/host/port等各种东西作为一个string保存在了数据库中，我要用MySQLdb检查这些数据库连接信息是够能正常使用，需要将数据库信息中的用户名/密码/host/port等信息作为参数传给MySQLdb.Connect()。者就需要将'{"host":"192.168.11.22", "port":3306, "user":"abc","passwd":"123", "db":"mydb", "connect_timeout":10}'”这样的string转化为dict。

在python中，将string转为一个dict，我所知有如下3中方法：
1. ast.literal_eval() 这是我常用的，依赖python2.6以上，据介绍时说比直接eval更安全一些，我没细究哈。
2. eval() 在string内容比较可控/安全的前提下，eval是不错的方法。
3. json.loads() 用json提供的loads方法是不错的，不过key/value中的string被转化为了unicode哦。

看实例代码：https://github.com/smilejay/python/blob/master/py2014/string2dict.py
其他类似，比如list '[...]'
"""
import MySQLdb
import ast
import json

def my_run():
    try:
        s = '{"host":"192.168.11.22", "port":3306, "user":"abc",\
              "passwd":"123", "db":"mydb", "connect_timeout":10}'
        d = ast.literal_eval(s)
        print type(d)
        print d
        d1 = eval(s)
        print type(d1)
        print d1
        d2 = json.loads(s)
        print type(d2)
        print d2
        MySQLdb.Connect(host=d['host'], port=d['port'], user=d['user'],
                        passwd=d['passwd'], db=d['db'],
                        connect_timeout=d['connect_timeout'])
        print 'right'
    except Exception, e:
        print 'wrong %s' % e
 
 
if __name__ == '__main__':
    my_run()
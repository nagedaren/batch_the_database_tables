# batch_the_database_tables
批量更新数据库中按月份分表
启动方式：python batch_the_database_tables.py conf/conf.ini

可以自己重新命名配置一个conf.ini启动。

conf.ini配置项

[db]

names=bp_pay,members,bp_fansmore

;要更新的数据库名称，可以是多个，用“，“分隔

charset=utf8

num=2

;每次增加几个月的表

[server]

host=ip#需要自己填写mysql的ip

port=3306

user=root

password=123456

备注：

python 需要有 pymysql 模块

没有pymysql 模块的话，先确保已经安装pip,

之后pip install pymysql安装即可

工作原理：

根据最新的月份分表增加新的月份分表

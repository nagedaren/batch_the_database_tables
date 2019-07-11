# -*- coding: utf-8 -*-
__author__ = 'xiaoxu12'
from DBTool import DBTool
import ConfigParser
import os
import sys
import shutil
from ReadFiles import ReadFiles
reload(sys)
sys.setdefaultencoding('utf8')
import pymysql

def deeltables(list):
    list2=[]
    if list:
        yymm=0
        flag=False
        table_temp=''
        for row in list:
            if row[0][-4:].isdigit():#是按月分表
                print(row[0])
                if flag==False:#第一次找到月份表
                    flag=True
                    table_temp=row[0][:-4]
                if table_temp==row[0][:-4]:#同一种表
                    if int(row[0][-4:]) >yymm:
                        yymm=int(row[0][-4:])
                else:#已经找到最大日期的表了，下一个表还是月份表
                    list2.append(str(table_temp)+str(yymm))
                    flag=True
                    yymm=0
                    table_temp=row[0][:-4]
            else:#已经找到最大日期的表，下一个表不是月份表
                if flag:
                    list2.append(str(table_temp)+str(yymm))
                    yymm=0
                    flag=False
    return  list2

def deeltables2(list):
    '''找到按月分表最新月份表的集合'''
    list2=[]
    if list:
        yymm=0
        table_temp=''
        for row in list:
            if row[0][-4:].isdigit():#是按月分表
               # print(row[0])
                table_temp=row[0][:-4]
                yymm=int(row[0][-4:])
                if len(list2)==0:
                    list2.append(str(table_temp)+str(yymm))
                    continue;
                for index, yymmtable in enumerate(list2):
                    if yymmtable[:-4]==table_temp:
                        if int(yymmtable[-4:])<yymm:
                            list2.remove(yymmtable)
                            list2.append(str(table_temp)+str(yymm))
                    elif index+1==len(list2):
                        list2.append(str(table_temp)+str(yymm))
                   # if list2.__contains__(yymmtable) and list2.index(yymmtable)==len(list2): #没有匹配的，这是个新的
                    #    list2.append(str(table_temp)+str(yymm))
    return  list2



def main(host,port,user,password,names,charset,confname,num):
    for name in names:
        conn_dict = {'host': host, 'port': port, 'user': user, 'password': password, 'db': name, 'charset': charset}
        print conn_dict
        conn = DBTool(conn_dict)
        sql_gettables = "select table_name from information_schema.`TABLES` WHERE TABLE_SCHEMA = '"+name+"';"
        print sql_gettables
        list = conn.execute_query(sql_gettables)
        #list2=deeltables(list)
        list3=deeltables2(list)
        print list3
        # 文件目标路径，先清空，再新建一个目录
        boot_file_path=os.path.split(os.path.realpath(__file__))[0]
        mysql_file_path = boot_file_path +'/mysqlscript/'+confname
        print mysql_file_path
        if not os.path.exists(mysql_file_path):
            os.mkdir(mysql_file_path)
        else:
            shutil.rmtree(mysql_file_path)
            os.mkdir(mysql_file_path)

        mysqldump_commad_dict = {'dumpcommad': 'mysqldump --no-data ', 'server': host, 'user': user,
                                'password': password, 'port': port, 'db':name}

        if list3:
            for row in list3:
                print(row)
                # 切换到新建的文件夹中
                os.chdir(mysql_file_path)
                #表名
                dbtable = row
                #文件名
                exportfile =  row + '.sql'
                print exportfile
                # mysqldump 命令
                sqlfromat = "%s -h%s -u%s -p%s -P%s %s %s >%s"
                # 生成相应的sql语句
                sql = (sqlfromat % (mysqldump_commad_dict['dumpcommad'],
                                    mysqldump_commad_dict['server'],
                                    mysqldump_commad_dict['user'],
                                    mysqldump_commad_dict['password'],
                                    mysqldump_commad_dict['port'],
                                    mysqldump_commad_dict['db'],
                                    dbtable,
                                    exportfile))
                print(sql)
                result = os.system(sql)
                if result:
                    print('export ok')
                else:
                    print('export fail')
        m_readfiles=ReadFiles() 
        m_readfiles.readfiles(conn_dict,confname,num)
        os.chdir(boot_file_path)#切换回来

if __name__ == '__main__':


    confpath = sys.argv[1]
    if not os.path.exists(confpath):
        print confpath+'配置文件不存在'
    conf = ConfigParser.ConfigParser()

    conf.read(confpath)  # 文件路径
    confname = confpath[confpath.find("/") + 1:confpath.find(".ini")]

    names = conf.get("db", "names")
    names=names.split(',')
    print names
    charset = conf.get("db", "charset")
    print charset
    #num = "1" 
    num = conf.get("db", "num")
    print num
    host = conf.get("server", "host")
    print host
    port = conf.get("server", "port")
    port =int(port)
    print port
    user= conf.get("server", "user")
    print user
    password = conf.get("server", "password")
    print password

    main(host,port,user,password,names,charset,confname,num)


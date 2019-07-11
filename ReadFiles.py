#coding:utf-8
import ConfigParser
import datetime
import time
import copy
from DBTool import DBTool
__author__ = 'xiaoxu12'
import os
class ReadFiles:
    def datetime_offset_by_month(self,datetime1, n = 1):
        one_day = datetime.timedelta(days = 1)
        q,r = divmod(datetime1.month + int(n), 12)
        datetime2 = datetime.datetime(
            datetime1.year + q, r + 1, 1) - one_day

        if datetime1.month != (datetime1 + one_day).month:
            return datetime2
        if datetime1.day >= datetime2.day:
            return datetime2
        return datetime2.replace(day = datetime1.day)
    def readfiles(self,conn_dict,confname,num=1):
        filepath = os.path.split(os.path.realpath(__file__))[0] +'/mysqlscript/'+confname
        # 切换到新建的文件夹中
        os.chdir(filepath)
        pathDir = os.listdir(filepath)
        for file in pathDir:
            lines = open(file, "r")
            content = ""
#            content = content + "\n"
            for line in lines:
                if not (str(line).startswith("--") or str(line).startswith("/*") ):
                    if(line!="\n" and str(line).startswith(") ENGINE")):
                        content = content +"\n"+ ");"
                    else:
                        content = content + line
            #将提炼后的内容重新写入文件
            yymm=file[-8:-4]
            tempyymm=yymm
            for i in range(1,int(num)+1):
                m_datetime=datetime.datetime(2000+int(yymm[:-2]),int(yymm[-2:]),2)
                newdate=self.datetime_offset_by_month(m_datetime,i)
                content= content.replace(tempyymm,newdate.strftime('%y%m'))
                tempyymm=newdate.strftime('%y%m')
                sqlcontent=copy.deepcopy(content)
                print sqlcontent
                index=0
                while sqlcontent.find(';',index)!=-1:
                    conn = DBTool(conn_dict)
                    conn.execute_noquery(sqlcontent[index:sqlcontent.find(';',index)])
                    sqlcontent=sqlcontent[sqlcontent.find(';',index)+1:]
                    conn = DBTool(conn_dict)
                    conn.execute_noquery(sqlcontent)
                    index=sqlcontent.find(';',index)+1

                
           # fp = open(file, 'w')
           # fp.write(content)
           # fp.close()


if __name__=='__main__':
    a =ReadFiles()
    conf = ConfigParser.ConfigParser()

    conf.read("conf/conf.ini")  # 文件路径
    names = conf.get("db", "names")
    names = names.split(',')
    print names
    charset = conf.get("db", "charset")
    print charset
    # num = "1"
    num = conf.get("db", "num")
    print num
    host = conf.get("server", "host")
    print host
    port = conf.get("server", "port")
    port = int(port)
    print port
    user = conf.get("server", "user")
    print user
    password = conf.get("server", "password")
    print password
    conn_dict = {'host': host, 'port': port, 'user': user, 'password': password, 'db': names[0], 'charset': charset}
    a.readfiles(conn_dict,3)

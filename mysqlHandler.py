from __future__ import division
import MySQLdb as mdb
import sys
import math
from config import MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB_NAME


def createDB():
    con = None
    try:
        con = get_con() 
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS idf;")
        cur.execute("DROP TABLE IF EXISTS doc_num;")
        cur.execute("CREATE TABLE `idf` (`ID` int(11) unsigned NOT NULL auto_increment,"
                "`word` char(80) UNIQUE NOT NULL,"
                "`occurrence` int(11) unsigned NOT NULL,"
                "primary key (`ID`));")
        cur.execute("CREATE TABLE `doc_num` (`ID` int(11) unsigned NOT NULL auto_increment,"
                "`total_num` int(11) NOT NULL,"
                "primary key (`ID`));")
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:    
        if con:    
            con.close()

def incr_occurrence(word,con):
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(1) FROM idf WHERE word = '{0}'".format(word))
        #if the word exists in the idf table, then increse the occurence 
        if cur.fetchone()[0]:
            sqlq = "UPDATE idf SET occurrence = occurrence+1 WHERE word = '%s'" % word
            print sqlq
            data = (word,1)
            cur.execute(sqlq)
            con.commit()
        #if not create a new row
        else:
            sqlq = "INSERT INTO idf (word,occurrence) values (%s,%s)"
            data = (word,1)
            print sqlq,data
            cur.execute(sqlq,data)
            con.commit()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def incr_total_doc_number(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(1) FROM doc_num WHERE ID = 1")
        if cur.fetchone()[0]:
            sqlq = "UPDATE doc_num SET total_num = total_num + 1 WHERE ID = 1"
            cur.execute(sqlq)
            con.commit()
        else:
            sqlq = "INSERT INTO doc_num (total_num) values (1)"
            cur.execute(sqlq)
            con.commit()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def get_idf(word,con):
    try:
        cur = con.cursor()
        cur.execute("SELECT occurrence FROM idf WHERE word = '{0}'".format(word))
        temp = cur.fetchone()
        occurrence_time = temp[0] if temp else 0
        cur.execute("SELECT total_num FROM doc_num WHERE ID = 1")
        D_num = cur.fetchone()[0]

        idf = math.log(D_num/(1+occurrence_time))
        return idf
    except mdb.Error,e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def get_con():
    con = None
    try:
        con = mdb.connect(host = MYSQL_HOST,user = MYSQL_USER, passwd = MYSQL_PASSWD, db = MYSQL_DB_NAME)
        return con
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

if __name__ == "__main__":
    createDB()

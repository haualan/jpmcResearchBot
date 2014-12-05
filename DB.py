from __future__ import division
import MySQLdb as mdb
import sys
import math
from config import MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB_NAME


def createTablesinDB():
    # drops existing tables and then creates all the necessary tables for the API
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

        cur.execute("DROP TABLE IF EXISTS T_exclusion;")
        cur.execute("DROP TABLE IF EXISTS T_inclusion;")
        create_T_exclusion_str = "CREATE TABLE `T_exclusion` (`id` int(11) NOT NULL AUTO_INCREMENT,`word` varchar(200) NOT NULL,PRIMARY KEY (`id`),UNIQUE KEY `word_UNIQUE` (`word`));"
        create_T_inclusion_str = "CREATE TABLE `T_inclusion` (`id` int(11) NOT NULL AUTO_INCREMENT,`word` varchar(200) NOT NULL,PRIMARY KEY (`id`),UNIQUE KEY `word_UNIQUE` (`word`));"
        cur.execute(create_T_exclusion_str)
        cur.execute(create_T_inclusion_str)


    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:    
        if con:    
            con.close()

def incr_occurrence(word,con):
    # increments the count for the particular word
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
    # increments the count of documents processed
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
    # initializes the connection with the database
    con = None
    try:
        con = mdb.connect(host = MYSQL_HOST,user = MYSQL_USER, passwd = MYSQL_PASSWD, db = MYSQL_DB_NAME)
        return con
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

def execSQL(sqlStr):
    #executes a sql statement to the database and returns a tuple of tuples
    con = get_con()
    try:
        cur = con.cursor()
        cur.execute(sqlStr)
        return cur.fetchall()
    except mdb.Error,e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    con.close()

def getInclusionList():
    # returns an array of words that needs to be included in the keywords
  result = execSQL("SELECT word FROM T_inclusion")
  return list(map(lambda x: x[0],result))

def getExclusionList():
    # returns an array of words that needs to be excluded in the keywords
  result = execSQL("SELECT word FROM T_exclusion")
  return list(map(lambda x: x[0],result))


if __name__ == "__main__":
    # createTablesinDB()
    con = get_con()
    # print execSQL("SELECT word FROM T_inclusion")
    print getInclusionList()



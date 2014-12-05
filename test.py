import MySQLdb as mdb
import sys

def getInclusionList():
  return execSQL("SELECT word FROM T_inclusion")

def getExclusionList():
  return execSQL("SELECT word FROM T_exclusion")


def execSQL(sqlStr):
  result=[]
  try:
      con = mdb.connect(host="localhost", # your host, usually localhost
                       user="root", # your username
                        # passwd="somepasswd", # your password
                        db="jpmcResearchBot_DB") # name of the data base

      # you must create a Cursor object. It will let
      #  you execute all the queries you need
      cur = con.cursor()
      cur.execute("SELECT VERSION()")

      ver = cur.fetchone()
      
      print "Database version : %s " % ver

      # Use all the SQL you like
      cur.execute(sqlStr)

      # print all the first cell of all the rows
      # for row in cur.fetchall() :
      #     print row[0]

      result = list(map(lambda x: x[0],cur.fetchall()))




      
  except mdb.Error, e:
    
      print "Error %d: %s" % (e.args[0],e.args[1])
      sys.exit(1)
      
  finally:    
          
      if con:    
          con.close()

  return result

if __name__ == '__main__':
  inclusionList = getInclusionList()
  exlusionList = getExclusionList()
  print inclusionList, exlusionList
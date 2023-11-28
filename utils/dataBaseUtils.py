# Libs
import firebirdsql

# Locale files
from utils.sysUtils import exitWithLog, decrypt
from classes.iniFile import iniFile
from utils.messagesUtils import formatDbConnectError, formatSQLExecError, formatSQLReadError

#Exceptions 
class noneConnectionError(Exception):
   pass

class intelectualSysDB:
   def __init__(self):
      try:
         self.connection = None
         self.fullPath = self.getFullPath()
         self.path = self.getPath(self.fullPath)
         self.host = self.getHost(self.fullPath)

      except Exception as ex:
         exMessage = str(ex)
         exitWithLog(formatDbConnectError(exMessage))


   def getPath(self, fullPath):
      iniPos = fullPath.find(':') + 1
      endPos = len(fullPath)
      
      return fullPath[iniPos : endPos]


   def getHost(self, fullPath):
      iniPos = 0
      endPos = fullPath.find(':')
      return fullPath[iniPos : endPos]
   

   def getFullPath(self):
      ini = iniFile()
      return decrypt(ini.getValue('DBCnxSystem'))
   

   def connect(self):
      self.connection = None
      try:
         self.connection = firebirdsql.connect(
            user = "SYSDBA",
            password = "masterkey",
            database = fr"{self.path}",
            host = fr"{self.host}")

         return self.connection      
      
      except Exception as ex:
         exMessage = str(ex)
         exitWithLog(formatDbConnectError(exMessage))


   def disconnect(self):
      if self.connection is not None:
         self.connection.close()


class SQLHandler:
   def __init__(self, connection):
      try:
         if connection is None: 
            raise noneConnectionError('Nenhuma conexão foi específicada na instancia da classe SQLHandler')

         self.connection = connection
         self.cur = connection.cursor()
         
      except Exception as e:
         exMessage = str(e)
         exitWithLog(formatDbConnectError(exMessage))
   

   def close(self):
      self.cur.close()
      self.connection = None
      

   def executeQuery(self, sql):
      try:
         self.connection.begin()
         self.cur.execute(sql)
         self.connection.commit()

      except Exception as e:
         exMessage = str(e)
         exitWithLog(formatSQLExecError(sql, exMessage))


   def fetchAll(self, sql):
      try:
         self.cur.execute(sql)
         return self.cur.fetchall()   
      
      except Exception as e:
         exMessage = str(e)
         exitWithLog(formatSQLReadError(sql, exMessage))
         

   def fetchOne(self, sql):
      try:
         self.cur.execute(sql)
         return self.cur.fetchone()
         
      except Exception as e:
         exMessage = str(e)
         exitWithLog(formatSQLReadError(sql, exMessage))

      
   def selectCount(self, table, where):
      sql = f"SELECT COUNT(*) FROM {table} WHERE {where}"
      return self.fetchOne(sql)
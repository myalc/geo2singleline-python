#!/usr/bin/python
from typing import Iterable
import psycopg2
import conf

class DatabaseConnectionClass(object):
  'Class for managing database connections and operations'

  __user = None
  __passw = None
  __host = None
  __port = None
  __database = None
  __conn = None

  def __init__(self, *args, **kwargs):
    super(DatabaseConnectionClass, self).__init__(*args, **kwargs)
    self.__createConnectionHandle()
    print(("initialized: {0}").format(DatabaseConnectionClass.__doc__))
  # end function

  def __del__(self):
    self.__destroyConnectionHandle()
    print(("destroyed: {0}").format(DatabaseConnectionClass.__doc__))
  # end function

  def __createConnectionHandle(self):
    self.__user = conf.get("/db_connection/user")
    self.__passw = conf.get("/db_connection/passw")
    self.__host = conf.get("/db_connection/host")
    self.__port = conf.get("/db_connection/port")
    self.__database = conf.get("/db_connection/name")
    
    try:
      self.__conn = psycopg2.connect(database=self.__database, user=self.__user, password=self.__passw, host=self.__host, port=self.__port)
      
      # Get version info
      cursor = self.__conn.cursor()
      cursor.execute("select version()")
      version = cursor.fetchone()
      print("Connection established to: ", version)
      cursor.close()
    except psycopg2.OperationalError as e:
      print(("Exception: {0}").format(e))
      self.__conn = None
  #end function

  def __destroyConnectionHandle(self):
    if self.__conn:
      self.__conn.close()
      print("Disconnected from database!")
  # end function
  
  def _isConnected(self):
    if self.__conn:
      return True
    else:
      print("Not connected to database!")
      return None
  # end function

  def _select(self, sql, parms=None):
    #print(("Select: SQL: {0}, PARMS: {1}").format(sql, parms))
    rs = None
    try:
      cursor = self.__conn.cursor()
      cursor.execute(sql, parms)
      rs = cursor.fetchall()
      cursor.close()    
    except psycopg2.OperationalError as e:
      print(("Exception: {0}").format(e))
      return None
    print(("Result length: {0}").format(len(rs)))
    return rs
  # end function

  def _execute(self, sql, parms=None, commit=False):
    #print(("Execute: SQL: {0}, PARMS: {1}, COMMIT: {2}").format(sql, parms, commit))
    try:
      cursor = self.__conn.cursor()
      cursor.execute(sql, parms)
      if commit:
        self.__conn.commit()
      cursor.close()
    except psycopg2.OperationalError as e:
      print(("Exception: {0}").format(e))
      return None
    return conf.SUCCESS
  # end function

  def _bulkInsert(self, sql, chunk, commit=False):
    #print(("BULK INSERT: SQL: {0}, PARMS: {1}, COMMIT: {2}").format(sql, chunk, commit))
    if not isinstance(chunk, Iterable):
      return None
    try:
      cursor = self.__conn.cursor()
      cursor.executemany(sql, chunk)
      if commit:
        self.__conn.commit()
      cursor.close()
    except psycopg2.OperationalError as e:
      print(("Exception: {0}").format(e))
      return None
    return conf.SUCCESS
  # end function          
# end class


class DataMgmtClass(DatabaseConnectionClass):
  'Class for managing data in database'

  def __init__(self, *args, **kwargs):
    super(DataMgmtClass, self).__init__(*args, **kwargs)
    print(("initialized: {0}").format(DataMgmtClass.__doc__))
  # end function

  def __del__(self):
    super(DataMgmtClass, self).__del__()
    print(("destroyed: {0}").format(DataMgmtClass.__doc__))
  # end function

  def _getConnectivity(self):
    if not self._isConnected():
      return None
    
    # select gidn1,gidn2 from t_conns union select gidn2,gidn1 from t_conns
    sql = ("select {0} from {1} union select {2} from {3}")\
            .format(conf.get("/db_tables/connectivity/cols")
                    ,conf.get("/db_tables/connectivity/name")
                    ,conf.get("/db_tables/connectivity/cols_r")
                    ,conf.get("/db_tables/connectivity/name"))
    conns = self._select(sql)
    return conns    
  # end function

  def _insertPlainNodes(self, position):
    nodes = list()
    sql = ("insert into {0} ({1}) values (%(gid)s, ST_GeomFromText('POINT(%(x)s %(y)s)', 4326))")\
          .format(conf.get("/db_tables/plain_nodes/name")
                 ,conf.get("/db_tables/plain_nodes/cols"))
    for k, v in position.items():
      nodes.append( {'gid':k, 'x':v[0], 'y':v[1]} )
    return self._bulkInsert(sql, nodes, True)
  # end function

  def _insertPlainLines(self, schema):
    lines = list()
    sql = ("insert into {0} ({1}) values (%(gidn1)s, %(gidn2)s, ST_GeomFromText(%(vals)s, 4326))")\
          .format(conf.get("/db_tables/plain_lines/name")
                 ,conf.get("/db_tables/plain_lines/cols")) 
    for k, vs in schema.items():
      if vs:
        pl = "LINESTRING ("
        for v in vs:
          pl  = pl + ("{0} {1},").format(v[0], v[1])
        pl = pl[:-1] + ")"
        lines.append( {'gidn1':k[0], 'gidn2':k[1], 'vals':pl} )
    return self._bulkInsert(sql, lines, True)
  # end function

  def _cleanUp(self):
    self._execute("truncate table {0}".format(conf.get("/db_tables/plain_nodes/name")), None, True)
    self._execute("truncate table {0}".format(conf.get("/db_tables/plain_lines/name")), None, True)
  # end function
  
# end class

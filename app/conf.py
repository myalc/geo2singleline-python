#!/usr/bin/python


#------------------------------------------------------------------------------
def get(path, default=None):
  'xpath style get'
  elem = conf_dict
  try:
    for x in path.strip("/").split("/"):
      elem = elem.get(x)
  except:
    pass
  if not elem:
    print(("Cannot find: '{0}'").format(path))
    elem = default
    
  return elem
#------------------------------------------------------------------------------

conf_dict = {
  'db_connection': {
    'user':'myuser',
    'passw':'mypass',
    #'host':'localhost',
    'host':'db',
    'port':5432,
    'name':'mydb'
  },
  'db_tables': {
    'connectivity': {
      'name': 't_conns', 
      'cols': 'gidn1,gidn2', 
      'cols_r': 'gidn2,gidn1'
    },
    'plain_nodes': {
      'name': 't_plain_nodes', 
      'cols': 'gid,geog'
    },
    'plain_lines': {
       'name': 't_plain_lines',
       'cols': 'gidn1,gidn2,geog'
    }
  },
  'draw': {
    'offset': {
      'x':10, 
      'y':20
    },
    'overlapFactor':0.15
  }
}
#------------------------------------------------------------------------------

SUCCESS = 1


#!/usr/bin/python
import sys
import conf
from database import DataMgmtClass
from location import LocationBuilderClass


class GraphBuilderClass(DataMgmtClass):
  'Class for building the graph'
  
  __graph_conns = {}
  __graph_childcnt = {}
  
  def __init__(self, *args, **kwargs):
    super(GraphBuilderClass, self).__init__(*args, **kwargs)
    print(("initialized: {0}").format(GraphBuilderClass.__doc__))
  # end function
    
  def __del__(self):
    super(GraphBuilderClass, self).__del__()
    print(("destroyed: {0}").format(GraphBuilderClass.__doc__))
  # end function
    
  def __sizeInfo(self):
    return ("Graph Builder. conns:{0:.4f} KB, child counts:{1:.4f} KB")\
      .format(sys.getsizeof(self.__graph_conns)/1024
             ,sys.getsizeof(self.__graph_childcnt)/1024)
  # end function

  def _buildGraph(self):
    raw_conns = self._getConnectivity()
    
    if raw_conns:
      for c in raw_conns:
        if not self.__graph_conns.get(c[0], None):
          self.__graph_conns[c[0]] = set()
          self.__graph_childcnt[c[0]] = 0
        self.__graph_conns[c[0]].add(c[1])

    print(("CONNS(EDGES): {0}").format(self.__graph_conns))
    print(self.__sizeInfo())
  # end function
  
  def _getConns(self):
    return self.__graph_conns
  # end function
  
  def _hasConns(self):
    if self.__graph_conns:
      return conf.SUCCESS
    else:
      return None
    # end function
  
  def _getChildCnts(self):
    return self.__graph_childcnt
  # end function
# end class


class GraphClass(LocationBuilderClass, GraphBuilderClass):
  'Class for graph implementations'
  
  __start = None

  def __init__(self, *args, **kwargs):
    super(GraphClass, self).__init__(*args, **kwargs)
    print(("initialized: {0}").format(GraphClass.__doc__))
  # end function
    
  def __del__(self):
    super(GraphClass, self).__del__()
    print(("destroyed: {0}").format(GraphClass.__doc__))
  # end function
    
  def __str__(self):
    return GraphClass.__doc__
  # end function
  
  def prepareGraph(self, start):
    self.__start = start
    self._buildGraph()
    self._prepareLocationBuilder(start)
  # end function
  
  def doDfs(self):
    v = self.__start
    visited = set()
    
    # perform Deep First Search on graph
    self.__doDfs(v, visited, self._getChildCnts())
    print(("VISITED: {0}").format(visited))
    print(("POSITION_2D[{0}]: {1}").format(len(self._getPosition2d()), self._getPosition2d()))
    print(("POSITION_GEO[{0}]: {1}").format(len(self._getPositionGeo()), self._getPositionGeo()))
  # end function

  def finalize(self):
    self._connect(self._getConns())
    self._cleanUp()
    self._insertPlainNodes(self._getPositionGeo())
    self._insertPlainLines(self._getPlainSchema())
  #end function

  def __doDfs(self, current, visited, childCnts, parent=None, level=0):
    #print(("Current: {0}").format(current))

    if parent is not None:
      #print(("locate: parent:{0}, current:{1}, level:{2}, siblingCnt:{4}")
              #.format(parent, current, level, parent, childCnts[parent]))
      # if the current node has a parent, then build 2d and cartesian connection between current and parent nodes
      self._locate(current, parent, childCnts[parent])
      childCnts[parent] = childCnts[parent] + 1
    else:
      #print(("do not locate: current:{0} is root").format(current))
      pass

    if current in self._getConns():
      for neighbour in self._getConns()[current]:
        if neighbour not in visited:
          visited.add(current)
          level = level + 1
          self.__doDfs(neighbour, visited, childCnts, current, level)
          level = level - 1
    return
  # end function

# end class

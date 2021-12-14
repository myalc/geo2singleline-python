#!/usr/bin/python
from sys import _current_frames
import conf
from longconnect import LongConnectFacade


class LocationBuilderClass(object):
  'Class for specifying locations and connections of plain schema'

  __offs = None
  __marginInfo = {}
  __position_2d = {}
  __position_geo = {}
  __plain_schema = {}
  __longConnect = None

  def __init__(self, *args, **kwargs):
    super(LocationBuilderClass, self).__init__(*args, **kwargs)
    print(("initialized: {0}").format(LocationBuilderClass.__doc__))
    self.__longConnect = LongConnectFacade()
  # end function

  def __del__(self):
    super(LocationBuilderClass, self).__del__()
    print(("destroyed: {0}").format(LocationBuilderClass.__doc__))
  # end function

  def _prepareLocationBuilder(self, start):
    # set initial x and y points of start node
    self.__position_2d[start] = (0, 0)
    self.__position_geo[start] = (0, 0)
    self.__offs = conf.get("/draw/offset")
  #end function

  def _getPositionGeo(self):
    return self.__position_geo
  # end function

  def _getPosition2d(self):
    return self.__position_2d
  # end function

  def _getPlainSchema(self):
    return self.__plain_schema
  # end function

  def _locate(self, current, parent, siblingCnt):
    #print(("locate(current):{1} parent:{0}, siblingCnt:{2}").format(parent, current, siblingCnt))
    ixp = self.__position_2d.get(parent)[0]
    iyp = self.__position_2d.get(parent)[1]
    #print((" --> parent:{0} ix[{0}]:{1}, iy[{0}]:{2}").format(parent, ixp, iyp))

    if current not in self.__position_2d:
      ix = ixp + siblingCnt
      iy = iyp - 1
      # to prevent grid conflicts shift ix to right if necessary
      while ix in self.__marginInfo and self.__marginInfo[ix] < iy:
        ix = ix + 1
      
      self.__position_2d[current] = (ix, iy)
      geox = ix*self.__offs.get('x')
      geoy = iy*self.__offs.get('y')
      self.__position_geo[current] = (geox, geoy)
      #print((" --> self:{0} 2dx[{0}]:{1}, 3dy[{0}]:{2}").format(current, ix, iy))
      #print((" --> self:{0} geox[{0}]:{1}, geoy[{0}]:{2}").format(current, geox, geoy))

      # store gird info
      self.__marginInfo[ix] = iy
      #print((" --> marginInfo:{0}").format(self.__marginInfo))
    else:
      #print(("node {0} already located").format(current))
      # loop detected
      raise "Loop detected!"
    # end function
  
  def _connect(self, conns):
    #print(("POSITIN_2D: {0}").format(self.__position_2d))
    #print(("POSITION_GEO: {0}").format(self.__position_geo))
    if not self.__position_geo:
      print("There is no position data available!")
      return None
    
    for n1, cs in conns.items():
      for n2 in cs:
        #print(("n:{0}, n:{1}").format(n1, n2))
        if not self.__plain_schema.get((n1, n2), None) and not self.__plain_schema.get((n2, n1), None):
          self.__plain_schema[n1, n2] = list()
        
          points = list()
          points = self._makePoints(n1, n2)
          for point in points:
            self.__plain_schema[n1, n2].append(point)
      
    print(("PLAIN_SCHEMA[{0}]: {1}").format(len(self.__plain_schema), self.__plain_schema))
  # end function
  
  def _makePoints(self, n1, n2):
    points = list()

    if not self.__position_2d.get(n1) or not self.__position_2d.get(n2):
      return points
    
    #print(("_makePoints n:{0}, n:{1}").format(n1, n2))
    ix1 = self.__position_2d.get(n1)[0]
    iy1 = self.__position_2d.get(n1)[1]
    ix2 = self.__position_2d.get(n2)[0]
    iy2 = self.__position_2d.get(n2)[1]
    #print(("_makePoints ix1:{0}, iy1:{1}, ix2:{2}, iy2:{3}").format(ix1, iy1, ix2, iy2))
    
    #if abs(ix2-ix1) <= 1 and abs(iy2-iy1) <= 1:
    if abs(ix2-ix1) < 1 or abs(iy2-iy1) < 1:
      pos1 = self.__position_geo.get(n1)
      pos2 = self.__position_geo.get(n2)
      points.append(pos1)
      points.append(pos2)
    else:
      #print(("long way from '{0}' to '{1}'").format(n1, n2))
      points = self.__longConnect.makePoints(self.__position_geo.get(n1)
                                            ,self.__position_geo.get(n2))
    return points
  # end function
# end class

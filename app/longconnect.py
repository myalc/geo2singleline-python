#!/usr/bin/python
from abc import ABCMeta, abstractmethod
import conf


class LongConnectStrategy(object):
  'Abstract class for building long way connections'

  __metaclass__ = ABCMeta
  _offs = None
  _oX = None
  _start = None
  _end = None
    
  def __init__(self):
    self._offs = conf.get("/draw/offset")
    self._oX = conf.get("/draw/overlapFactor")
  # end function
  
  def setPoints(self, start, end):
    self._start = start
    self._end = end
    
  @abstractmethod
  def longConnect(self):
    raise "Method not implemented"
  # end function
#end class


class LongConnectStrategyW2E(LongConnectStrategy):
  'Class for "West->East" like connection'
  
  def longConnect(self):
    points = list()
    
    mid1 = (self._start[0] + self._offs.get('x')*self._oX
           ,self._start[1] - self._offs.get('y')*self._oX)
    mid2 = (self._end[0] - self._offs.get('x')*self._oX
           ,self._end[1] - self._offs.get('y')*self._oX)
    points.append(self._start)  
    points.append(mid1)
    points.append(mid2)
    points.append(self._end)
    
    return points
  # end function
# end class
    

class LongConnectStrategyN2S(LongConnectStrategy):
  'Class for "North->South" like connection'
  
  def longConnect(self):
    points = list()
    
    mid1 = (self._start[0] - self._offs.get('x')*self._oX
           ,self._start[1] - self._offs.get('y')*self._oX)
    mid2 = (self._end[0] - self._offs.get('x')*self._oX
           ,self._end[1] + self._offs.get('y')*self._oX)
    points.append(self._start)  
    points.append(mid1)
    points.append(mid2)
    points.append(self._end)
    
    return points
  # end function
# end class


class LongConnectStrategyNE2SW(LongConnectStrategy):
  'Class for "NorthEast->SouthWest" like connection'
  
  def longConnect(self):
    points = list()
    
    mid = (self._end[0], self._start[1])
    points.append(self._start)
    points.append(mid)
    points.append(self._end)
    
    return points
  # end function
# end class


class LongConnectStrategyNW2SE(LongConnectStrategy):
  'Class for "NorthWest->SouthEast" like connection'
  
  def longConnect(self):
    points = list()
    
    mid = (self._end[0], self._start[1])
    points.append(self._start)
    points.append(mid)
    points.append(self._end)
    
    return points
  # end function
#end class
# =============================================================================


class LongConnectFacade(object):
  'Connection Builder Class'

  __startPoint = None
  __endPoint = None
  __strategy = None

  def __init__(self):
    self.__strategy = LongConnectStrategy()
  # end function

  def makePoints(self, pos1, pos2):
    self.__adjustPoints(pos1, pos2)
    self.__clarifyStrategy()
    points = self.__strategy.longConnect()
    #print(("makePoints: {0}, strategy:{1}").format(points, self.__strategy.__doc__))
    
    return points
  # end function

  def __adjustPoints(self, pos1, pos2):
    # adjust start & end points
    if pos1[1] > pos2[1]:        # y1>y2
      self.__startPoint = pos1
      self.__endPoint = pos2
    elif pos1[1] < pos2[1]:      # y1<y2
      self.__startPoint = pos2
      self.__endPoint = pos1
    elif pos1[1] == pos2[1]:     # y1==y2
      if pos1[0] > pos2[0]:      # x1>x2
        self.__startPoint = pos1
        self.__endPoint = pos2
      elif pos1[0] < pos2[0]:    # x1<x2
        self.__startPoint = pos2
        self.__endPoint = pos1
  # end function
    
  def __clarifyStrategy(self):
    # decide for a strategy
    if self.__startPoint[1] == self.__endPoint[1]:   # y1==y2
      self.__strategy = LongConnectStrategyW2E()
    elif self.__startPoint[0] == self.__endPoint[0]: # x1==x2
      self.__strategy = LongConnectStrategyN2S()
    elif self.__startPoint[0] < self.__endPoint[0]:  # x1<x2
      self.__strategy = LongConnectStrategyNW2SE()
    elif self.__startPoint[0] > self.__endPoint[0]:  # x1>x2
      self.__strategy = LongConnectStrategyNE2SW()
      
    self.__strategy.setPoints(self.__startPoint, self.__endPoint)
  # end function
# end class






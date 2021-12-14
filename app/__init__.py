#!/usr/bin/python
from graph import GraphClass

if __name__ == '__main__':  
  g = GraphClass()
  g.prepareGraph(0)
  g.doDfs()
  g.finalize()
  
  print("End of main")

import os
import sys

def fileExists(file):
   return (os.path.isfile(rf"{file}"))


def getCurrentPath():
   if getattr(sys, 'frozen', False):
      return os.path.abspath(sys.executable)
   else:
      return os.path.abspath(os.path.dirname(__file__))
   

def getCurrentDisk():
   return os.path.abspath(os.sep)
   
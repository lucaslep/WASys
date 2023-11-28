import os 
from utils.fileUtils import getCurrentPath

# DatBase connection 
CONNECTION = None
PATH = None
DIR = None

def setApplicationPathAndDir(file):
   global PATH
   global DIR
   PATH = getCurrentPath()
   DIR = os.path.dirname(PATH)

def getApplicationPath():
   return PATH

def getApplicationDir():
   return os.path.dirname(PATH)

def setConnection(conn):
   global CONNECTION
   CONNECTION = conn 

def getConnection():
   return CONNECTION






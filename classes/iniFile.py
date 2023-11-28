# Libs
from utils.fileUtils import fileExists

# Variveis globais 
import config.globals as globals

class iniFile:
   def __init__(self):
      self.path = rf'{globals.DIR}\IntelectualSys.ini'

      if (not fileExists(self.path)):
         raise FileNotFoundError(f'O arquivo ini: {self.path} não foi encontrado!')
      
      self.readIniFile()


   def readIniFile(self):
      with open(self.path, 'r', encoding='UTF-8') as ini:
         self.lines = clearTextLines(ini.readlines())


   def getValue(self, valueName):
      value = ''

      for line in self.lines:
         if valueName in line:
            startPos = line.find('=') + 1
            value = line[startPos : len(line)]
            
            return value


def clearTextLines(lines):
   return [line.rstrip() for line in lines]
         


      

      


      





    
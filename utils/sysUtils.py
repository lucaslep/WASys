import datetime
import locale
import sys

def log(message):
   locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
   timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

   log_message = f"{timestamp}: {message}\n"

   with open("log.txt", "a") as log_file:
      log_file.write(log_message)


def logAndPrint(message):
   log(message)
   print(message)


def exitWithLog(message):
   log(message)
   sys.exit(message)
   

def decrypt(s):
   sDecrypted = ''

   for char in s:
      sDecrypted = sDecrypted + \
         chr(23 ^ ord(bytearray(char, encoding='UTF-8')))

   return sDecrypted

   
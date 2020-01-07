import os
import subprocess

class logHis:

  print("System Log Status\n")
  print("1. Users Information\n")
  print("2. Login,Logout,Boot,Shutdown History\n")
  print("3. Recent Success Login History\n")
  print("4. Failed Login History\n)"
  print("Choose the number\n")
  
  value=input()
  
  def choose(self):
    if self.value=='1':
      result = os.popen('w').read()
      print(result)
      
     elif self.value=='2':
      result = os.popen('last').read()
      print(result)
      
     elif self.value=='3':
      result = os.popen('lastlog').read()
      print(result)
      
     elif self.value=='4':
      result = os.popen('lastb').read()
      print(result)
  
  t=logHis()
  t.choose()

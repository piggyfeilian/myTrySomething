#!/usr/bin/env python
# -*-coding: UTF-8 -*-
#for testing ai_debugger using data in Ui_2DReplay/testdata.py

import socket,sio,time
from testdata_debugger import *
serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#try:
serv.bind((sio.HOST,sio.UI_PORT))
#except:
 #   print 'port occupied, the program will exit...'
  #  time.sleep(3)
  #  exit(1)

serv.listen(1)
connUI, address = serv.accept()
(gameMode,gameMapPath,gameAIPath)=sio._recvs(connUI)
print gameMode,gameMapPath,gameAIPath
aiInfo = []

sio._sends(connUI, (maps,units0,aiInfo))
#Round 1
sio._sends(connUI, begInfo0)
#time.sleep(3)
sio._sends(connUI, (cmd0, endInfo0))
print "re1 send"
#time.sleep(8)

#Round 2
sio._sends(connUI, begInfo1)
#time.sleep(3)
sio._sends(connUI, (cmd1, endInfo1))

print "re2 send"
#time.sleep(10)

#Round 3
sio._sends(connUI, begInfo2)
#time.sleep(3)
#cmd0 = Command(0,(0,0))
sio._sends(connUI, (cmd2, endInfo2))
print "re3 send"
#time.sleep(10)
winner = "side1"
sio._sends(connUI,winner)
connUI.close()
serv.close()

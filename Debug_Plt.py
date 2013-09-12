#!/usr/bin/env python
# -*-coding: UTF-8 -*-
#for testing ai_debugger using data in Ui_2DReplay/testdata.py

import socket,sio,time
from testdata import *
serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serv2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
serv.bind((sio.HOST,sio.UI_PORT))
serv2.bind((sio.HOST,sio.AI_PORT))
#except:
 #   print 'port occupied, the program will exit...'
  #  time.sleep(3)
  #  exit(1)

serv.listen(1)
serv2.listen(1)

connUI, address = serv.accept()
print "abc"
connAI, address2 = serv2.accept()
print "daf"

print "9"
gameMode,gameMapPath,gameAIPath=sio._recvs(connUI)
print "10"
print gameMode,gameMapPath,gameAIPath

sio._sends(connAI, maps)
print "11"
info = sio._recvs(connAI)
print "12"
aiInfo = info[0]
print info
sio._sends(connUI, (maps,aiInfo, units0))
print "send init info"
#Round 1
sio._sends(connUI, begInfo0)
print "sent first"
sio._sends(connAI, begInfo0)
print "sent Ai first"
cmd0_ = sio._recvs(connAI)
print "movepos",cmd0_.move
print "recv command"
sio._sends(connUI, (cmd0, endInfo0))
print "re1 send"
time.sleep(3)
#Round 2
sio._sends(connUI, begInfo1)
#time.sleep(3)
sio._sends(connUI, (cmd2_, endInfo2_))
print "re2 send"
#time.sleep(10)
#Round 3
sio._sends(connUI, begInfo2)
sio._sends(connAI, begInfo2)
print "sent ai second"
cmd1 = sio._recvs(connAI)
print cmd1.move
print "rev command"
#time.sleep(3)
endInfo = endInfo1
endInfo.over = 0
sio._sends(connUI, (cmd1,endInfo))
print "re3 send"
#time.sleep(10)
winner = "side1"
sio._sends(connUI,winner)
connUI.close()
serv.close()

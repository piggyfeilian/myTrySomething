# -*- coding:UTF-8 -*-


#test data
from basic import *
import copy
m = Map_Basic
u = Base_Unit
maps = [[m(0),m(1),m(0),m(0),m(1), m(0)],
        [m(1),m(0),m(1),m(1), m(0), m(1)],
        [m(2), m(0),m(1),m(1),m(0), m(2)],
        [m(0), m(1), m(2),m(2),m(1),m(0)],
        [m(0), m(2),m(1),m(1),m(2),m(0)]]
#初始位置(0,0),(1,0),(1,1)
#        (5,4), (4,4), (3,3)
units0 = [[u(1,(0,0)),u(2,(1,0)),u(3,(1,1))],
          [u(1,(5,4)),u(2,(4,4)),u(3,(3,3))]]
iniInfo = Begin_Info(maps, units0)

begInfo0 = Round_Begin_Info((0,0),[], units0,[])
cmd0 = Command(0, (1,3))
units1 = [[u(1,(1,3)),u(2,(1,0)),u(3,(1,1))],
          [u(1,(5,4)),u(2,(4,4)),u(3,(3,3))]]
endInfo0 = Round_End_Info(units1, [], [], (-1, -1), (0,0), -1)

begInfo1 = Round_Begin_Info((1,2), [], units1,[])
cmd1 = Command(1, (2,3),(0,0))
units2=[[u(1,(1,3)),u(2,(1,0)),u(3,(1,1))],
          [u(1,(5,4)),u(2,(4,4)),u(3,(2,3))]]
endInfo1 = Round_End_Info(units2, [],[],(1,1), (2,0), -1)

begInfo2 = Round_Begin_Info((0,0),[],units2,[])
cmd2 = Command(1, (1,3), (1,2))
units3 = [[u(1,(1,3)),u(2,(1,0)),u(3,(1,1))],
          [u(1,(5,4)),u(2,(4,4)),u(3,(2,3))]]
units3[1][2].life = 0

endInfo2 = Round_End_Info(units3, [], [], (1,-1),(2,3), 1)

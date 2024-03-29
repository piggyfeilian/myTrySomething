#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from basic import *
import main
m = Map_Basic
u = Base_Unit

#maps = [[m(0), m(0), m(1), m(1)],
#        [m(1), m(1), m(0), m(1)],
#        [m(1), m(0), m(1), m(0)],
#        [m(0), m(0), m(1), m(1)]]
maps = [[m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)]]
units0 = [[u(1, (0, 0)), u(2, (1, 0)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
iniInfo = Begin_Info(maps, units0)


#初始位置:(0, 0) (0, 1) (0, 2)
#        (3, 3) (3, 2) (3, 1)

units1 = [[u(1, (3, 0)), u(2, (0, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
begInfo0 = Round_Begin_Info((0, 0), [], units0, [])
cmd0 = Command(1, (3,0),(1,2))
#move_range = main.available_spots(maps, units1,begInfo0.id)
#endInfo0 = main.calculation(cmd0, units0, maps,move_range,[],(0,0) ,begInfo0.id)
endInfo0 = Round_End_Info(units1, [], [],(1,1), (0,0),-1)
print endInfo0
begInfo1 = Round_Begin_Info((0,0), [], units1, [])
#第零回合：
#id 0 : (0, 0)->(1, 1) standby

units2_ = [[u(1,(1,1)), u(2, (1, 0)), u(3, (0,2))],
           [u(3, (3,3)), u(2,(3,2)), u(1, (3,1))]]
begInfo2_ = Round_Begin_Info((0,0),[],units1,[])
cmd2_ = Command(0,(1,1))
endInfo2_ = Round_End_Info(units2_, [], [],(-1,-1), (0,0),-1)

target = u(2, (3, 2))
target.life = 0
units2 = [[u(1, (1, 1)), u(2, (2, 1)), u(3, (0, 2))],
          [u(3, (3, 3)), target , u(1, (3, 1))]]
begInfo2 = Round_Begin_Info((0, 1), [], units2_, [])
cmd1 = Command(1, (2, 1),(1,1))
endInfo1 = Round_End_Info(units2, [], [],(1, -1), (0, 0), 1)

#第一回合：
#id 1 : (0, 1)->(2, 1) standby

units3 = [u(1, (1, 1)), u(2, (0, 1)), u(3, (0, 2)),
        u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]

if __name__ == "__main__":

    maps = [[m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)],
        [m(0), m(0), m(1), m(1), m(1), m(1), m(1), m(0)]]
    units0 = [[u(1, (0, 0)), u(2, (1, 0)), u(3, (0, 2))],
          [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
#初始位置:(0, 0) (1, 0) (0, 2)
#        (3, 3) (3, 2) (3, 1)

    units1 = [[u(1, (3, 0)), u(2, (1, 0)), u(3, (0, 2))],
              [u(3, (3, 3)), u(2, (3, 2)), u(1, (3, 1))]]
    begInfo0 = Round_Begin_Info((0, 0), [], units0, [])
    cmd0 = Command(1, (3,0),(1,2))
    endInfo0 = main.calculation(cmd0, units0, maps,move_range,[],(0,0) ,begInfo0.id)
    print endInfo0.route

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#回放GraphicsView定义



from myHumanReplay import *
import sys,copy
from myGetRoute import *
class REPLAYERROR(Exception):
    def __init__(self, value = ""):
        self.value = value

    def __str__(self):
        return self.value
MCE_Type = QEvent.registerEventType()
#KCE_Type = QEvent.registerEventType()

class CommEvent(QEvent):
    def __init__(self, value):
        super(CommEvent, self).__init__(MCE_Type)
        self.value = value
#class KeyCommEvent(QEvent):
#    def __init(self, key):
#        super(KeyCommEvent, self).__init__(KCE_Type)

class CommTransition(QAbstractTransition):
    def __init__(self, value, source = None):
        super(CommTransition, self).__init__(source)
        self.value = value

    def eventTest(self, event):
        if not isinstance(event, CommEvent):
            return False
        if event.value == self.value:
            return True
        return  False

    def onTransition(self,event):
        pass
class HumanReplay(QGraphicsView):
#    commBeg = pyqtSignal()
#    moveFinished = pyqtSignal()
#    lastAgain = pyqtSignal()
#    oprFinished = pyqtSignal()
    endGame = pyqtSignal()
#    commandFinished = pyqtSignal()
    def __init__(self, scene, parent = None):
        super(HumanReplay, self).__init__(parent)

        self.scene = scene
        self.setScene(self.scene)
        #游戏记录变量
        self.iniMapInfo = None
        self.latestStatus = 1
        self.latestRound = 0
        self.nowMoveUnit = None
        self.now_state = None
        #命令变量
        self.command = None
        self.moveToPos = None
        self.Operation = None
        #临时命令展示信息
        self.route_ind_list = []
        self.move_range_list = []
        self.attack_range_list = []

        #储存展示信息
        self.UnitBase = [[],[]]
        self.MapList=[]
        self.mapChangeInfo = []

        #储存游戏信息
        self.command_list = []
        self.gameBegInfo = []
        self.gameEndInfo = []
        #鼠标选定单位
        self.focusUnit = MouseFocusUnit(0, 0)
        self.focusUnit.setVisible(False)

        self.mouseUnit = MouseIndUnit(0, 0)
        self.mouseUnit.setVisible(False)

        self.setCursor(QCursor(QPixmap(":normal_cursor.png"),0,0))
        #状态机定义与连接
        self.stateMachine = QStateMachine(self)
        self.State_Run = QState(self.stateMachine)
        self.State_No_Comm = QState(self.State_Run)
        self.State_Comm = QState(self.State_Run)
        self.State_Move = QState(self.State_Comm)
        self.State_Opr = QState(self.State_Comm)
        self.State_Target = QState(self.State_Comm)
        self.stateMachine.setInitialState(self.State_Run)
        self.State_Run.setInitialState(self.State_No_Comm)
        self.State_Comm.setInitialState(self.State_Move)
        self.State_Final = QFinalState(self.stateMachine)

        self.stateList = [self.State_No_Comm, self.State_Move, self.State_Opr, self.State_Target]
        transition = CommTransition("commBeg")
        transition.setTargetState(self.State_Move)
        self.State_No_Comm.addTransition(transition)
        transition = CommTransition("moveFinished")
        transition.setTargetState(self.State_Opr)
        self.State_Move.addTransition(transition)
        transition = CommTransition("lastAgain")
        transition.setTargetState(self.State_Move)
        self.State_Opr.addTransition(transition)
        transition.setTargetState(self.State_Opr)
        self.State_Target.addTransition(transition)
        transition = CommTransition("oprFinished")
        transition.setTargetState(self.State_Target)
        self.State_Opr.addTransition(transition)
        transition = CommTransition("commandFinished")
        transition.setTargetState(self.State_No_Comm)
        self.State_Comm.addTransition(transition)
        self.State_Run.addTransition(self, SIGNAL("endGame()"), self.State_Final)

        for state in self.stateList:
            self.connect(state, SIGNAL("entered()"), self.on_Entered)
        self.connect(self.State_Target, SIGNAL("exited()"), self.on_Exited)
        self.stateMachine.start()
    #begin to get command
    def GetCommand(self):
        self.stateMachine.postEvent(CommEvent("commBeg"))
        print "emit"
        print self.gameBegInfo
        print "id",self.gameBegInfo[self.latestRound].id
        self.nowMoveUnit = self.UnitBase[self.gameBegInfo[-1].id[0]][self.gameBegInfo[-1].id[1]]
    #event handlers
    def mouseMoveEvent(self, event):
        pos = event.pos()
        if not self.mouseUnit.isVisible():
            self.mouseUnit.setVisible(True)
        item = self.itemAt(pos)
        if self.mouseUnit.corX == item.corX and self.mouseUnit.corY == item.corY:
            return
        self.mouseUnit.setPos(item.corX, item.corY)

    def mousePressEvent(self, event):
        pos = event.pos()
        if not self.focusUnit.isVisible():
            self.focusUnit.setVisible(True)
        item = self.itemAt(pos)
        #还没有做发出展示信号的部分
        if item == self.focusUnit:
            return
        if not self.now_state == self.State_Move:
            self.focusUnit.setPos(item.corX, item.corY)
        if self.now_state == self.State_No_Comm or self.now_state == self.State_Opr:
            return
        if self.now_state == self.State_Move:

            if (item.corX, item.corY) not in self.move_range_list:
                return
            self.moveToPos = (item.corX, item.corY)
            self.stateMachine.postEvent(CommEvent("moveFinished"))
            return
        if self.now_state == self.State_Target:
            if (item.corX, item.corY) not in self.attack_range_list:
                return
            for item in self.items(pos):
                if isinstance(item, SoldierUnit):
                    self.command = basic.Command(self.Opr, self.moveToPos, item.obj.id)
                    self.emit(SIGNAL("commandFinished"), self.command)
                    self.stateMachine.postEvent(CommEvent("commandFinished"))
                    self.command_list.append(self.command)

    def keyPressEvent(self, event):
        if event.key == Qt.Key_Escape:
            if self.now_state == self.State_Opr or self.State_Target:
                self.stateMachine.postEvent(CommEvent("lastAgain"))
        if self.now_state != self.State_Opr:
            return
        if event.key == Qt.Key_A:
            self.Operation = 1
            self.stateMachine.postEvent(CommEvent("oprFinished"))
        elif event.key == Qt.Key_S:
            self.Operation = 2
            self.stateMachine.postEvent(CommEvent("oprFinished"))
        elif event.key == Qt.Key_D:
            self.command = basic.Command(0, self.moveToPos, None)
            self.command_list.append(self.command)
            self.emit(SIGNAL("commandFinished"), self.command)
            self.stateMachine.postEvent(CommEvent("commandFinished"))
    #展示便于用户下达命令的信息
    def on_Entered(self):
        now_state = self.sender()
        print now_state
        if not isinstance(now_state, QState):
            return
        self.now_state = now_state
        self.resetToPlay()
        if now_state == self.State_No_Comm:
            print "nocomm"
            self.Operation = self.moveToPoint = self.command = None
        elif now_state == self.State_Move:
            print "move state"
            if isinstance(self.nowMoveUnit, SoldierUnit):
                self.focusUnit.setPos(self.nowMoveUnit.corX, self.nowMoveUnit.corY)
                self.move_range_list = getMoveArrange(self.getMap(self.latestRound,0), self.gameBegInfo[-1].base, self.gameBegInfo[-1].id)
                self.drawArrange(self.move_range_list)
        elif now_state == self.State_Opr:
            if isintance(self.nowMoveUnit, SoildierUnit):
                self.route_ind_list = GetRoute(self.getMap(self.latestRound, 0), self.gameBegInfo[-1].base, self.gameBegInfo[-1].id,self.moveToPos)
                self.drawRoute(self.route_ind_list)
        elif now_state == self.State_Target:
            if self.Operation == 1:
                self.setCursor(QCursor(QPixmap(":attack_cursor.png"),0,0))
                self.attack_range_list = getAttackRange(self.getMap(self.latestRound, 0), self.gameBegInfo[-1].base, self.gameBegInfo[-1].id, self.moveToPos)
                self.drawArrange(self.attack_range_list)
            elif self.Operation == 2:
                self.setCursor(QCursor(QPixmap(":skill_cursor.png"),0,0))
                #not completed
#                self.
#            elif self.Operation == "N":
#                self.emit("commandComplete")

    def on_Exited(self):
        self.setCursor(QCursor(QPixmap(":normal_cursor.png"),0,0))
    def drawArrange(self, arrange_list):
        for pos in arrange_list:
            ind_unit = ArrangeIndUnit(pos[0], pos[1])
            self.scene.addItem(ind_unit)
            ind_unit.setPos(pos[0],pos[1])
    #得到指定回合的地图,通过每回合mapchange计算
    def getMap(self, round_, status):
        map_ = copy.copy(self.iniMapInfo)
        for i in range(round_):
            if mapChangeInfo[i]:
                for change in mapChangeInfo[i]:
                    map_[change[1][1]][change[1][0]] = basic.Map_Basic(change[0])
        if status:
            change = mapChangeInfo[round_]
            map_[change[1][1]][change[1][0]] = basic.Map_Basic(change[0])
        return map_
    def setMap(self, map_):
        self.resetMap()
        self.width = len(map_[0])
        self.height = len(map_)
        for i in range(self.height):
            for j in range(self.width):
                new_map = MapUnit(j,i,map_[i][j])
                self.scene.addItem(new_map)
                new_map.setPos(j,i)
                self.MapList.append(new_map)

    def setSoldier(self, units):
        self.resetUnit()
        for i in range(2):
            for j in range(len(units[i])):
                new_unit = SoldierUnit(units[i][j])
                self.scene.addItem(new_unit)
                new_unit.setPos(new_unit.corX, new_unit.corY)
                self.UnitBase[i].append(new_unit)
        print "base",len(self.UnitBase[0])
    def Initialize(self,begInfo,frInfo):
        self.setMap(begInfo.map)
        self.iniMapInfo = begInfo.map
        self.setSoldier(begInfo.base)
        self.latestStatus = 0
        self.gameBegInfo.append(frInfo)
#        self.stateMachine.start()

    def UpdateBeginInfo(self, rbInfo):
        self.gameBegInfo.append(rbInfo)
        self.latestStatus = 0
        self.latestRound += 1

    def UpdateEndInfo(self, comInfo, reInfo):
        self.gameEndInfo.append((comInfo, reInfo))
        self.latestStatus = 1
        self.mapChangeInfo.append(reInfo.change)
#        if reInfo.change:
#            map_item = self.scene.items(GetPos(change[1][0], change[1][1]))[-1]
#            map_item.obj = Map_Basic(change[0])
#            map_item.update()
#            map_list
    #从当前回合开始播放至这一回合结束
    def Play(self):
        pass
    #展示round_, status的场面
    def GoToRound(self, round_, status):
#        if self.animation:
#            self.TerminateAni()
        if round_ * 2 + status > self.latestRound * 2 + self.latestStatus:
            raise REPLAYERROR("not update to that status")

        self.setMap(self.getMap(round_, status))
        if status:
            self.setSoldier(self.gameEndInfo[round_][1].base)
        else:
            self.setSoldier(self.gameBegInfo[round_].base)

    def resetMap(self):
        for item in self.MapList:
            self.scene.removeItem(item)

        self.MapList = []
    def resetUnit(self):
        for item in self.UnitBase[0]:
            self.scene.removeItem(item)
        for item in self.UnitBase[1]:
            self.scene.removeItem(item)
        self.UnitBase = [[],[]]

    #去掉临时方便用户命令的信息展示
    def resetToPlay(self):
        for item in self.move_range_list:
            self.scene.removeItem(item)
        self.move_range_list = []
        for item in self.attack_range_list:
            self.scene.removeItem(item)
        self.attack_range_list = []
        for item in self.route_ind_list:
            self.scene.removeItem(item)
        self.route_ind_list = []

    #供结束游戏时的完全清理,需要保存录像请在此之前提取游戏信息
    def reset(self):
        self.emit(SIGNAL("endGame()"))
        self.resetToPlay()
        self.route_ind_list = []
        self.move_range_list = []
        self.attack_range_list = []

        self.resetUnit()
        self.resetMap()
        self.mapChangeInfo = []

        self.command_list = []
        self.gameBegInfo = []
        self.gameEndInfo = []

        self.now_state = self.nowMoveUnit = self.command = self.moveToPos = self.Operation = self.iniMapInfo = None
        self.latestStatus = 1
        self.latestRound = 0

#test
if __name__ == "__main__":
    import time
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    form = HumanReplay(scene)
    form.show()
    m = basic.Map_Basic
    map_ = [[m(0), m(0), m(1), m(2), m(0), m(0)],
            [m(0), m(1), m(0), m(0), m(1), m(0)],
            [m(2), m(2), m(0), m(0), m(1), m(0)]]
    u = basic.Base_Unit
    units = [[u(0,(0,0)), u(1,(0,2))],
             [u(0,(3,1)), u(1,(2,0))]]
    form.Initialize(basic.Begin_Info(map_,units,((6,6),(6,6))),basic.Round_Begin_Info((0,1),0,units,0))
    time.sleep(1)
    app.exec_()
#   form.GetCom()
    

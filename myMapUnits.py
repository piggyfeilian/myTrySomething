#!/usr/bin/env python
# -*- coding:UTF-8 -*-
#地图编辑器回放界面,单位定义
#不用item.contains(QPointF)改用view.items(QPoint)来判断
#item的mouseMoveEvent没有用是为啥呢。。。
#解决了unititem放回原处删除的bug
#解决了mouse grabber没有切换回来的bug
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import basic
import qrc_resource
UNIT_WIDTH = 50
UNIT_HEIGHT = 50
EDGE_WIDTH = 4

FILE_UNIT = ["saber", "lancer", "archer", "dragon_rider", "warrior",
             "wizard", "hero_1", "hero_2", "hero_3"]
FILE_MAP = ["plain", "mountain", "forest", "barrier", "turret",
                     "trap", "temple", "gear"]

def GetPos(x, y):
    return QPointF(x * (UNIT_WIDTH + EDGE_WIDTH), y * (UNIT_HEIGHT + EDGE_WIDTH))


class AbstractUnit(QGraphicsObject):
    """界面上元素的基类"""
    def __init__(self, x, y, parent):
        super(AbstractUnit, self).__init__(parent)

        self.corX = x
        self.corY = y
    def boundingRect(self):
        return QRectF(0, 0, UNIT_WIDTH+EDGE_WIDTH,
                       UNIT_HEIGHT+EDGE_WIDTH)

    def getParent(self):
        return self.scene().views()[0]
class MapUnit(AbstractUnit):
    """地形元素类"""
    def __init__(self, x, y, map_, parent = None):
        super(MapUnit, self).__init__(x, y, parent)

        self.obj = map_
#QGraphicsItem reimplement paint() rather than paintEvent
    def paint(self, painter, option, widget = None):
#        painter = QPainter()

        filename = ":" + FILE_MAP[self.obj.kind] + ".png"
        image = QImage(filename)
        painter.drawImage(QPoint(EDGE_WIDTH/2, EDGE_WIDTH/2), image.scaled(UNIT_WIDTH, UNIT_HEIGHT,
                                                      Qt.IgnoreAspectRatio))
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(EDGE_WIDTH)
        painter.setPen(pen)
        painter.drawRect(0, 0, UNIT_WIDTH + EDGE_WIDTH, UNIT_HEIGHT + EDGE_WIDTH)

    def mousePressEvent(self, event):
        if event.button() != Qt.RightButton:
            event.ignore()
        else:
#            self.startPos = event.pos()
            event.accept()

#   def mouseMoveEvent(self, event):
#        if event.button() != Qt.RightButton:
#            event.ignore()
#            return
#        elif event.pos() - self.startPos.manhattanLength() < QApplication.startDragDistance():
#            event.ignore()
#            return
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream << QVariant(self.obj.kind)
            mimeData = QMimeData()
            mimeData.setData("application/map", data)
            drag = QDrag(self.getParent())
            drag.setMimeData(mimeData)
            print self.obj.kind
            drag.setPixmap(QPixmap(":%s.png" %FILE_MAP[self.obj.kind]).scaled(30,30))
            drag.setHotSpot(QPoint(15,15))
            if drag.start(Qt.MoveAction) == Qt.MoveAction:
                #让item失去mouse grabber
                self.setVisible(False)
                self.obj = basic.Map_Basic(0)
                self.setVisible(True)
                self.update()
#            drag.start(Qt.MoveAction)
#    def mouseRelease
class SoldierUnit(AbstractUnit):
    """单位基类"""
    def __init__(self, unit, parent = None):
        super(SoldierUnit, self).__init__(unit.position[0], unit.position[1], parent)

        self.obj = unit

        self.setZValue(0.5)
    def paint(self, painter, option, widget = None):
#        painter = QPainter()

        filename = ":" + FILE_UNIT[self.obj.kind] + ".png"
        image = QImage(filename)
        painter.setCompositionMode(QPainter.CompositionMode_Multiply)
        painter.drawImage(QPoint(EDGE_WIDTH/2, EDGE_WIDTH/2), image.scaled(UNIT_WIDTH, UNIT_HEIGHT,
                                                                           Qt.IgnoreAspectRatio))

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            event.ignore()
            return
        print self.obj.kind, "press"
#        self.startPos = event.pos()
        event.accept()

#    def mouseMoveEvent(self, event):
#        print "abc"
#        if event.button() != Qt.LeftButton:
#            event.ignore()
#            return
#        elif event.pos() - self.startPos.manhattanLength() < QApplication.startDragDistance():
#            event.ignore()
#            return
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
#        stream << self.obj
        stream << QVariant(self.obj.kind)
        mimeData = QMimeData()
        mimeData.setData("application/unit", data)
        drag = QDrag(self.getParent())
        drag.setMimeData(mimeData)
        drag.setPixmap(QPixmap(":%s.png" %FILE_UNIT[self.obj.kind]).scaled(30,30))
        drag.setHotSpot(QPoint(15,15))
        print drag
        if drag.start(Qt.MoveAction) == Qt.MoveAction:
            try:
                self.scene().removeItem(self)
            except:
                pass

class FocusUnit(AbstractUnit):
    """光标"""
    def __init__(self, x, y ,parent = None):
        super(FocusUnit, self).__init__(x, y, parent)

        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.timeOut)
        self.timer.start(600)


    def timeOut(self):
        self.setVisible(not self.isVisible())
    def hideEvent(self):
        self.setVisible(False)
        self.timer.stop()
    def showEvent(self):
        self.setVisible(True)
        self.timer.start()
    def paint(self, painter, option, widget = None):
        RLINE = 0.4 #rate of line
        pen = QPen()
        pen.setWidth(EDGE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setColor(QColor(Qt.blue).lighter())
        painter.setPen(pen)

        painter.drawLine(QPointF(0, 0),
                         QPointF(0, RLINE*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(0, 0),
                         QPointF(RLINE*(UNIT_WIDTH + EDGE_WIDTH), 0))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, 0),
                         QPointF(UNIT_WIDTH + EDGE_WIDTH, RLINE*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, 0),
                         QPointF((1-RLINE)*(UNIT_WIDTH + EDGE_WIDTH), 0))
        painter.drawLine(QPointF(0, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF(0, (1-RLINE)*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(0, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF(RLINE*(UNIT_WIDTH + EDGE_WIDTH), (UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF(UNIT_WIDTH + EDGE_WIDTH, (1-RLINE)*(UNIT_HEIGHT + EDGE_WIDTH)))
        painter.drawLine(QPointF(UNIT_WIDTH + EDGE_WIDTH, (UNIT_HEIGHT + EDGE_WIDTH)),
                         QPointF((1-RLINE)*(UNIT_WIDTH + EDGE_WIDTH), (UNIT_HEIGHT + EDGE_WIDTH)))

class MapView(QGraphicsView):
    def __init__(self, parent = None):
        super(MapView, self).__init__(parent)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setAcceptDrops(True)

        self.map_list = []
        self.unit_list = []
        self.width = 0
        self.height = 0

        self.focusGrid = FocusUnit(0, 0)
        self.focusMapUnit = None
        self.scene.addItem(self.focusGrid)
        self.focusGrid.setPos(GetPos(self.focusGrid.corX, self.focusGrid.corY))
        self.focusGrid.hide()

    def setMap(self, map_):
        self.resetAll()
        self.width = len(map_[0])
        self.height = len(map_)
        for i in range(self.height):
            for j in range(self.width):
                new_map = MapUnit(j, i, map_[i][j])
                self.scene.addItem(new_map)
                new_map.setPos(GetPos(j, i))
                self.map_list.append((j, i, new_map))


    def setUnits(self, units):
        for i in range(2):
            for j in range(len(units[i])):
                new_unit = SoldierUnit(units[i][j])
                self.scene.addItem(new_unit)
                new_unit.setPos(GetPos(new_unit.corX, new_unit.corY))

                self.unit_list.append((new_unit.corX, new_unit.corY, i, new_unit))



    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/unit") or \
                event.mimeData().hasFormat("application/map"):
            event.accept()
            self.focusGrid.hide()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/unit") or \
                event.mimeData().hasFormat("application/map"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for map1 in self.map_list:
            print map1[2].obj.kind
        if event.mimeData().hasFormat("application/unit") or \
                event.mimeData().hasFormat("application/map"):
            print "ready drop"
#            dropPoint = self.mapToScene(event.pos())
            dropPoint = event.pos()
            print dropPoint
            targetItem = None
#            for i in range(len(self.map_list)):
#                print "judge"
#                if self.map_list[i][2].contains(dropPoint):
#                    print "true"
#                    targetItem = self.map_list[i]
#                    break
            #获取地图元素targetItem
            try:
                targetItem = self.items(dropPoint)[len(self.items(dropPoint)) - 1]
            except:
                return
            if not targetItem or not isinstance(targetItem, MapUnit):
#                event.setDropAction(Qt.CopyAction)
                event.accept()
                return
            if event.mimeData().hasFormat("application/unit"):
                data = event.mimeData().data("application/unit")
#                unit = Base_Unit(0)
                unit = QVariant()
                side = QVariant()
                stream = QDataStream(data, QIODevice.ReadOnly)
                stream >> unit >> side
                new_unit = SoldierUnit(basic.Base_Unit(unit.toInt()[0],(targetItem.corX, targetItem.corY)))
                side = side.toInt()[0]

                items = self.items(dropPoint)

                #删除该点原有单位
                for item in items:
                    if isinstance(item, SoldierUnit):
                        for i in range(len(self.unit_list)):
                            if item is self.unit_list[i][3]:
                                self.unit_list[i][3].scene().removeItem(self.unit_list[i][3])
                                self.unit_list.pop(i)
                                break
                    break
                self.scene.addItem(new_unit)
                #记得要setPos
                new_unit.setPos(GetPos(new_unit.corX, new_unit.corY))
                print new_unit.corX,new_unit.corY
                self.unit_list.append((new_unit.corX, new_unit.corY, side, new_unit))

            elif event.mimeData().hasFormat("application/map"):
                data = event.mimeData().data("application/map")
#                map_ = Map_Basic(0)
                map_ = QVariant()

                stream = QDataStream(data, QIODevice.ReadOnly)
                stream >> map_
                print "maptype",map_.toInt()[0]
                targetItem.obj = basic.Map_Basic(map_.toInt()[0])
                targetItem.update()

            event.setDropAction(Qt.MoveAction)
            event.accept()
            self.emit(SIGNAL("dropRec()"))
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self.focusMapUnit:
            #contains到底可以用吗?
            if self.focusMapUnit.contains(event.pos()):
                pass
            else:
                self.focusMapUnit = self.items(event.pos())[len(self.items(event.pos()))-1]
                self.focusGrid.setPos(self.focusMapUnit.pos())

    def resetAll(self):
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.unit_list = []
        self.map_list = []
        self.width = 0
        self.height = 0

    def initEmpty(self, x, y):
        if self.map_list or self.unit_list:
            return
        self.width = x
        self.height = y
        for i in range(x):
            for j in range(y):
                map_ = MapUnit(i, j, basic.Map_Basic(0))
                self.scene.addItem(map_)
                map_.setPos(GetPos(i,j))
                self.map_list.append((i, j, map_))

    def changeWidth(self, new_width):

        if new_width < self.width:
            list_to_rm = []
            for i in range(len(self.map_list)):
                if self.map_list[i][0] >= new_width:
                    self.scene.removeItem(self.map_list[i][2])
                    list_to_rm.append(self.map_list[i])
            for item in list_to_rm:
                self.map_list.remove(item)
            list_to_rm = []
            for i in range(len(self.unit_list)):
                if self.unit_list[i][0] >= new_width:
                    self.scene.removeItem(self.unit_list[i][3])
                    list_to_rm.append(self.unit_list[i])
            for item in list_to_rm:
                self.unit_list.remove(item)
        else:
            for i in range(self.height):
                for j in range(new_width - self.width):
                    new_map = MapUnit(j+self.width,i,basic.Map_Basic(0))
                    self.map_list.append((j + self.width, i, new_map))
                    self.scene.addItem(new_map)
                    new_map.setPos(GetPos(j + self.width, i))

        self.width = new_width

    def changeHeight(self, new_height):
        if new_height < self.height:
            list_to_rm = []
            for i in range(len(self.map_list)):
                if self.map_list[i][1] >= new_height:
                    self.scene.removeItem(self.map_list[i][2])
                    list_to_rm.append(self.map_list[i])
            for item in list_to_rm:
                self.map_list.remove(item)

            list_to_rm = []
            for i in range(len(self.unit_list)):
                if self.unit_list[i][1] >= new_height:
                    self.scene.removeItem(self.unit_list[i][3])
                    list_to_rm.append(self.map_list[i])
            for item in list_to_rm:
                self.unit_list.remove(item)
        else:
            for i in range(self.width):
                for j in range(new_height - self.height):
                    new_map = MapUnit(i,j+self.height,basic.Map_Basic(0))
                    self.map_list.append((i, j + self.height, new_map))
                    self.scene.addItem(new_map)
                    new_map.setPos(GetPos(i, j + self.height))
        self.height = new_height

#改变地图元素时同步map_list记录,unit_list同步已嵌入dropEvent
#    def updateMapItem(self, targetItem):
#        for i in range(len(self.map_list)):
#            if self.map_list[i][0] == targetItem.corX and self.map_list[i][1] == targetItem.corY:
#                self.map_list[i] = (targetItem.corX, targetItem.corY, targetItem)

#for test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = basic.Map_Basic
    map_ = [[m(0), m(0), m(1), m(2), m(0), m(0)],
            [m(0), m(1), m(0), m(0), m(1), m(0)],
            [m(2), m(2), m(0), m(0), m(1), m(0)]]
    u = basic.Base_Unit
    units = [[u(0,(0,0)), u(1,(0,2))],
             [u(0,(3,1)), u(1,(2,0))]]
    view = MapView()
    view.setMap(map_)
    view.setUnits(units)
#    app.setStartDragDistance(1)
    view.show()
    app.exec_()



#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#地图编辑器主界面

from myMapUnits import *
import sys
import ui_mapWindow

SIDE = 0#default side
MAP_DIR = "."#地图文件默认路径

class MainForm(ui_mapWindow.Ui_MapWindow, QWidget):
    def __init__(self, parent = None):
        super(MainForm, self).__init__(parent)

        self.dirty = False
        self.fileName = ""
        self.setupUi()
        self.mapEditWidget = MapView()
        self.widget_layout.addWidget(self.mapEditWidget)

        self.mapList = DrListWidget("map")
        self.unitList = DrListWidget("unit")
        for unit in FILE_UNIT:
            item = QListWidgetItem(unit)
            item.setIcon(QIcon(":"+unit+".png"))
            self.unitList.addItem(item)
        for _map in FILE_MAP:
            item = QListWidgetItem(_map)
            item.setIcon(QIcon(":"+_map+".png"))
            self.mapList.addItem(item)
        self.connect(self.mapEditWidget, SIGNAL("dropRec()"), self.setDirty)

    @pyqtSlot()
    def on_openButton_clicked(self):
        if not self.dirty or self.okToContinue():
            filename = QFileDialog.getOpenFileName(self, QString.fromUtf8("打开地图文件"), MAP_DIR,
                                                   "mapfiles (*.map)")
            if filename:
                try:
                    self.parseFromFile(filename)
                except (IOError), e:
                    QMessageBox.critical(self, QString.fromUtf8("打开文件失败"), QString.fromUtf8("错误：%s" %e),
                                         QMessageBox.Ok, QMessageBox.NoButton)
                else:
                    self.dirty = False

    @pyqtSlot()
    def on_newButton_clicked(self):
        if not self.dirty or self.okToContinue():
            self.resetAll()
            self.dirty = False
            self.fileName = ""

    @pyqtSlot()
    def on_resetButton_clicked(self):
        self.resetAll()

    def resetAll(self):
        if len(self.mapEditWidget.scene.items()) == 0:
class DrListWidget(QListWidget):
    def __init__(self, type_, parent = None):
        super(DrListWidget, self).__init__(parent)

        self.setDragEnabled(True)
        self.type = type_

    def startDrag(self, dropAction):
        item = self.currentItem()
        icon = item.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        if self.type == "map":
            stream << FILE_MAP.index(item.text())
        else:
            global SIDE
            stream << FILE_UNIT.index(item.text()) << SIDE
        mimeData = QMimeData()
        mimeData.setData("application/%s" %self.type, data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(30, 30)
        drag.setHotSpot(QPoint(15, 15))
        drag.setPixmap(pixmap)
        drag.start(Qt.CopyAction)
  

        

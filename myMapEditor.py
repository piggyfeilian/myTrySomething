#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#地图编辑器主界面

from myMapUnits import *
import sys,os
import ui_mapWindow
MAGIC_NUMBER = 111
FILE_VERSION = 1
SIDE = 0#default side
MAP_DIR = "."#地图文件默认路径

class MapError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

     
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
            stream << QVariant(FILE_MAP.index(item.text()))
        else:
            global SIDE
            stream << QVariant(FILE_UNIT.index(item.text()))
            stream << QVariant(SIDE)
        mimeData = QMimeData()
        mimeData.setData("application/%s" %self.type, data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(30, 30)
        drag.setHotSpot(QPoint(15, 15))
        drag.setPixmap(pixmap)
        drag.start(Qt.CopyAction)
  

class MainForm(ui_mapWindow.Ui_MapWindow, QWidget):
#     class CValidator(QValidator):
#          def __init__(self, parent = None):
#               super(CValidator, self).__init__(parent)
#          def validate(
     def __init__(self, parent = None):
          super(MainForm, self).__init__(parent)

          self.width = 8
          self.height = 8

          self.dirty = False
          self.filename = ""
          self.setupUi(self)
          self.side1.setChecked(True)
          self.mapEditWidget = MapView()
          self.widget_layout.addWidget(self.mapEditWidget)
          self.vali = QIntValidator(2, 20, self)
          self.widthEdit.setValidator(self.vali)
          self.heightEdit.setValidator(self.vali)
          self.mapListWidget = DrListWidget("map")
          self.unitListWidget = DrListWidget("unit")
          for unit in FILE_UNIT:
               item = QListWidgetItem(unit)
               item.setIcon(QIcon(":"+unit+".png"))
               self.unitListWidget.addItem(item)
          for _map in FILE_MAP:
               item = QListWidgetItem(_map)
               item.setIcon(QIcon(":"+_map+".png"))
               self.mapListWidget.addItem(item)
          self.listLayout.addWidget(self.mapListWidget)
          self.listLayout.addWidget(self.unitListWidget)
          self.connect(self.mapEditWidget, SIGNAL("dropRec()"), self.setDirty)
          self.connect(self.widthEdit, SIGNAL("editingFinished()"),self.widthEdit_editingFinished, Qt.QueuedConnection)
          self.connect(self.heightEdit, SIGNAL("editingFinished()"),self.heightEdit_editingFinished, Qt.QueuedConnection)

          self.setWindowTitle('""--MapEditor.exe')

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
                         self.filename = filename
                         self.updateUi()


     @pyqtSlot()
     def on_saveButton_clicked(self):
          if not self.dirty:
               return
          if not self.filename:
               self.on_saveAsButton_clicked()
          else:
               try:
                    self.writeToFile(self.filename)
               except (IOError), e:
                    QMessageBox.critical(self, QString.fromUtf8("错误"),
                                         QString.fromUtf8("存储文件过程中发生错误%s"%e),
                                         QMessageBox.Ok, QMessageBox.NoButton)

               else:
                    self.dirty = False
                    self.updateUi()

     @pyqtSlot()
     def on_saveAsButton_clicked(self):
          filename = QFileDialog.getSaveFileName(self, QString.fromUtf8("另存为"),
                                                 MAP_DIR, "mapfiles (*.map)")
          if filename:
               #            if os.path.isfile(filename):
#                answer = QMessageBox.question(self, QString.fromUtf8("另存为"),
#                                              QString.fromUtf8("已有同名文件存在，是否继续覆盖同名文件?"),
#                                              QMessageBox.Yes, QMessageBox.No)
#                if answer == QMessageBox.No:
#                    return
               try:
                    self.writeToFile(filename)
               except (IOError), e:
                    QMessageBox.critical(self, QString.fromUtf8("错误"),
                                         QString.fromUtf8("存储文件过程中发生错误%s"%e),
                                         QMessageBox.Ok, QMessageBox.NoButton)
               else:
                    self.dirty = False
                    if not self.filename:
                         self.filename = filename
                         self.updateUi()

     @pyqtSlot()
     def on_newButton_clicked(self):
          if not self.dirty or self.okToContinue():
            self.resetAll()
            self.mapEditWidget.initEmpty(self.width, self.height)
            self.dirty = False
            self.fileName = ""
            self.updateUi()

     @pyqtSlot()
     def on_returnButton_clicked(self):
        if not self.dirty or self.okToContinue():
            self.resetAll()
            self.dirty = False
            self.fileName = ""
            self.updateUi()

     @pyqtSlot()
     def on_resetButton_clicked(self):
        self.resetAll()
        self.mapEditWidget.initEmpty(self.width, self.height)

     @pyqtSlot()
     def on_side1_toggled(self, on):
        if on:
            global SIDE
            SIDE = 0
     @pyqtSlot()
     def on_side2_toggled(self, on):
        if on:
            global SIDE
            SIDE = 1

     def widthEdit_editingFinished(self):
         text =  self.widthEdit.text()
         print "abc"
         text = text.toInt()[0]
         print text
         if text == self.width:
              return
         if not text:
              self.widthEdit.setText("%d"%self.width)
              return
         if text > 20 or text < 2:
              self.widthEdit.setText("%d"%self.width)
              return
         print "here"
         self.changeWidth(text)

     def heightEdit_editingFinished(self):
         text = self.heightEdit.text()
         text = text.toInt()[0]
         if text == self.height:
              return
         if not text:
              self.heightEdit.setText("%d"%self.height)
              return
         if text > 20 or text < 2:
              self.heightEdit.setText("%d"%self.height)
              return
         self.changeHeight(text)

     def updateUi(self):
        fn = self.filename.split("/")[-1] if self.filename else ""
        string = '"' + fn + '"--MapEditor.exe'
        if self.dirty:
            string = "**" + string
        self.setWindowTitle(string)

     def okToContinue(self):
        if self.dirty:
            answer = QMessageBox.question(self, QString.fromUtf8("放弃进度"),
                                          QString.fromUtf8("你有未保存的工作，确定不保存继续吗?"),
                                          QMessageBox.Yes, QMessageBox.No)
            if answer == QMessageBox.No:
                return False
        return True

     def setDirty(self):
        self.dirty = True
        self.updateUi()

     def resetAll(self):
        self.mapEditWidget.resetAll()
        self.dirty = True
        self.updateUi()

     def writeToFile(self, fname):
        error = None
        fh = None
        try:
            fh = QFile(fname)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt32(FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_2)
    
            mlt = self.mapEditWidget.map_list
            rows = self.mapEditWidget.height
            cols = self.mapEditWidget.width
            stream.writeInt16(rows)
            stream.writeInt16(cols)
            i = 0
            while i < rows:
                j = 0
                while j < cols:
                    for m in mlt:
                        if (m[0],m[1]) == (j,i):
                            stream.writeInt16(m[2].obj.kind)
                            break
                    else:
                        stream.writeInt16(0)
                        error=MAPError(QString.fromUtf8("地图元素缺少%d行,%d列,用默认地图元素代替"%(i,j)))
                    j += 1
                i += 1
            ult = self.mapEditWidget.unit_list
            stream.writeInt16(len(ult))
            for u in ult:
                stream.writeInt16(u[2])
                stream.writeInt16(u[3].obj.kind)
                stream.writeInt16(u[3].obj.position[0])
                stream.writeInt16(u[3].obj.position[1])
        except IOError,e :
            raise IOError,e
        finally:
            if fh:
                fh.close()
            if error:
                QMessageBox.warning(self, QString.fromUtf8("数据有误"),
                                    error.value,QMessageBox.Ok,QMessageBox.NoButton)

     def parseFromFile(self, fname):
        error = None
        fh = None
        try:
            fh = QFile(fname)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            magic = stream.readInt32()
            print "magic",magic
            if magic != MAGIC_NUMBER:
                raise IOError, "unrecognized file type"
            version = stream.readInt32()
            print version
            if version < FILE_VERSION:
                raise IOError, "old and unreadable file format"
            elif version > FILE_VERSION:
                raise IOError, "new and unreadable file format"
            stream.setVersion(QDataStream.Qt_4_2)
            rows = stream.readInt16()
            cols = stream.readInt16()
            print rows, cols
            tmp_map = []
            kind = 0
            for i in range(rows):
                tmp_map.append([])
                for j in range(cols):
                    kind = stream.readInt16()
                    print kind
                    tmp_map[i].append(basic.Map_Basic(kind))
            nums = stream.readInt16()
            print "unit",nums
            side = 0
            kind = 0
            tmp_unit = [[],[]]
            for i in range(nums):
                side = stream.readInt16()
                kind = stream.readInt16()
                position=(stream.readInt16(), stream.readInt16())
                tmp_unit[side].append(basic.Base_Unit(kind,position))

        except IOError,e:
            error = "Error:" + e
            raise IOError,error
        finally:
            if fh is not None:
                fh.close()
            if not error:
#                self.on_widthEdit_textEdited(QString("%d"%cols))
 #               self.on_heightEdit_textEdited(QString("%d"%rows))
                 self.width = cols
                 self.height = rows
                 self.widthEdit.setText("%d"%cols)
                 self.heightEdit.setText("%d"%rows)
                 self.mapEditWidget.setMap(tmp_map)
                 self.mapEditWidget.setUnits(tmp_unit)

     def changeWidth(self, new_width):
          if new_width == self.width:
               return
          answer = QMessageBox.question(self, QString.fromUtf8("警告"),
                                        QString.fromUtf8("在有单位或已编辑地形的时候改变地图大小，很可能"
                                                         "会打乱您之前编辑地图的对称性，一些在新的界线外的单位会消失，你确定要改变吗?"),
                                        QMessageBox.Yes, QMessageBox.No)
          if answer == QMessageBox.No:
               self.widthEdit.setText("%d"%self.width)
               return
          self.width = new_width
          self.widthEdit.setText("%d"%new_width)
          self.mapEditWidget.changeWidth(new_width)
          self.dirty = True

     def changeHeight(self, new_height):
          if new_width == self.width:
               return

          answer = QMessageBox.question(self, QString.fromUtf8("警告"),
                                        QString.fromUtf8("在有单位或已编辑地形的时候改变地图大小，很可能"
                                                         "会打乱您之前编辑地图的对称性，一些在新的界线外的单位会消失，你确定要改变吗?"),
                                        QMessageBox.Yes, QMessageBox.No)
          if answer == QMessageBox.No:
               self.heightEdit.setText("%d"%self.height)
               return
          self.heightEdit.setText("%d"%new_height)
          self.height = new_height
          self.mapEditWidget.changeHeight(new_height)
          self.dirty = True


#test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = basic.Map_Basic
    map_ = [[m(0), m(0), m(1), m(2), m(0), m(0)],
            [m(0), m(1), m(0), m(0), m(1), m(0)],
            [m(2), m(2), m(0), m(0), m(1), m(0)]]
    u = basic.Base_Unit
    units = [[u(0,(0,0)), u(1,(0,2))],
             [u(0,(3,1)), u(1,(2,0))]]
    form = MainForm()
    form.mapEditWidget.initEmpty(8,8)
    form.show()
    app.exec_()


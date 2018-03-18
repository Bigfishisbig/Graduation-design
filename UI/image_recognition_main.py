#-*-coding:utf8-*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, traceback, os, cv2, time
import open_image
from UI import image_recogntion
import CommonClass

save_flag = False
roiImg = []
class MyWindow_3(QtWidgets.QDialog, image_recogntion.Ui_dialog):

    def __init__(self):
        super(MyWindow_3, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openimage)
        self.pushButton_3.clicked.connect(self.img_clear)
        self.pushButton_6.clicked.connect(self.setToggle_btn)
        self.pushButton_4.clicked.connect(self.findName)
        self.pushButton_5.clicked.connect(self.save)


    def openimage(self):
        # 打开文件路径
        # 设置文件扩展名过滤,注意用双分号间隔
        global save_flag
        try:
            imgName, imgType = QtWidgets.QFileDialog.getOpenFileName(self,"打开图片",""," *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
            print("imgName:", imgName)
            imgPath = ''
            if imgName is not '': #判断是否选择了图片
                imgPath = imgName #选中了图片
            else:
                pass
            if imgPath is not '' and imgType is not '':  # 图片是否改变
                # 利用qlabel显示图片
                png = QtGui.QPixmap(imgPath).scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
                self.label.setPixmap(png)
                save_flag = True
                self.pushButton_2.setEnabled(save_flag)
                self.pushButton_2.clicked.connect(lambda: self.dealimage(imgPath))
            else:
                pass
        except:
            traceback.print_exc()


    def dealimage(self, imgPath):
        try:
            global roiImg
            if imgPath == '':
                self.label_2.clear()
                QtWidgets.QMessageBox.information(self, "提示", "请选择原图片！", QtWidgets.QMessageBox.Ok)
                self.pushButton_2.setEnabled(False)
            else:
                p = open_image.getPhoto()
                path, roiImg = p.getP(imgPath)
                png = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
                self.label_2.setPixmap(png)
                if os.path.exists(path):
                    os.remove(path)
                # self.pushButton_2.setEnabled(False)
        except:
            traceback.print_exc()

    def img_clear(self):
        self.label.clear()
        self.label_2.clear()
        global save_flag
        save_flag = False
        self.pushButton_2.setEnabled(save_flag)
        roiImg.clear()

    def setToggle_btn(self):
        if self.pushButton_6.isChecked():
            self.groupBox_2.setEnabled(True)
        else:
            self.groupBox_2.setEnabled(False)

    rows = None
    def findName(self):
        try:
            self.tableWidget.clearContents()  # 每一次查询时清除表格中信息
            self.tableWidget.setHorizontalHeaderLabels(['id', '姓名', '年级', '班级', '院系'])
            global rows
            self.sqlstring = "select * from t_student where "
            temp_sqlstring = self.sqlstring
            temp_sqlstring += " Sname like '%" + self.lineEdit.text() + "%'"
            get_table = CommonClass.Common()
            rows,row = get_table.get_data(temp_sqlstring)
            if row == 0:
                vol = 0
                QtWidgets.QMessageBox.information(self, "提示", "查无此人物记录！", QtWidgets.QMessageBox.Ok)
            else:
                vol = len(rows[0])# 取得记录个数，用于设置表格的行数
                vol = vol - 1

            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(vol)


            for i in range(row):
                for j in range(vol):
                    temp_data = rows[i][j]  # 临时记录，不能直接插入表格
                    data = QtWidgets.QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)
        except:
            traceback.print_exc()


    def save(self):
        try:
            row = self.tableWidget.currentRow()
            print ("row:",row)
            if row < 0:
                QtWidgets.QMessageBox.information(self, "提示", "请选择存储人物位置！", QtWidgets.QMessageBox.Ok)
            else:
                self.textBrowser_3.clear()
                addr = rows[row][-1]
                num = len(roiImg)
                if num is not 0:
                    path = addr + str(time.time()) + '.jpg'  # 时间戳命名
                    self.textBrowser_3.setText(path)
                    new_path = self.textBrowser_3.toPlainText()
                    if num == 1:
                        # cv2.imwrite(new_path, roiImg[0])
                        cv2.imencode('.jpg', roiImg[0])[1].tofile(new_path)   # 写入图像
                        QtWidgets.QMessageBox.information(self, "提示", "存储成功！", QtWidgets.QMessageBox.Ok)
                    else:
                        QtWidgets.QMessageBox.information(self, "提示", "有多个人物，无法存储！", QtWidgets.QMessageBox.Ok)
                else:
                    QtWidgets.QMessageBox.information(self, "提示", "无图像存储！", QtWidgets.QMessageBox.Ok)
            self.tableWidget.clearSelection()  # 取消表格选中
        except:
            traceback.print_exc()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow_3()
    MainWindow.show()
    sys.exit(app.exec_())
#-*-coding:utf8-*-
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
import read_camera, open_camera, dataSet, train_model, open_image
from UI import main_windows, loginGUI, image_recogntion
import traceback, pymysql
from PyQt5 import QtWidgets, QtGui

class MyWindow(QtWidgets.QWidget, loginGUI.Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.msg)

    def msg(self):

        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                passwd='',
                db='info',
                #
                charset='utf8',
            )
            self.cur = self.conn.cursor()

            self.sqlstring = "select password from t_administrator where "
            temp_sqlstring = self.sqlstring
            print(temp_sqlstring)
            mystr = self.lineEdit.text()
            print(mystr)
            temp_sqlstring += "username = '" + mystr + "'"
            print(temp_sqlstring)
            self.cur.execute(temp_sqlstring)
            data = self.cur.fetchall()
            for row in data:
                username = row[0]
            print("data:", username)
            print("hahaha")
            print(self.lineEdit_2.text())
            if username == self.lineEdit_2.text():
                print('yes')
                self.close()
                self.w = MyWindow_2()
                self.w.show()

            else:
                print('NO')
        except:
            # 输出异常信息
            traceback.print_exc()
            # 如果发生异常，则回滚
            self.conn.rollback()
        finally:
            self.conn.close()

    def output(self):
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())




class MyWindow_2(QtWidgets.QMainWindow, main_windows.Ui_MainWindow):
    def __init__(self):
        super(MyWindow_2, self).__init__()
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.getPictrue)
        self.pushButton_4.clicked.connect(self.read_camera)

    def read_camera(self):
        self.camera = read_camera.Camera_reader()
        self.camera.build_camera()

    def getPictrue(self):
        try:
            self.name = self.lineEdit.text()
            print (self.name)
            self.getP = open_camera.getPhoto()
            self.getP.getP(self.name)

            self.dataset = dataSet.DataSet('D:\\myProject\\pictures\\dataset')
            self.model = train_model.Model()
            self.model.read_trainData(self.dataset)
            self.model.build_model()
            self.model.train_model()
            self.model.evaluate_model()
            self.model.save()
        except:
            # 输出异常信息
            traceback.print_exc()
            # 如果发生异常，则回滚
            self.conn.rollback()

class MyWindow_3(QtWidgets.QDialog, image_recogntion.Ui_dialog):
    def __init__(self):
        super(MyWindow_3, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openimage)

    def openimage(self):
        # 打开文件路径
        # 设置文件扩展名过滤,注意用双分号间隔
        try:
            imgName, imgType = QtWidgets.QFileDialog.getOpenFileName(self,"打开图片",""," *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
            print(imgName)
            # 利用qlabel显示图片
            png = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
            self.label.setPixmap(png)

            p = open_image.getPhoto()
            img = p.getP(imgName)
            # png = QtGui.QPixmap(img).scaled(self.label_2.width(), self.label_2.height())
            # self.label_2.setPixmap(png)
        except:
            traceback.print_exc()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.show()
    sys.exit(app.exec_())

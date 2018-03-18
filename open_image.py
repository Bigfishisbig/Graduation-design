#-*-coding:utf8-*-
import cv2
import os
import traceback, numpy
import time
from PyQt5 import QtGui
from UI import image_recogntion as img

class getPhoto():
    def getP(self, imgPath):
        try:
            cascade = cv2.CascadeClassifier("Source\haarcascade_frontalface_alt.xml")
            cascade.load("F:\Git\Graduation-design\Source\haarcascade_frontalface_alt.xml")
            # self.img = cv2.imread(imgPath.encode("gbk"))
            self.img = cv2.imdecode(numpy.fromfile(imgPath, dtype=numpy.uint8), -1) # 读取图像
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            rect = cascade.detectMultiScale(gray, scaleFactor=1.15,minNeighbors=5,minSize=(5,5),flags=cv2.CASCADE_SCALE_IMAGE)
            roi = []
            if not rect is ():
                i = 0
                for x, y, z, w in rect:
                    roiImg = cv2.resize(gray[y:(y + w), x:(x + z)], (200, 200))
                    roi.append(roiImg)
                    cv2.rectangle(self.img, (x, y), (x + z, y + w), (0, 0, 255), 2)
                    i += 1
            self.save_path ="F:\Git\Graduation-design\Source\image\img_dealed.jpg" # 检测后原图的存放地址
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
            else:
                pass
            cv2.imwrite(self.save_path, self.img)
            return self.save_path, roi
        except:
            # 输出异常信息
            traceback.print_exc()
#
# if __name__ == '__main__':
#     photo = getPhoto()
#     photo.getP('asd')
#-*-coding:utf8-*-
import cv2
import os
import traceback
import time

class getPhoto():
    def getP(self, name):
        try:
            save_path = 'D:\\myProject\\pictures\\dataset\\%s\\'%name
            if os.path.exists(save_path):
                pass
            else:
                os.makedirs(save_path)
            cascade = cv2.CascadeClassifier("Source\haarcascade_frontalface_alt.xml")
            cap = cv2.VideoCapture(0)
            i = 0
            flag = 0
            while flag < 20:
                ret,frame = cap.read()
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                rect = cascade.detectMultiScale(gray, 1.3, 5)
                # rect = cascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=9,minSize=(50,50),flags = cv2.CASCADE_SCALE_IMAGE)
                print ("rect",rect)
                if not rect is ():
                    flag = flag + 1
                    for x,y,z,w in rect:
                        roiImg = cv2.resize(gray[y:(y + w), x:(x + z)], (200, 200))
                        # cv2.imwrite(save_path+str(i)+'.jpg',roiImg)
                        cv2.imencode('.jpg', roiImg)[1].tofile(save_path+str(i))  # 写入图像
                        cv2.rectangle(frame,(x,y),(x+z,y+w),(0,0,255),2)
                        i +=1
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) &0xFF == ord('q'):
                    break
                time.sleep(1)
            cap.release()
            cv2.destroyAllWindows()
        except:
            # 输出异常信息
            traceback.print_exc()
            # 如果发生异常，则回滚
            self.conn.rollback()

# if __name__ == '__main__':
#     photo = getPhoto()
#     photo.getP('asd')
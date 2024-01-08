import os, sys
import shutil

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon,QPixmap

form_class = uic.loadUiType(os.getcwd() + '/ui/' + os.path.splitext(os.path.basename(__file__))[0] + '.ui')[0]
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# form = resource_path("ui/{0}".format(os.path.splitext(os.path.basename(__file__))[0] + '.ui'))
# form_class = uic.loadUiType(form)[0]

class WdgPIC(QMainWindow, form_class): #QMainWindow와 ui를 변환한 class의 다중상속
    def __init__(self): # 초기값 설정
        super( ).__init__( ) # 부모 클래스의 초기값 호출
        self.setupUi(self) # Ui 를 셋업
        self.initUI()
        self.listener()

    def initUI(self):
        self.setWindowTitle(self.tr('Performance Improvement Clculation'))
        self.setWindowIcon(QIcon(QPixmap(":WdgPIC")))

        self.lb_result.setText("")

    def listener(self):
        self.btnRun.clicked.connect(self.run)

    def run(self):
        self.lb_result.setText("")
        if self.txt_t1.text() !="" and self.txt_t2.text() !="":
            
            if self.check_float(self.txt_t1.text()) and self.check_float(self.txt_t2.text()):
                t1 = float(self.txt_t1.text()) # 이전수치
                t2 = float(self.txt_t2.text()) # 현재수치

                result = ((t1-t2)/t2)
                
                self.lb_result.setText("속도향상율 : " + str(result)+"\n성능개선율 : "+str(result*100)+"%")
        else:
            QMessageBox.warning(self,self.tr("Alert"),"값을 입력하세요")
            return

    
    def check_float(self,txt):
        result = False
        partition = txt.partition(".")

        if txt.isdigit():
            newelement = float(txt)
            result = True
            return result

        elif (
            (partition[0].isdigit() and partition[1] == "." and partition[2].isdigit())
            or (partition[0] == "" and partition[1] == "." and partition[2].isdigit())
            or (partition[0].isdigit() and partition[1] == "." and partition[2] == "")
        ):
            result = True
            return result
        else:
            QMessageBox.warning(self,self.tr("Alert"),"숫자 형태가 아닙니다.")
            return result

    

# if __name__ == '__main__':
#     app = QApplication(sys.argv) # app 생성
#     myWindow = WdgPIC( ) # Ui를 myWindow에 할당
#     myWindow.show( ) # Ui 출력
#     app.exec_( ) # app무한루프
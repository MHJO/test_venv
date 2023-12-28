import os, sys

import modules
from modules import WdgUnzip
from modules import WdgFileMerge

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType(os.getcwd() + '/ui/' + os.path.splitext(os.path.basename(__file__))[0] + '.ui')[0]


class WindowClass(QMainWindow, form_class): #QMainWindow와 ui를 변환한 class의 다중상속
    

    def __init__(self): # 초기값 설정
        super( ).__init__( ) # 부모 클래스의 초기값 호출
        self.setupUi(self) 
        self.initUI()
        self.init()
        self.wdg_unzip = None
        self.wdg_filemerge = None

    def initUI(self):
        self.setWindowTitle(self.tr('My Tool'))

    def init(self):
        self.btn_unzip.clicked.connect(self.show_unzip)
        self.btn_FileMerge.clicked.connect(self.show_FileMerge)

    # 압축해제
    def show_unzip(self):
        try:
            if self.wdg_unzip is None:
                self.wdg_unzip = WdgUnzip.WdgUnzip()
                self.wdg_unzip.show()

            elif self.wdg_unzip is not None:
                self.wdg_unzip.close()
                self.wdg_unzip = WdgUnzip.WdgUnzip()
                self.wdg_unzip.show()

        except Exception as e:
            print (str(e))
    
    # File 병합
    def show_FileMerge(self):
        try:
            if self.wdg_filemerge is None:
                self.wdg_filemerge = WdgFileMerge.WdgFileMerge()
                self.wdg_filemerge.show()

            elif self.wdg_filemerge is not None:
                self.wdg_filemerge.close()
                self.wdg_filemerge = WdgFileMerge.WdgFileMerge()
                self.wdg_filemerge.show()

        except Exception as e:
            print (str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv) # app 생성
    myWindow = WindowClass( ) # Ui를 myWindow에 할당
    myWindow.show( ) # Ui 출력
    app.exec_( ) # app무한루프

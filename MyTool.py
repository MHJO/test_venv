import os, sys
from functools import partial

import modules
from modules import WdgUnzip
from modules import WdgFileMerge
from modules import WdgFileDivision

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import uic

form_class = uic.loadUiType(os.getcwd() + '/ui/' + os.path.splitext(os.path.basename(__file__))[0] + '.ui')[0]
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# form = resource_path("ui/{0}".format(os.path.splitext(os.path.basename(__file__))[0] + '.ui'))
# form_class = uic.loadUiType(form)[0]

class MyTool(QMainWindow, form_class): #QMainWindow와 ui를 변환한 class의 다중상속
    

    def __init__(self): # 초기값 설정
        super( ).__init__( ) # 부모 클래스의 초기값 호출
        self.setupUi(self) 
        self.wdg_unzip = None
        self.wdg_filemerge = None
        self.wdgFileDivision = None

        self.initUI()
        self.init()
        self.listener()
        

    def initUI(self):
        self.setWindowTitle(self.tr('My Tool'))
        self.setWindowIcon(QIcon(QPixmap(":windows_icon")))

    def init(self):
        self.unzip = partial(self.show_widget,self.wdg_unzip,WdgUnzip.WdgUnzip())
        self.merge = partial(self.show_widget,self.wdg_filemerge,WdgFileMerge.WdgFileMerge())
        self.division = partial(self.show_widget,self.wdgFileDivision,WdgFileDivision.WdgFileDivision())

    def listener(self):
        self.btn_unzip.clicked.connect(self.unzip)
        self.btn_FileMerge.clicked.connect(self.merge)
        self.btn_Division.clicked.connect(self.division)

    def show_widget(self, widget, widget_class):
        try:
            if widget is None:
                widget = widget_class
                widget.show()

            elif widget is not None:
                widget.close()
                widget = widget_class
                widget.show()

        except Exception as e:
            print (str(e))

    

if __name__ == '__main__':
    app = QApplication(sys.argv) # app 생성
    myWindow = MyTool( ) # Ui를 myWindow에 할당
    myWindow.show( ) # Ui 출력
    app.exec_( ) # app무한루프
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

class WdgUnzip(QMainWindow, form_class): #QMainWindow와 ui를 변환한 class의 다중상속
    def __init__(self): # 초기값 설정
        super( ).__init__( ) # 부모 클래스의 초기값 호출
        self.setupUi(self) # Ui 를 셋업
        self.init()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr('Unzip'))
        self.setWindowIcon(QIcon(QPixmap(":WdgUnzip")))
        self.progressBar.setValue(0)
        

    def init(self):
        self.btn_inputPath.clicked.connect(lambda: self.open_folder(self.txt_intputPath))
        self.btn_outputPath.clicked.connect(lambda: self.open_folder(self.txt_outputPath))
        self.btn_unzip.clicked.connect(self.unzip)

    
    def open_folder(self, txt):
        try:
            folder=QFileDialog.getExistingDirectory(self,"Select folder")
            txt.setText(folder)
        except Exception as e:
            print (e.__str__)
            QMessageBox.warning(self,self.tr("Alert"),e.__str__)

    def unzip(self):
        try:
            input_path=self.txt_intputPath.text()
            output_dir = self.txt_outputPath.text()
            
            if input_path == "" or output_dir =="":
                QMessageBox.warning(self,self.tr("Alert"),"경로를 입력해주세요")
                return
            
            zipCount = [cnt for cnt in os.listdir(input_path) if os.path.splitext(cnt)[1]==".zip"]
            self.progressBar.setMaximum(len(zipCount))
            
            count = 1
            for file_csv in os.listdir(input_path):
                if os.path.splitext(file_csv)[1] ==".zip":
                    
                    print (file_csv)
                    file =input_path+"/"+file_csv
                    format = "zip"
                    shutil.unpack_archive(file, output_dir, format)
                    self.progressBar.setValue(count)
                    count +=1

            QMessageBox.information(self,self.tr("Alert"),self.tr("압축해제가 완료되었습니다."))

        except Exception as e:
            print (e.__str__)
            QMessageBox.warning(self,self.tr("Alert"),e.__str__)

# if __name__ == '__main__':
#     app = QApplication(sys.argv) # app 생성
#     myWindow = WdgUnzip( ) # Ui를 myWindow에 할당
#     myWindow.show( ) # Ui 출력
#     app.exec_( ) # app무한루프
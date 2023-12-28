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

class WdgFileMerge(QMainWindow, form_class): #QMainWindow와 ui를 변환한 class의 다중상속
    def __init__(self): # 초기값 설정
        super( ).__init__( ) # 부모 클래스의 초기값 호출
        self.setupUi(self) # Ui 를 셋업
        self.init()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr('File Merge'))
        self.setWindowIcon(QIcon(QPixmap(":WdgFileMerge")))
        self.progressBar.setValue(0)
        

    def init(self):
        self.btn_inputPath.clicked.connect(lambda: self.select_files(self.txt_intputPath))
        self.btn_outputPath.clicked.connect(lambda: self.save_file(self.txt_outputPath))
        self.btn_FileMerge.clicked.connect(self.fileMerge)

    
    def select_files(self, txt):
        try:
            filter = "csv files(*.csv)"
            files=QFileDialog.getOpenFileNames(self,"Select files","",filter)[0]
            txt.setText(str(files).replace("[","").replace("]","").replace("'",""))
        except Exception as e:
            print (e.__str__)
            QMessageBox.warning(self,self.tr("Alert"),e.__str__)

    def save_file(self, txt):
        try:
            filter = "csv files(*.csv)"
            file=QFileDialog.getSaveFileName(self,"Save file","",filter)[0]
            txt.setText(file)
        except Exception as e:
            print (e.__str__)
            QMessageBox.warning(self,self.tr("Alert"),e.__str__)

    def fileMerge(self):
        try:
            input_files=self.txt_intputPath.text()
            output_file = self.txt_outputPath.text()
            
            
            if input_files == "" or output_file =="":
                QMessageBox.warning(self,self.tr("Alert"),"경로를 입력해주세요")
                return
            

            zipCount = [cnt1 for cnt1 in input_files.split(",")]
            self.progressBar.setMaximum(len(zipCount))

            # 파일 리스트
            if self.chk_fixHeader.isChecked():
                with open(output_file, 'w') as outfile:
                    cnt = 1
                    for filename in input_files.split(","):
                        print (filename)
                        with open(filename.strip()) as file:
                            if cnt == 1:
                                for i in (file.readlines()):
                                    outfile.write(i)
                                outfile.write("\n")
                            else:
                                for i in (file.readlines()[1:]):
                                    outfile.write(i)
                        self.progressBar.setValue(cnt)
                        cnt +=1
            else:
                with open(output_file, 'w') as outfile:
                    cnt = 1
                    for filename in input_files.split(","):
                        print (filename)
                        with open(filename.strip()) as file:
                            for i in (file.readlines()):
                                outfile.write(i)
                            outfile.write("\n")
                        self.progressBar.setValue(cnt)
                        cnt +=1

            QMessageBox.information(self,self.tr("Alert"),self.tr("파일 병합이 완료되었습니다."))

        except Exception as e:
            print (str(e))
            QMessageBox.warning(self,self.tr("Alert"),str(e))

# if __name__ == '__main__':
#     app = QApplication(sys.argv) # app 생성
#     myWindow = WdgFileMerge( ) # Ui를 myWindow에 할당
#     myWindow.show( ) # Ui 출력
#     app.exec_( ) # app무한루프
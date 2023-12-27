import os, sys
import csv

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon,QPixmap
import pandas


form_class = uic.loadUiType(os.getcwd() + '/ui/' + os.path.splitext(os.path.basename(__file__))[0] + '.ui')[0]
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# form = resource_path("ui/{0}".format(os.path.splitext(os.path.basename(__file__))[0] + '.ui'))
# form_class = uic.loadUiType(form)[0]

class WdgFileDivision(QMainWindow, form_class): #QMainWindow와 ui를 변환한 class의 다중상속
    def __init__(self): # 초기값 설정
        super( ).__init__( ) # 부모 클래스의 초기값 호출
        self.setupUi(self) # Ui 를 셋업
        self.init()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr('File Division'))
        self.progressBar.setValue(0)
        self.txt_rm_text.setText('D')
                

    def init(self):
        self.btn_inputPath.clicked.connect(lambda: self.select_file(self.txt_intputPath))
        self.btn_outputPath.clicked.connect(lambda: self.save_file(self.txt_outputPath))
        self.btn_fileDivision.clicked.connect(self.fileDivision)
        self.chk_auto.stateChanged.connect(self.checkChagned)
        self.chk_rm_text.stateChanged.connect(self.checkChagned)
        
    
    def checkChagned(self):
        if self.chk_auto.isChecked():
            self.txt_outputPath.setEnabled(False)
            self.btn_outputPath.setEnabled(False)
        elif self.chk_auto.isChecked() == False:
            self.txt_outputPath.setEnabled(True)
            self.btn_outputPath.setEnabled(True)

        if self.chk_rm_text.isChecked():
            self.txt_rm_text.setEnabled(True)
        elif self.chk_rm_text.isChecked() == False:
            self.txt_rm_text.setEnabled(False)

    # region 파일 선택
    def select_file(self, txt):
        try:
            filter = "csv file(*.csv)"
            file=QFileDialog.getOpenFileName(self,"Select files","",filter)[0]
            txt.setText(file)
        except Exception as e:
            print (e.__str__)
            QMessageBox.warning(self,self.tr("Alert"),e.__str__)
    # endregion

    # region 저장 경로 선택
    def save_file(self, txt):
        try:
            filter = "csv file(*.csv)"
            file=QFileDialog.getSaveFileName(self,"Save file","",filter)[0]
            txt.setText(file)
        except Exception as e:
            print (e.__str__)
            QMessageBox.warning(self,self.tr("Alert"),e.__str__)
    # endregion

    # region 파일 분할 기능 -main
    def fileDivision(self):
        try:
            input_file=self.txt_intputPath.text()
            output_file = self.txt_outputPath.text()
            
            
            if input_file == "" or output_file =="":
                if self.chk_auto.isChecked():
                    pass
                else:
                    QMessageBox.warning(self,self.tr("Alert"),"파일을 입력해주세요")
                    return
            
            if self.chk_auto.isChecked():
                self.auto_savePath()
            else:
                self.Noauto_savePath()
            
            QMessageBox.information(self,self.tr("Alert"),self.tr("파일 분할이 완료되었습니다."))

        except Exception as e:
            print (str(e))
            QMessageBox.warning(self,self.tr("Alert"),str(e))
    
    # endregion

    # region [자동이름 처리]  
    def auto_savePath(self):
        # self.chk_auto 체크박스를 누른 경우 호출
        inputFile = self.txt_intputPath.text()
        outdir = os.path.dirname(inputFile)

        # 특정 구문 포함 줄 삭제 여부
        if self.chk_rm_text.isChecked():
            # outdir = os.path.dirname(output)
            result = self.del_value_line(inputFile,outdir)
        else:
            result = inputFile

        dvline = self.sb_line.value()  # 분할 라인 수
        try:
            data = pandas.read_csv(result,encoding='cp949', sep='\t')

            # 파일을 분할합니다.
            chunks = [data[i:i+dvline] for i in range(0, data.shape[0], dvline)]

            format1 = os.path.splitext(result)[1]
            outNm = os.path.basename(os.path.splitext(result)[0])
            for i, chunk in enumerate(chunks):
                outputFile = f"{outdir}/{outNm}_{i}{format1}"
                chunk.to_csv(outputFile, quoting=csv.QUOTE_NONE)
        except Exception as e:
            print (str(e))

        # with open(result,'r') as f1:
        #     lines = f1.readlines()

        # cnt =0
        # Fnt=1
        # for line in lines:
        #     format1 = os.path.splitext(result)[1]
        #     fileNm = os.path.basename(os.path.splitext(result)[0])
        #     outputFile = f"{outdir}/{fileNm}_{Fnt}{format1}"
            
        #     fw=open(outputFile,'a')    
        #     fw.write(line)
        #     fw.close()        

        #     if cnt == dvline:
        #         cnt=0
        #         Fnt+=1
        #     cnt+=1

    # endregion


    
    # region [특정 구문 값 포함 라인 제거]
    def del_value_line(self, inputFile, outdir):
        fileNm = os.path.basename(os.path.splitext(inputFile)[0])
        format1 = os.path.splitext(inputFile)[1]
        outputFile = f"{outdir}/{fileNm}_md{format1}"

        rm_text = self.txt_rm_text.text()

        with open(inputFile, 'r') as f1, open(outputFile, 'w', newline='') as f2:
            rdr = csv.reader(f1)
            wr = csv.writer(f2)
            for line in rdr:
                if (rm_text not in line):
                    wr.writerow(line)

        return outputFile
    # endregion

    # region [자동이름 처리 아닌 경우]
    def Noauto_savePath(self):
        inputFile = self.txt_intputPath.text()
        output = self.txt_outputPath.text()
        # 특정 구문 포함 줄 삭제 여부
        if self.chk_rm_text.isChecked():
            outdir = os.path.dirname(output)
            result = self.del_value_line(inputFile,outdir)
        else:
            result = inputFile
        
        dvline = self.sb_line.value()
        try:
            data = pandas.read_csv(result,encoding='cp949', sep='\t')

            # 파일을 분할합니다.
            chunks = [data[i:i+dvline] for i in range(0, data.shape[0], dvline)]

            outdir = os.path.dirname(output)
            outNm = os.path.basename(os.path.splitext(output)[0])
            format1 = os.path.splitext(result)[1]
            for i, chunk in enumerate(chunks):
                # 각 분할된 파일에 헤더를 포함하여 저장합니다.
                outputFile = f"{outdir}/{outNm}_{i}{format1}"
                chunk.to_csv(outputFile, index=False, doublequote=False, escapechar='"', quoting=csv.QUOTE_NONE)

        except Exception as e:
            print (str(e))

        
        # outdir = os.path.dirname(output)
        # outNm = os.path.basename(os.path.splitext(output)[0])

        # dvline = self.sb_line.value()

        # with open(result, 'r') as f1:
        #     lines = f1.readlines()

        # line_count =0
        # File_count=1
        # for line in lines:
        #     format1 = os.path.splitext(result)[1]
        #     outputFile = f"{outdir}/{outNm}_{File_count}{format1}"

        #     with open(outputFile, 'a') as fw:
        #         fw.write(line)

        #     if line_count == dvline:
        #         line_count=0
        #         File_count+=1
        #     line_count+=1

       


    # endregion
            
    def get_header(self, inputFile):
        with open(inputFile, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
        
        return header



if __name__ == '__main__':
    app = QApplication(sys.argv) # app 생성
    myWindow = WdgFileDivision( ) # Ui를 myWindow에 할당
    myWindow.show( ) # Ui 출력
    app.exec_( ) # app무한루프
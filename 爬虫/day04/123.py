#!/user/bin/python3
# -*- coding:utf-8 -*-
'''''
Create Tool Form
'''
__author__ = 'zhangss-c'
import sys
import os
import fnmatch
import shutil, tarfile, zipfile, rarfile
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QProgressBar, QPushButton,
                             QScrollBar, QSizePolicy, QSlider, QSpinBox, QStyleFactory,
                             QVBoxLayout, QWidget,QMessageBox)


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.style = """ 
                        QPushButton{background-color:grey;color:white;} 
                        #window{ background:white; }
                        #test{ background-color:black;color:white; }
                    """
        self.setStyleSheet(self.style)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.edit1 = None
        self.edit2 = None
        self.fileName = "C:/Program Files/Glodon/GCCP/5.0-X64"
        self.destFileName = ""
        self.format = ""
        self.fileSize = ""

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, 500, 220)
        self.setWindowTitle('杀毒测试-打包工具')
        self.setObjectName("window")

        ##设置及选择安装包的路径
        lbl1 = QLabel("安装包路径：", self)
        lbl1.setFixedSize(90, 25)
        self.edit1 = QLineEdit(self)
        self.edit1.setText(self.fileName)
        btn1 = QPushButton("选择目录", self)
        btn1.clicked.connect(self.showFile)

        ##设置及选择存放压缩包的路径
        lbl2 = QLabel("压缩包存放路径：", self)
        lbl2.setFixedSize(90, 25)
        self.edit2 = QLineEdit(self)
        btn2 = QPushButton("选择目录", self)
        btn2.clicked.connect(self.showDestFile)

        ##设置需要压缩文件的大小
        lbl3 = QLabel("设置大小：", self)
        lbl3.setFixedSize(90, 25)
        edit3 = QLineEdit(self)
        edit3.textEdited[str].connect(self.onFileSizeChanged)
        lbl31 = QLabel("如1K则输入1024", self)

        ##设置需要过滤的文件格式
        lbl4 = QLabel("设置要过滤的文件格式：", self)
        lbl4.setFixedSize(140, 30)
        edit4 = QLineEdit(self)
        edit4.textEdited[str].connect(self.onChanged)
        lbl41 = QLabel("如dll、exe", self)

        ##选择需要压缩的格式
        lbl5 = QLabel("选择压缩格式：", self)
        lbl5.setFixedSize(90, 25)
        self.combox = QComboBox(self)
        self.combox.insertItem(0, "zip")
        self.combox.insertItem(1, "rar")

        ##设置确定及取消键
        btn6 = QPushButton("确定", self)
        btn6.clicked.connect(self.DoExcute)
        btn7 = QPushButton("取消", self)
        btn7.clicked.connect(self.close)

        ##设置布局格式
        hbox1 = QHBoxLayout()  # 水平布局
        hbox1.addWidget(lbl1)
        hbox1.addWidget(self.edit1)
        hbox1.addWidget(btn1)

        hbox2 = QHBoxLayout()  # 水平布局
        hbox2.addWidget(lbl2)
        hbox2.addWidget(self.edit2)
        hbox2.addWidget(btn2)

        hbox3 = QHBoxLayout()  # 水平布局
        hbox3.addWidget(lbl3)
        hbox3.addWidget(edit3)
        hbox3.addWidget(lbl31)

        hbox4 = QHBoxLayout()  # 水平布局
        hbox4.addWidget(lbl4)
        hbox4.addWidget(edit4)
        hbox4.addWidget(lbl41)

        hbox5 = QHBoxLayout()  # 水平布局
        hbox5.addWidget(lbl5)
        hbox5.addWidget(self.combox)

        hbox6 = QHBoxLayout()  # 水平布局
        hbox6.addStretch()
        hbox6.addWidget(btn6)
        hbox6.addWidget(btn7)

        vbox = QVBoxLayout()  # 垂直布局
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        self.setLayout(vbox)

        self.show()

    def showFile(self):
        self.fileName = QFileDialog.getExistingDirectory(self,
                                                         "选取文件夹",
                                                         "C:/")
        self.edit1.clear()
        self.edit1.setText(self.fileName)

    def showDestFile(self):
        self.destFileName = QFileDialog.getExistingDirectory(self,
                                                             "选取文件夹",
                                                             "C:/")
        self.edit2.clear()
        self.edit2.setText(self.destFileName)

    def onChanged(self, text):
        self.format = text

    def onFileSizeChanged(self, text):
        self.fileSize = text


    ##遍历所有后缀名为dll或exe的文件
    def searchAll(self):
        for root, dirs, files in os.walk(self.fileName):
            if not os.path.exists(self.destFileName + '/' + self.format + '/more/'):
                os.makedirs(self.destFileName + '/' + self.format + '/more/')
            if not os.path.exists(self.destFileName + '/' + self.format + '/less/'):
                os.makedirs(self.destFileName + '/' + self.format + '/less/')
            for name in files:
                if fnmatch.fnmatch(name, '*.'+ self.format):
                    if os.path.getsize(os.path.join(root, name)) >= int(self.fileSize):
                        shutil.copy(os.path.join(root, name),
                                    self.destFileName + '/' + self.format + '/more/' + name)  ##大于50M的文件放在more文件夹下
                    else:
                        shutil.copy(os.path.join(root, name),
                                    self.destFileName + '/' + self.format + '/less/' + name)  ##小于50M的文件放在less文件夹下

    #将文件拆分到不同的文件夹下，每个文件夹的大小不大于你设置的大小，且文件不能超过20个
    def chai_fen_wenjian(self):
        sum = 0
        i = 0
        num = 0
        os.makedirs( self.destFileName + '/' + self.format + '/shadu/'+self.format + str(i))
        file = self.destFileName + '/' + self.format + "/less/"
        for root, dirs, files in os.walk(file):
            for name in files:
                sum += os.path.getsize(os.path.join(root, name))
                if sum <= int(self.fileSize) and num < 20:
                    shutil.move(os.path.join(root, name), self.destFileName + '/' + self.format + '/shadu/'+self.format + str(i) + '/' + name)
                    num += 1
                else:
                    sum = os.path.getsize(os.path.join(root, name))
                    num = 1
                    i += 1
                    os.makedirs(self.destFileName + '/' + self.format + '/shadu/'+self.format + str(i))
                    shutil.move(os.path.join(root, name), self.destFileName + '/' + self.format + '/shadu/'+self.format + str(i) + '/' + name)

    #将文件压缩成zip格式的文件
    def zip_Dir(self):
        srcPath = self.destFileName + '/' + self.format + '/shadu/'
        for dir in os.listdir(srcPath):
            zf = zipfile.ZipFile(srcPath + dir + ".zip", "w", zipfile.ZIP_DEFLATED)
            for file in os.listdir(srcPath + '/' + dir):
                zf.write(os.path.join(srcPath + '/' + dir, file), dir)
                # rarHandle.add(os.path.join(srcPath+'/'+dir,file))
            zf.close()

    #将文件压缩成tar格式的文件
    def tar_Dir(self):
        srcPath = self.destFileName + '/' + self.format + '/shadu/'
        for dir in os.listdir(srcPath):
            tarHandle = tarfile.open(srcPath + dir + '.tar.gz', "w:gz")
            for file in os.listdir(srcPath + '\\' + dir):
                tarHandle.add(os.path.join(srcPath + '\\' + dir, file))

            tarHandle.close()

    def chose_Type(self):
        if self.combox.currentText() == "zip":
            self.zip_Dir()
        elif self.combox.currentText() == "tar":
            self.tar_Dir()


    def closeEvent1(self):
        reply = QMessageBox.information(self, '提示', '打包'+self.format+'完成',
                                     QMessageBox.Yes | QMessageBox.No)


    def DoExcute(self):

        self.searchAll()
        self.chai_fen_wenjian()
        self.chose_Type()

        self.closeEvent1()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyDialog()
    sys.exit(app.exec_())

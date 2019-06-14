#this file convert txt file to html file
#テキストファイルを読み込んで，その中にある改行コードを消して空白を挿入する
#改行コードを消す動作はは，最終的にhtmlに変換するため，無駄ではあるが行う
#by J.Yagi 2019/06/07

import sys
import os
import pyperclip
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        html1 = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>thesis_converter</title></head><body><div>"
        f = open("result.html","w")
        f.write(html1)
        f.close()
        self.button1 = QPushButton('入力を追加')
        self.button1.clicked.connect(self.input)
        self.button2 = QPushButton('改行を挿入')
        self.button2.clicked.connect(self.inputbr)
        self.button3 = QPushButton('[終了]：HTMLの作成 → "result.html"')
        self.button3.clicked.connect(self.makefile)
        self.button4= QPushButton('空行を挿入')
        self.button4.clicked.connect(self.inputbr2)
        self.button5= QPushButton('ペースト')
        self.button5.clicked.connect(self.clipPaste)
        self.button6= QPushButton('画面クリア')
        self.button6.clicked.connect(self.clearDisplay)
        self.label = QLabel('使い方：コピーした文をペーストすると最終的に改行を含まないHTML文に変換できます．ボタン操作で意図的に挿入することもできます．')
        self.inputText = QTextEdit()
        self.inputText.setText("")

        buttonlayout1 = QHBoxLayout()                       #テキスト操作のボタン群
        buttonlayout1.addWidget(self.button5)
        buttonlayout1.addWidget(self.button6)
        
        buttonlayout2 = QHBoxLayout()                       #ファイルに書き込むボタン群
        buttonlayout2.addWidget(self.button1)
        buttonlayout2.addWidget(self.button2)
        buttonlayout2.addWidget(self.button4)
        
        layout = QVBoxLayout()                              #最終的なレイアウト
        layout.addWidget(self.label)
        layout.addWidget(self.inputText)
        layout.addLayout(buttonlayout1)
        layout.addLayout(buttonlayout2)
        layout.addWidget(self.button3)
        
        self.setLayout(layout)
        self.setWindowIcon(QIcon(self.resource_path('resources/icon.png')))
        self.setWindowTitle("Thesis_converter")

    def resource_path(self,relative_path):              #実行可能ファイルにしたときにアイコンのパスを直す
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def clearDisplay(self):                            #画面をクリア
        self.inputText.setText("")

    def clipPaste(self):                               #クリップボードをペースト
        self.inputText.setText(pyperclip.paste())

    def input(self):
        origin_text = self.inputText.toPlainText()
        converted_text = origin_text.replace('\r',' ') #改行コードごとに取り除く
        converted_text = converted_text.replace('\n',' ')
        try:
            f = open("result.html","a")
            f.write(converted_text)
        except UnicodeEncodeError:
            QMessageBox().warning(self, "UnicodeEncodeError", "処理できない文字が含まれています.\nその文字を消してやり直してください.", QMessageBox.Ok)
            # print("処理できない文字が含まれています.\nその文字を消してやり直してください．")
        except IOError:
            print("IOError")
        else:
            self.inputText.setText("")
        finally:
            f.close()

    def inputbr(self):
        with open("result.html","a") as f:
            f.write("<br>")

    def inputbr2(self):
        with open("result.html","a") as f:
            f.write("<br><br>")
        
    def makefile(self):
        html2 = "</div></body></html>"
        with open("result.html","a") as f:
            f.write(html2)
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setGeometry(20, 20, 900, 900)
    main_window.setWindowFlags(Qt.Window|Qt.WindowMinMaxButtonsHint)
    
    main_window.show()
    sys.exit(app.exec_())
import os, sys, time, random, re, csv
from survey import Survey_Form
from basic import Basic_Form
from explain import Explain_Form
from suggest import Suggest_Form
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMessageBox, QMainWindow
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.Qt import QUrl
random.seed(time.time())

def listdir(path):
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        list_name.append(file_path)
    return list_name

class MyWindow_1(QWidget, Explain_Form):
    def __init__(self, music_name):
        super().__init__()
        self.music = music_name
        self.center()
        self.init_ui()

    def init_ui(self):
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('隐私声明')
        self.setWindowIcon(QIcon(img_path + '/private.ico'))
        self.checkBox.stateChanged.connect(self.ChangeBtn)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def ChangeBtn(self):
        btn = self.pushButton
        btn.setEnabled(True)
        btn.clicked.connect(self.open_new_window)

    def open_new_window(self):
        self.window2 = MyWindow_2(self.music)
        self.window2.show()
        self.close()

    def closeEvent(self, event):
        global exit_flag
        event.accept()
        exit_flag = True

class MyWindow_2(QWidget, Basic_Form):
    def __init__(self, music_name):
        super().__init__()
        self.music = music_name
        self.ltext_1, self.ltext_2, self.ltext_3, self.ltext_4 = None, None, None, None
        self.ltext, self.rtext = None, None
        self.center()
        self.init_ui()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def closeEvent(self, event):
        global exit_flag
        event.accept()
        exit_flag = True

    def init_ui(self):
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('基本信息')
        self.setWindowIcon(QIcon(img_path + '/info.ico'))
        self.pushButton.setEnabled(False)
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z^\u4e00-\u9fa5]{8}")))
        self.lineEdit_2.setValidator(QIntValidator())
        self.lineEdit_2.setMaxLength(3)
        self.lineEdit_3.setValidator(QRegExpValidator(QRegExp("[a-zA-Z^\u4e00-\u9fa5]{8}")))
        self.lineEdit_4.setValidator(QRegExpValidator(QRegExp("[a-zA-Z^\u4e00-\u9fa5]{6}")))
        self.radioButton.clicked.connect(lambda: self.select_radioButton(self.radioButton))
        self.radioButton_2.clicked.connect(lambda: self.select_radioButton(self.radioButton_2))
        self.lineEdit.textChanged.connect(lambda: self.select_lineEdit(self.lineEdit))
        self.lineEdit_2.textChanged.connect(lambda: self.select_lineEdit(self.lineEdit_2))
        self.lineEdit_3.textChanged.connect(lambda: self.select_lineEdit(self.lineEdit_3))
        self.lineEdit_4.textChanged.connect(lambda: self.select_lineEdit(self.lineEdit_4))
        self.pushButton.clicked.connect(self.open_new_window_1)

    def select_radioButton(self, rb):
        state = self.sender()
        self.rtext = state.text()
        self.ltext = self.label_5.text()
        self.btnEnable()

    def select_lineEdit(self, le):
        if le is self.lineEdit:
            self.ltext_1 = le.text()
        elif le is self.lineEdit_2:
            self.ltext_2 = le.text()
        elif le is self.lineEdit_3:
            self.ltext_3 = le.text()
        elif le is self.lineEdit_4:
            self.ltext_4 = le.text()
        self.btnEnable()

    def btnEnable(self):
        if self.ltext_1 is not None and self.ltext_2 is not None and self.ltext_3 is not None \
                and self.ltext_4 is not None and self.rtext is not None:
            self.pushButton.setEnabled(True)

    def open_new_window_1(self):
        global part_name
        ts = []
        part_name = self.ltext_1
        labels = [self.label.text(), self.label_2.text(), self.label_3.text(), self.label_4.text()]
        ltexts = [self.ltext_1, self.ltext_2, self.ltext_3, self.ltext_4]
        labels = [labels[0][5:], labels[1][5:], labels[2][5:], labels[3][5:]]
        ts.append([labels[0], ltexts[0]])
        ts.append([labels[1], ltexts[1]])
        ts.append([labels[2], ltexts[2]])
        ts.append([labels[3], ltexts[3]])
        header = [ts[0][0], ts[1][0], ts[2][0], ts[3][0], self.ltext]
        detail = [ts[0][1], ts[1][1], ts[2][1], ts[3][1], self.rtext]
        with open('output/People_Score/' + self.ltext_1 + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(detail)
            file.close()
        self.window3 = MyWindow_3(self.music)
        self.window3.show()
        self.close()

class MyWindow_3(QWidget, Survey_Form):
    def __init__(self, music_name):
        super().__init__()
        self.music = music_name
        self.l_f, self.total_time, self.value = False, 0, 100
        self.ltext_1, self.ltext_2, self.ltext_3, self.ltext_4 = None, None, None, None
        self.player = QMediaPlayer(self)
        self.center()
        self.init_ui()
        self.BtnChange()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def closeEvent(self, event):
        global exit_flag, sign
        event.accept()
        if not sign:
            exit_flag = True
        else:
            exit_flag = False

    def init_ui(self):
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('调查问卷')
        self.setWindowIcon(QIcon(img_path + '/survey.ico'))
        self.pushButton_7.setIcon(QIcon(img_path + '/sound_on.png'))
        self.progressBar.setRange(0, len(musics))
        self.progressBar.setValue(len(musics) - len(musics_list))
        self.lcdNumber.display('0' + '-' + '0')
        self.media_list = musics_list
        self.listWidget.addItems([os.path.basename(m) for m in self.media_list])
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music)))
        self.player.setVolume(self.value)
        self.listWidget.hide()
        result = random.sample(range(1, 5), 4)
        self.label.setText('1、' + data[result[0] - 1][0])
        self.label_2.setText('2、' + data[result[1] - 1][0])
        self.label_3.setText('3、' + data[result[2] - 1][0])
        self.label_4.setText('4、' + data[result[3] - 1][0])
        self.comboBox.addItems(data1[result[0] - 1])
        self.comboBox_2.addItems(data1[result[1] - 1])
        self.comboBox_3.addItems(data1[result[2] - 1])
        self.comboBox_4.addItems(data1[result[3] - 1])

    def BtnChange(self):
        self.pushButton.clicked.connect(self.play)
        self.pushButton_2.clicked.connect(self.open_new_window_2)
        self.pushButton_3.clicked.connect(lambda: self.Btn_Func(self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.Btn_Func(self.pushButton_4))
        self.pushButton_5.clicked.connect(lambda: self.Btn_Func(self.pushButton_5))
        self.pushButton_6.clicked.connect(lambda: self.Btn_Func(self.pushButton_6))
        self.pushButton_7.clicked.connect(lambda: self.Btn_Func(self.pushButton_7))
        self.horizontalSlider.valueChanged.connect(self.VolumeSlider)
        self.listWidget.doubleClicked.connect(self.ListPlay)
        self.player.durationChanged.connect(self.GetDuration)
        self.player.positionChanged.connect(self.GetPosition)

    def GetDuration(self, d):
        self.total_time = d

    def GetPosition(self, p):
        left_time = int((self.total_time - p) / 1000)
        self.pushButton.setText(f'当前播放{os.path.basename(self.music)}中,倒计时{left_time}s,请仔细聆听！')
        if left_time == 0:
            self.pushButton.setText('请点击按钮播放音频文件')

    def VolumeSlider(self, value):
        self.value = value
        self.player.setVolume(value)
        self.label_5.setText(f'{value}')
        if value == 0:
            self.pushButton_7.setIcon(QIcon(img_path + '/sound_off.png'))
        else:
            self.pushButton_7.setIcon(QIcon(img_path + '/sound_on.png'))

    def ListPlay(self):
        music_index = self.listWidget.item(self.listWidget.currentRow()).text()
        self.music = music_path + f'/{music_index}'
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music)))
        self.play()

    def Btn_Func(self, btn):
        global total_time
        if btn == self.pushButton_3:
            self.pushButton_3.setIcon(QIcon(img_path + '/replay.png'))
            self.pushButton_3.setText('')
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music)))
            self.play()
            self.pushButton_4.setIcon(QIcon(''))
            self.pushButton_4.setText('暂停')
            self.pushButton_5.setIcon(QIcon(''))
            self.pushButton_5.setText('继续')
        elif btn == self.pushButton_4:
            if self.player.state() == 1:
                self.player.pause()
                self.pushButton_4.setIcon(QIcon(img_path + '/pause.png'))
                self.pushButton_4.setText('')
                self.pushButton_3.setIcon(QIcon(''))
                self.pushButton_3.setText('重播')
                self.pushButton_5.setIcon(QIcon(''))
                self.pushButton_5.setText('继续')
        elif btn == self.pushButton_5:
            if self.player.state() == 2:
                self.player.play()
                self.pushButton_5.setIcon(QIcon(img_path + '/play.png'))
                self.pushButton_5.setText('')
                self.pushButton_3.setIcon(QIcon(''))
                self.pushButton_3.setText('重播')
                self.pushButton_4.setIcon(QIcon(''))
                self.pushButton_4.setText('暂停')
        elif btn == self.pushButton_6:
            if self.listWidget.isHidden():
                self.listWidget.show()
                self.l_f = True
                self.pushButton_6.setIcon(QIcon(img_path + '/show.png'))
                self.pushButton_6.setText('')
            else:
                self.listWidget.hide()
                self.l_f = False
                self.pushButton_6.setIcon(QIcon(''))
                self.pushButton_6.setText('查看')
        elif btn == self.pushButton_7:
            if self.player.isMuted():
                self.player.setMuted(False)
                self.pushButton_7.setIcon(QIcon(img_path + '/sound_on.png'))
                self.player.setVolume(100)
                self.horizontalSlider.setValue(100)
                self.label_5.setText('100')
            else:
                self.player.setMuted(True)
                self.player.setVolume(0)
                self.horizontalSlider.setValue(0)
                self.label_5.setText('0')
                self.pushButton_7.setIcon(QIcon(img_path + '/sound_off.png'))

    def play(self):
        self.pushButton.setEnabled(False)
        self.pushButton.setText(f'当前播放{os.path.basename(self.music)}中,倒计时{0}s,请仔细聆听！')
        self.player.play()
        self.pushButton_5.setIcon(QIcon(img_path + '/play.png'))
        self.pushButton_5.setText('')
        self.lcdNumber.display(os.path.basename(self.music).split('.')[0] + '-' + f'{int(self.total_time / 1000)}')
        self.player.mediaStatusChanged.connect(self.StatusChange)
        self.comboBox.currentIndexChanged.connect(lambda: self.sle(self.comboBox))
        self.comboBox_2.currentIndexChanged.connect(lambda: self.sle(self.comboBox_2))
        self.comboBox_3.currentIndexChanged.connect(lambda: self.sle(self.comboBox_3))
        self.comboBox_4.currentIndexChanged.connect(lambda: self.sle(self.comboBox_4))

    def StatusChange(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.pushButton.setText('请点击按钮播放音频文件')
            self.pushButton.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.comboBox_3.setEnabled(True)
            self.comboBox_4.setEnabled(True)
            self.pushButton_5.setIcon(QIcon(''))
            self.pushButton_5.setText('继续')
            self.pushButton_4.setIcon(QIcon(''))
            self.pushButton_4.setText('暂停')
            self.pushButton_3.setIcon(QIcon(''))
            self.pushButton_3.setText('重播')

    def sle(self, cb):
        if cb is self.comboBox:
            self.ltext_1 = cb.currentText()
        elif cb is self.comboBox_2:
            self.ltext_2 = cb.currentText()
        elif cb is self.comboBox_3:
            self.ltext_3 = cb.currentText()
        elif cb is self.comboBox_4:
            self.ltext_4 = cb.currentText()
        if self.ltext_1 is not None and self.ltext_2 is not None and self.ltext_3 is not None and self.ltext_4 is not None:
            self.pushButton_2.setEnabled(True)

    def open_new_window_2(self):
        global part_name, header_flag, sign
        ts = []
        sign = True
        labels = [self.label.text(), self.label_2.text(), self.label_3.text(), self.label_4.text()]
        ltexts = [self.ltext_1, self.ltext_2, self.ltext_3, self.ltext_4]
        labels = [labels[0][2:], labels[1][2:], labels[2][2:], labels[3][2:]]
        ts.append([labels[i] for i in range(4) if ltexts[i] in data[0][1:]])
        ts.append([ltexts[i] for i in range(4) if ltexts[i] in data[0][1:]])
        ts.append([labels[i] for i in range(4) if ltexts[i] in data[1][1:]])
        ts.append([ltexts[i] for i in range(4) if ltexts[i] in data[1][1:]])
        ts.append([labels[i] for i in range(4) if ltexts[i] in data[2][1:]])
        ts.append([ltexts[i] for i in range(4) if ltexts[i] in data[2][1:]])
        ts.append([labels[i] for i in range(4) if ltexts[i] in data[2][1:]])
        ts.append([ltexts[i] for i in range(4) if ltexts[i] in data[2][1:]])
        header1 = [ts[0][0], ts[2][0], ts[4][0], ts[6][0], '音频名称']
        Wav_name = os.path.basename(self.music)
        detail1 = [ts[1][0], ts[3][0], ts[5][0], ts[7][0], Wav_name]
        detail2 = [ts[1][0], ts[3][0], ts[5][0], ts[7][0]]
        with open('output/People_Score/' + part_name + '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if header_flag:
                writer.writerow(header1)
                header_flag = False
            writer.writerow(detail1)
            file.close()
        with open('output/Wav_Score/' + Wav_name + '.csv', 'a', newline='') as file1:
            writer = csv.writer(file1)
            writer.writerow(detail2)
            file1.close()
        if end:
            self.w = MyWindow_4()
            self.w.show()
        self.close()

class MyWindow_4(QWidget, Suggest_Form):
    def __init__(self):
        super().__init__()
        self.center()
        self.init_ui()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def init_ui(self):
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('建议')
        self.setWindowIcon(QIcon(img_path + '/sug.ico'))
        self.textEdit.textChanged.connect(self.getText)
        self.pushButton.clicked.connect(self.closewin)

    def getText(self):
        global quit_flag
        self.sugs = self.textEdit.toPlainText()
        if self.sugs == 'end':
            quit_flag = True
        print(self.sugs, quit_flag)

    def closewin(self):
        global sug_flag, part_name, start_t
        head = ['被试者', '建议', '所用时间']
        end_t = time.time()
        times = end_t - start_t
        sugtime = [part_name, self.sugs, str(times)]
        with open('output/Suggest/' + 'suggest' + '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if sug_flag:
                writer.writerow(head)
                sug_flag = False
            writer.writerow(sugtime)
            file.close()
        self.close()

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    sug_flag, quit_flag, exit_flag, sign = True, False, False, False
    input_path = os.path.join(os.getcwd(), 'input')
    img_path = os.path.join(input_path, 'image')
    music_path = os.path.join(input_path, 'music_path')
    issue = os.path.join(input_path, 'problem', 'issue.txt')
    musics = listdir(music_path)
    with open(issue, 'r', encoding='utf-8') as infile:
        data = []
        for line in infile:
            data_line1 = line.strip("\n").split(',')  # 去除首尾换行符，并按空格划分
            for i in data_line1:
                data.append(re.split('，', i))
    data1 = []
    for i in range(len(data)):
        cb = data[i][1:]
        cb.insert(0, '请选择')
        data1.append(cb)
    # while True:
    #     if quit_flag:
    #         break
    start_t = time.time()
    part_name, header_flag, end = '', True, False
    num = random.sample(range(1, len(musics) + 1), len(musics))
    music_name = musics[num[0] - 1]
    musics_list = []
    for i in range(len(num)):
        musics_list.append(musics[num[i] - 1])
    window1 = MyWindow_1(music_name)
    window1.show()
    app.exec()
    musics_list.pop(0)
    for i in range(len(num) - 1):
        if exit_flag:
            app = QApplication.instance()
            app.quit()
            break
        if i == len(num) - 2:
            end = True
        sign = False
        music_name = musics[num[i + 1] - 1]
        window2 = MyWindow_3(music_name)
        window2.show()
        app.exec()
        musics_list.pop(0)




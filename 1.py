import sys, sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTableWidgetItem, QComboBox, QTableWidget
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(473, 272)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 20, 151, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.SearchBT = QtWidgets.QPushButton(self.centralwidget)
        self.SearchBT.setGeometry(QtCore.QRect(390, 20, 75, 23))
        self.SearchBT.setObjectName("SearchBT")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(180, 20, 201, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 47, 13))
        self.label_5.setObjectName("label_5")
        self.ErrorLable = QtWidgets.QLabel(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 473, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Название"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Год выпуска"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Продолжительность"))
        self.SearchBT.setText(_translate("MainWindow", "Поиск"))


class Find(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.SearchBT.clicked.connect(self.run)
        self.ErrorLable.resize(100, 30)

    def run(self):
        try:
            if self.comboBox.currentText() != 'Название':
                int(self.lineEdit.text())
        except Exception:
            self.ErrorLable.setText('Ошибка ввода')
        else:
            con = sqlite3.connect('films_db.sqlite')
            cur = con.cursor()

            if self.comboBox.currentText() == 'Название':
                result = cur.execute("""SELECT DISTINCT * FROM films WHERE title = ?""",
                                     (self.lineEdit.text(),)).fetchall()
            elif self.comboBox.currentText() == 'Год выпуска':
                result = cur.execute("""SELECT DISTINCT * FROM films WHERE year = ?""",
                                     (int(self.lineEdit.text()),)).fetchall()
            elif self.comboBox.currentText() == 'Продолжительность':
                result = cur.execute("""SELECT DISTINCT * FROM films WHERE duration = ?""",
                                     (int(self.lineEdit.text()),)).fetchall()
            names = [i[0] for i in cur.description]
            ex.load_table(result, names)
            con.close()


class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Фильмотека')

        self.btn = QPushButton('добавить', self)
        self.btn.resize(100, 20)
        self.btn.move(0, 0)

        self.btn2 = QPushButton('искать', self)
        self.btn2.resize(100, 20)
        self.btn2.move(110, 0)

        self.btn.clicked.connect(self.open_second_form)
        self.btn2.clicked.connect(self.open_find)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(5, 50)
        self.tableWidget.resize(800, 300)
        self.load_table()

    def load_table(self, table=None, name=None):
        con = sqlite3.connect('films_db.sqlite')
        cur = con.cursor()
        if not table:
            result = cur.execute("""SELECT * FROM films""").fetchall()
            films = result
            names = [i[0] for i in cur.description]
        else:
            films = table
            names = name
        res = cur.execute("""SELECT * FROM genres""").fetchall()
        genres = {}
        for i in res:
            genres[i[0]] = i[1]
        self.tableWidget.setColumnCount(len(names))
        self.tableWidget.setHorizontalHeaderLabels(names)
        self.tableWidget.setRowCount(0)
        for index, i in enumerate(films):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            i = list(i)
            i[3] = genres.get(i[3])
            for j, elem in enumerate(i):
                self.tableWidget.setItem(index, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        con.close()

    def open_second_form(self):
        self.second_form = SecondForm()
        self.second_form.show()

    def open_find(self):
        self.find = Find()
        self.find.show()

class SecondForm(QWidget):
    def __init__(self):
        con = sqlite3.connect('films_db.sqlite')
        super().__init__()
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Добавить')
        y = 20
        for i in range(4):
            self.label = QLabel(['Name', 'Year', 'Genre', 'Duration'][i], self)
            self.label.move(20, y)
            y += 30
        self.Name = QLineEdit(self)
        self.Name.move(120, 20)
        self.Year = QLineEdit(self)
        self.Year.move(120, 45)
        self.Duration = QLineEdit(self)
        self.Genres = QComboBox(self)
        self.Genres.move(120, 70)
        self.Duration.move(120, 100)
        cur = con.cursor()
        self.genres = cur.execute("""SELECT DISTINCT title FROM genres""").fetchall()
        con.close()
        self.Genres.addItems([i[0] for i in self.genres])
        self.Run = QPushButton('Добавить', self)
        self.Run.move(200, 300)
        self.Run.clicked.connect(self.run)
        self.a = QLabel(self)
        self.a.move(100, 350)
        self.a.resize(200, 40)
        self.info = []
        self.info.append(self.Name)
        self.info.append(self.Year)
        self.info.append(self.Duration)

    def run(self):
        try:
            if not all([i.text() for i in self.info]):
                raise ValueError
            elif int(self.Year.text()) > 2020:
                raise ValueError
            elif int(self.Duration.text()) <= 0:
                raise ValueError
        except Exception:
            self.a.setText('Неверный формат данных')
        else:
            global ex
            con = sqlite3.connect('films_db.sqlite')
            cur = con.cursor()
            a = cur.execute("""SELECT id FROM films""").fetchall()
            a = a[-1][0]
            genre = cur.execute("""SELECT id FROM genres WHERE title = ?""", (self.Genres.currentText(),)).fetchall()
            info = (a + 1, self.Name.text(), int(self.Year.text()),
                    genre[0][0], int(self.Duration.text()))
            cur.execute("""INSERT INTO films VALUES(?, ?, ?, ?, ?)""", info)
            con.commit()
            ex.load_table()
            con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())
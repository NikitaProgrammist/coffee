import sys

import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QAbstractItemView


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.adding)
        self.pushButton_2.clicked.connect(self.rewrite)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.loadTable()

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT * from coffee""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for t, el in enumerate(row):
                self.tableWidget.setItem(i, t, QTableWidgetItem(str(el)))
        self.tableWidget.resizeColumnsToContents()

    def adding(self):
        self.edit_film_widget = CoffeeDialog(self)
        if self.edit_film_widget.exec_() == QDialog.Accepted:
            con = sqlite3.connect('coffee.sqlite')
            cursor = con.cursor()
            cursor.execute(f"""INSERT INTO coffee (name, exp, molot, description, price, volume) 
                                VALUES('{self.edit_film_widget.name.text()}', '{self.edit_film_widget.exp.text()}', 
            '{self.edit_film_widget.molot.text()}', '{self.edit_film_widget.description.toPlainText()}', 
            '{self.edit_film_widget.price.text()}', '{self.edit_film_widget.volume.text()}')""")
            con.commit()
        self.loadTable()

    def rewrite(self):
        row = [self.tableWidget.item(self.tableWidget.selectionModel().currentIndex().row(), i).text() for i in range(7)]
        self.edit_film_widget = CoffeeDialog(self)
        self.edit_film_widget.name.setText(row[1])
        self.edit_film_widget.exp.setText(row[2])
        self.edit_film_widget.molot.setText(row[3])
        self.edit_film_widget.description.setPlainText(row[4])
        self.edit_film_widget.price.setText(row[5])
        self.edit_film_widget.volume.setText(row[6])
        if self.edit_film_widget.exec_() == QDialog.Accepted:
            con = sqlite3.connect('coffee.sqlite')
            cursor = con.cursor()
            cursor.execute(f"""REPLACE INTO coffee (id, name, exp, molot, description, price, volume) 
                                VALUES({row[0]}, '{self.edit_film_widget.name.text()}', 
            '{self.edit_film_widget.exp.text()}', '{self.edit_film_widget.molot.text()}', 
            '{self.edit_film_widget.description.toPlainText()}', '{self.edit_film_widget.price.text()}', 
            '{self.edit_film_widget.volume.text()}')""")
            con.commit()
        self.loadTable()


class CoffeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
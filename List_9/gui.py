from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QFont

import sys
import database

database.create_base()


class Database_GUI(QMainWindow):

    def __init__(self):
        super(Database_GUI, self).__init__()
        self.button_height = 70
        self.button_width = 120
        self.k = self.button_width + 80

        self.font = QFont('TimesNewRoman', 13)

        self.setGeometry(200, 200, 8 * self.button_width, 9 * self.button_height - 10)
        self.setWindowTitle("")
        self.initUI()

    def initUI(self):
        self.search_button = QtWidgets.QPushButton(self)
        self.search_button.setText("Search")
        self.search_button.setGeometry(50, 0, self.button_width, self.button_height)
        self.search_button.setFont(QFont('TimesNewRoman', 16))
        self.search_button.clicked.connect(lambda: self.search_value())

        self.search_box = QLineEdit(self)
        self.search_box.move(0, self.button_height)
        self.search_box.setFont(QFont('TimesNewRoman', 16))
        self.search_box.setMaxLength(49)
        self.search_box.resize(2 * self.button_width, self.button_height)

        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setText("Title: ")
        self.title_label.move(0, 3 * self.button_height + 30)
        self.title_label.setFont(QFont('TimesNewRoman', 16))

        self.title_box = QLineEdit(self)
        self.title_box.move(0, 4 * self.button_height)
        self.title_box.setFont(QFont('TimesNewRoman', 16))
        self.title_box.setMaxLength(49)
        self.title_box.resize(self.button_width + 50, self.button_height)

        self.author_label = QtWidgets.QLabel(self)
        self.author_label.setText("Author: ")
        self.author_label.move(self.button_width + 50, 3 * self.button_height + 30)
        self.author_label.setFont(QFont('TimesNewRoman', 16))

        self.author_box = QLineEdit(self)
        self.author_box.move(self.button_width + 50, 4 * self.button_height)
        self.author_box.setFont(QFont('TimesNewRoman', 16))
        self.author_box.setMaxLength(49)
        self.author_box.resize(self.button_width + 50, self.button_height)

        self.pub_year_label = QtWidgets.QLabel(self)
        self.pub_year_label.setText("Pub year: ")
        self.pub_year_label.move(2 * self.button_width + 100, 3 * self.button_height + 30)
        self.pub_year_label.setFont(QFont('TimesNewRoman', 16))

        self.pub_year_box = QLineEdit(self)
        self.pub_year_box.move(2 * self.button_width + 100, 4 * self.button_height)
        self.pub_year_box.setFont(QFont('TimesNewRoman', 16))
        self.pub_year_box.setMaxLength(49)
        self.pub_year_box.resize(self.button_width, self.button_height)

        self.is_borrowed_label = QtWidgets.QLabel(self)
        self.is_borrowed_label.setText("Is borrowed: ")
        self.is_borrowed_label.move(3 * self.button_width + 100, 3 * self.button_height + 30)
        self.is_borrowed_label.resize(120, 30)
        self.is_borrowed_label.setFont(QFont('TimesNewRoman', 16))

        self.is_borrowed_box = QLineEdit(self)
        self.is_borrowed_box.move(3 * self.button_width + 100, 4 * self.button_height)
        self.is_borrowed_box.setFont(QFont('TimesNewRoman', 16))
        self.is_borrowed_box.setMaxLength(49)
        self.is_borrowed_box.resize(self.button_width, self.button_height)

        self.edit_button = QtWidgets.QPushButton(self)
        self.edit_button.setText("Edit")
        self.edit_button.setFont(QFont('TimesNewRoman', 16))
        self.edit_button.setGeometry(self.button_width, 5 * self.button_height + 20, self.button_width,
                                     self.button_height)

        self.edit_button.clicked.connect(lambda: self.edit_book())
        self.add_new_button = QtWidgets.QPushButton(self)
        self.add_new_button.setText("Add new")
        self.add_new_button.setFont(QFont('TimesNewRoman', 16))
        self.add_new_button.setGeometry(2 * self.button_width, 5 * self.button_height + 20, self.button_width,
                                        self.button_height)
        self.add_new_button.clicked.connect(lambda: self.add_new_book())

        self.is_borrowed_label = QtWidgets.QLabel(self)
        self.is_borrowed_label.setText("Books list: ")
        self.is_borrowed_label.move(5 * self.button_width, 0)
        self.is_borrowed_label.resize(120, 30)
        self.is_borrowed_label.setFont(QFont('TimesNewRoman', 16))

        self.search_label = QtWidgets.QLabel(self)
        self.search_label.setText("Search results:  ")
        self.search_label.move(3 * self.button_width, 0)
        self.search_label.resize(160, 30)
        self.search_label.setFont(QFont('TimesNewRoman', 16))

        self.search_list = QtWidgets.QComboBox(self)
        self.search_list.move(3 * self.button_width, 40)
        self.search_list.resize(230, 30)
        self.search_list.addItem("")

        self.book_list = QtWidgets.QComboBox(self)
        self.book_list.move(5 * self.button_width, 40)
        self.book_list.resize(300, 30)
        self.book_list.addItem("")
        for book in database.return_book_list():
            self.book_list.addItem('{},{},{}'.format(book[0], book[1], book[2]))
        self.book_list.currentIndexChanged.connect(lambda: self.choose_element())

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setText("Delete")
        self.delete_button.setFont(QFont('TimesNewRoman', 16))
        self.delete_button.setGeometry(3 * self.button_width, 5 * self.button_height + 20, self.button_width,
                                       self.button_height)
        self.delete_button.clicked.connect(lambda: self.delete_book())
        self.show()

    def choose_element(self):
        if self.book_list.currentIndex() == 0:
            return
        list_element = self.book_list.currentText().split(',')
        self.title_box.setText(list_element[0])
        self.author_box.setText(list_element[1])
        self.pub_year_box.setText(list_element[2])
        self.is_borrowed_box.setText(str(database.select_by_borrow(list_element[0], list_element[1])))

    def edit_book(self):
        if self.book_list.currentIndex() == 0:
            return
        new_title = self.title_box.text()
        new_author = self.author_box.text()
        new_pub_year = self.pub_year_box.text()
        new_borrowed = self.is_borrowed_box.text()
        if new_borrowed == 'True' or new_borrowed == 'true':
            new_borrowed = True
        else:
            new_borrowed = False

        old_data = self.book_list.currentText().split(',')[0]
        index = self.book_list.currentIndex()
        self.book_list.setItemText(index, '{},{},{}'.format(new_title, new_author, new_pub_year))

        try:
            database.update_record(old_data, new_title, new_author, new_pub_year, new_borrowed)

        except Exception as e:
            return e

    def add_new_book(self):

        new_title = self.title_box.text()
        new_author = self.author_box.text()
        new_pub_year = self.pub_year_box.text()
        new_borrowed = self.is_borrowed_box.text()
        if new_borrowed == 'True' or new_borrowed == 'true':
            new_borrowed = True
        else:
            new_borrowed = False

        self.book_list.addItem('{},{},{}'.format(new_title, new_author, new_pub_year))
        database.add_new_book(new_title, new_author, new_pub_year, new_borrowed)

    def delete_book(self):
        title = self.title_box.text()
        database.delete_book(title)
        self.book_list.removeItem(self.book_list.currentIndex())

    def search_value(self):
        search_value = self.search_box.text()
        book_list = database.search_database(search_value)

        self.search_list.clear()

        for book in book_list:
            self.search_list.addItem('{},{},{}'.format(book[0], book[1], book[2]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Database_GUI()
    sys.exit(app.exec_())

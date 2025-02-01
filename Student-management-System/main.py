# Importing the req libs

import sqlite3
import sys
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QComboBox
, QPushButton, QLabel, QWidget, QToolBar, QStatusBar, QGridLayout, QMessageBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student DataBase Management System")
        self.setMinimumSize(QSize(640,480))
        # self.controls = QWidget(self)

        # adding the menu bar
        file_menu_bar = self.menuBar().addMenu("&File")
        edit_menu_bar = self.menuBar().addMenu("&Edit")
        help_menu_bar = self.menuBar().addMenu("&Help")

        #creating sub-menu items
        add_student_action = QAction(QIcon("icons/add.png"), "Add student", self)
        file_menu_bar.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        help_student_action = QAction("About",self)
        help_menu_bar.addAction(help_student_action)
        help_student_action.triggered.connect(self.about)

        edit_menu_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_bar.addAction(edit_menu_action)
        edit_menu_action.triggered.connect(self.search_student_name)


        # Creating tabular data
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels(["ID","NAME","COURSE","CONTACT"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 250)
        self.table.verticalHeader().setVisible(False)

        # Search bar.
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Student Name to search...")
        self.searchbar.textChanged.connect(self.search_update)

        # Creating a toolbar
        tool_bar = QToolBar()
        tool_bar.setMovable(True)
        self.addToolBar(tool_bar)
        tool_bar.addAction(add_student_action)
        tool_bar.addAction(edit_menu_action)

        # Create status bar and status elements.
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Detect cursor click
        self.table.cellClicked.connect(self.cell_clicked)

        # Creating an additional widget and adding to the main window.
        container = QWidget(self)
        containerLayout = QVBoxLayout()

        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.table)


        container.setLayout(containerLayout)
        self.setCentralWidget(container)

    def about(self):
        """ Connected to about action widget. Creating a dialog box """
        dialog = AboutDialog()
        dialog.exec()

    def cell_clicked(self):
        """ For editing and deleting record on selection """
        edit_record_button = QPushButton("Edit Selected Record")
        edit_record_button.clicked.connect(self.edit_record)

        del_record_button = QPushButton("Delete Selected Record")
        del_record_button.clicked.connect(self.del_record)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)
        self.status_bar.addWidget(edit_record_button)
        self.status_bar.addWidget(del_record_button)

    def edit_record(self):
        """ Calling the edit record class and executing it. """
        dialog = EditRecord()
        dialog.exec()

    def del_record(self):
        dialog = DeleteRecord()
        dialog.exec()

    def load_data(self):
        """ Method to load the data after any modification and when the program is run. """
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table.setItem(row_num,col_num,QTableWidgetItem(str(col_data)))

        connection.close()

    def search_update(self):
        """ Method to search for records based on parameters. """
        # Create search functionality
        name = self.searchbar.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_student_name(self):
        search = EditBar()
        search.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Window")
        self.setMinimumSize(200,200)
        self.setText("Application showing fake student data from a SQLITE database in a structured form in python"
                        " with additional editing and deletion capabilities. ")


class EditRecord(QDialog):
    """ Creates a separate window for editing records """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300,300))
        self.setWindowTitle("Edit Selected Record")
        layout = QVBoxLayout()

        #Getting the row,col of the selected cell
        index = window.table.currentRow()
        self.student_id = window.table.item(index,0).text()
        student_name = window.table.item(index,1).text()
        course_name = window.table.item(index, 2).text()
        contact_edit = window.table.item(index, 3).text()

        # Add a student edit label
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name...")
        layout.addWidget(self.student_name)

        # Adding the combo box
        label = QLabel("Course to choose ")
        self.course = QComboBox()
        self.course.addItems(["Math","Astronomy","Physics","Biology"])
        self.course.setCurrentText(course_name)
        layout.addWidget(label)
        layout.addWidget(self.course)

        # Editing contact number
        self.contact_number = QLineEdit(contact_edit)
        self.contact_number.setPlaceholderText("Mobile ")
        layout.addWidget(self.contact_number)


        # Add edited record
        button = QPushButton("Edit Record")
        button.clicked.connect(self.update_student_record)
        layout.addWidget(button)

        layout.addStretch(0)
        self.setLayout(layout)


    def update_student_record(self):
        """ Updating the student records, in new window. """
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ? "
                       ,(self.student_name.text(),self.course.itemText(self.course.currentIndex())
                         ,self.contact_number.text(),self.student_id))
        connection.commit()
        connection.close()
        window.load_data()


class DeleteRecord(QDialog):
    """ Delete records as selected. """
    def __init__(self):
        super().__init__()
        self.setMinimumSize(150, 100)
        self.setWindowTitle("Delete Record")

        layout = QGridLayout()
        confirmation = QLabel("Confirm to delete.")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        index = window.table.currentRow()
        self.name_to_delete = window.table.item(index,1).text()
        yes.clicked.connect(self.del_records)
        no.clicked.connect(self.no_close_window)


        layout.addWidget(confirmation,0,0,1,2)
        layout.addWidget(yes,1,0)
        layout.addWidget(no,1,1)

        self.setLayout(layout)

    def del_records(self):
        """ Deletes selected records and closes window after deletion. """
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE name = ?"
                                    ,(self.name_to_delete,))
        connection.commit()
        connection.close()
        confirmation = QMessageBox.question(self, "Record deleted successfully.", "Would you like to delete more records?"
                                            , QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.No:
            self.close()  # Close the app

        window.load_data()

    def no_close_window(self):
        """ Closes the window when "no" is selected """
        self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(QSize(300,300))

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name ")
        layout.addWidget(self.student_name)

        label = QLabel("Course to choose ")
        self.course = QComboBox()
        self.course.addItems(["Math","Astronomy","Physics","Biology"])
        layout.addWidget(label)
        layout.addWidget(self.course)

        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Mobile ")
        layout.addWidget(self.contact_number)

        # Submit button to search by name.
        submit_button = QPushButton("Submit Record",self)
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        layout.addStretch(0)
        layout.setContentsMargins(10, 0, 10, 0)

        window.load_data()
        self.setLayout(layout)


    def add_student(self):
        """ Inserting row based on name, course and contact number. """
        name = self.student_name.text()
        course = self.course.itemText(self.course.currentIndex())
        contact = self.contact_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor().execute("INSERT INTO students (name,course,mobile) VALUES (?,?,?)",
                                             (name,course,contact))
        connection.commit()
        cursor.close()
        connection.close()


class EditBar(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Search")
        self.setMinimumSize(QSize(300, 300))

        layout = QVBoxLayout()

        # Search bar.
        self.search_student_id = QLineEdit()
        self.search_student_id.setPlaceholderText("Student ID... ")
        layout.addWidget(self.search_student_id)

        self.search_student_course = QLineEdit()
        self.search_student_course.setPlaceholderText("Course registered ... ")
        layout.addWidget(self.search_student_course)

        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.search_student)

        layout.addStretch(0)
        layout.addWidget(search_button)
        self.setLayout(layout)

    def search_student(self):
        """ Match id of student for searching records instead of name. """

        id = self.search_student_id.text()
        course = self.search_student_course.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ? OR course = ?",(id,course))
        items = window.table.findItems(id, Qt.MatchFlag.MatchExactly)
        item_course = window.table.findItems(course, Qt.MatchFlag.MatchExactly)
        for item in items:
            window.table.item(item.row(),0).setSelected(True)
        for sel in item_course:
            window.table.item(sel.row(), 2).setSelected(True)
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.load_data()
    window.show()

    #Start the event loop
    app.exec()
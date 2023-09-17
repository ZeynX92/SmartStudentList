from PyQt5 import uic, QtWidgets
from data import db_session
from data.students import Student
from PyQt5.QtWidgets import QWidget
from sqlalchemy import and_


class AddStudentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        uic.loadUi('ui/student.ui', self)

        db_name = "students.db"
        db_session.global_init(f"db/{db_name}")

        self.warn = None

        self.save.clicked.connect(self.save_pr)
        self.cancel.clicked.connect(self.cancel_pr)

        self.delete_2.setVisible(False)

    def save_pr(self):
        surname = self.lineEdit.text()
        name = self.lineEdit_2.text()
        lastname = self.lineEdit_3.text()
        telephone_number = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        note = self.lineEdit_6.text()

        db_sess = db_session.create_session()

        if db_sess.query(Student).filter(
                and_(Student.surname == surname, Student.name == name, Student.lastname == lastname)).first():
            self.warn = Warn("Такой ученик уже есть")
            self.warn.show()
        else:

            student = Student()
            if name and surname and lastname:
                student.name = name
                student.surname = surname
                student.lastname = lastname
                student.telephone_number = telephone_number if telephone_number else "Номер отсутствует..."
                student.email = email if email else 'E-mail отсутствует...'
                student.note = note if note else 'Заметка отсутствует...'

                db_sess.add(student)
                db_sess.commit()

                self.parent.setEnabled(True)
                self.parent.search_student()
                self.hide()
            else:
                self.warn = Warn("Форма заполнена неверно!")
                self.warn.show()

    def cancel_pr(self):
        self.parent.setEnabled(True)
        self.hide()

    def closeEvent(self, event):
        self.cancel_pr()


class EditStudentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('ui/student.ui', self)

        self.db_sess = db_session.create_session()

        self.student = self.db_sess.query(Student).filter(and_(Student.surname == str(
            parent.tableWidget.item(parent.tableWidget.currentRow(), 0).text()), Student.name == str(
            parent.tableWidget.item(parent.tableWidget.currentRow(), 1).text()), Student.lastname == str(
            parent.tableWidget.item(parent.tableWidget.currentRow(), 2).text()))).first()

        self.lineEdit.setText(self.student.surname)
        self.lineEdit_2.setText(self.student.name)
        self.lineEdit_3.setText(self.student.lastname)
        self.lineEdit_4.setText(self.student.telephone_number)
        self.lineEdit_5.setText(self.student.email)
        self.lineEdit_6.setText(self.student.note)

        self.warn = None

        self.save.clicked.connect(self.save_pr)
        self.cancel.clicked.connect(self.cancel_pr)
        self.delete_2.clicked.connect(self.delete)

    def delete(self):
        self.db_sess.delete(self.student)
        self.db_sess.commit()

        self.parent.setEnabled(True)
        self.parent.search_student()
        self.hide()

    def save_pr(self):
        surname = self.lineEdit.text()
        name = self.lineEdit_2.text()
        lastname = self.lineEdit_3.text()
        telephone_number = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        note = self.lineEdit_6.text()

        if name and surname and lastname:
            self.student.name = name
            self.student.surname = surname
            self.student.lastname = lastname
            self.student.telephone_number = telephone_number if telephone_number else "Номер отсутствует..."
            self.student.email = email if email else 'E-mail отсутствует...'
            self.student.note = note if note else 'Заметка отсутствует...'

            self.db_sess.commit()

            self.parent.setEnabled(True)
            self.parent.search_student()
            self.hide()
        else:
            self.warn = Warn("Форма заполнена неверно!")
            self.warn.show()

    def cancel_pr(self):
        self.parent.setEnabled(True)
        self.hide()

    def closeEvent(self, event):
        self.cancel_pr()


class Warn(QWidget):
    def __init__(self, warn_text: str):
        super().__init__()
        uic.loadUi('ui/warning.ui', self)

        self.label_2.setText(warn_text)

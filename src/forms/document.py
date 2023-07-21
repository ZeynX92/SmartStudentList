from PyQt5 import uic, QtWidgets
from data import db_session
from data.documents import Document
from PyQt5.QtWidgets import QWidget, QFileDialog
import os
import shutil
import sys


class AddDocumentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        uic.loadUi('ui/document.ui', self)

        db_name = "students.db"
        db_session.global_init(f"db/{db_name}")

        self.warn = None
        self.file_name = None

        self.save.clicked.connect(self.save_pr)
        self.select.clicked.connect(self.select_pr)
        self.cancel.clicked.connect(self.cancel_pr)

        self.delete_2.setVisible(False)

    def select_pr(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'All Files (*);')[0]
        shutil.move(self.file_name,
                    os.path.join(os.path.split(os.path.realpath(sys.argv[0]))[0], "documents"))

        self.lineEdit.setText(self.file_name.split('\\')[-1])

    def save_pr(self):
        title = self.lineEdit.text().split('/')[-1]
        description = self.lineEdit_6.text()
        db_sess = db_session.create_session()

        doc = Document()
        if title:
            doc.title = title
            doc.description = description if description else 'Заметка отсутствует...'

            db_sess.add(doc)
            db_sess.commit()

            self.parent.setEnabled(True)
            self.parent.search_document()
            self.hide()
        else:
            self.warn = Warn("Форма заполнена неверно!")
            self.warn.show()

    def cancel_pr(self):
        self.parent.setEnabled(True)
        self.hide()

    def closeEvent(self, event):
        self.cancel_pr()


class EditDocumentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('ui/document.ui', self)

        self.db_sess = db_session.create_session()

        self.doc = self.db_sess.query(Document).filter(Document.title == str(
            parent.tableWidget_1.item(parent.tableWidget_1.currentRow(), 0).text()) and Document.description == str(
            parent.tableWidget_1.item(parent.tableWidget_1.currentRow(), 1).text())).first()

        self.lineEdit.setText(self.doc.title)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_6.setText(self.doc.description)

        self.warn = None

        self.save.clicked.connect(self.save_pr)
        self.cancel.clicked.connect(self.cancel_pr)

        self.select.clicked.connect(self.save_file)
        self.select.setText("Выгрузить")

        self.delete_2.clicked.connect(self.delete)

    def delete(self):
        self.db_sess.delete(self.doc)
        self.db_sess.commit()

        # TODO: Удаления файла из ./documents

        self.parent.setEnabled(True)
        self.parent.search_document()
        self.hide()

    def save_file(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")

        shutil.copyfile(f"documents/{self.doc.title}",
                        os.path.join(path, f"{self.doc.title}"))

    def save_pr(self):
        description = self.lineEdit_6.text()

        self.doc.description = description if description else 'Заметка отсутствует...'

        self.db_sess.commit()

        self.parent.setEnabled(True)
        self.parent.search_document()
        self.hide()

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

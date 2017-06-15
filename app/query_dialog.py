from PyQt4 import QtGui, QtCore
import pandas as pd
import csv
import os

from StyleSheets import group_box_style, run_button_style
from paramSqlTotranSql import data_mapping
from database_file import check_existing_tables


class QueryWindow(QtGui.QWidget):
    def __init__(self, parent=None, fields=None, desc=None, tablelist=None):
        super(QueryWindow, self).__init__(parent)
        self.tableList = tablelist
        self.fields = fields
        self.desc = desc
        self.text_fields = []

        self.setFixedHeight(500)
        self.setFixedWidth(800)
        self.setWindowTitle("QryBots")
        self.setWindowIcon(QtGui.QIcon("querybots.png"))

        self.group = QtGui.QGroupBox('Description: %s' % self.desc)
        group_box_style(self.group)

        self.form = QtGui.QFormLayout()
        self.save_form = QtGui.QFormLayout()
        self.horizontal = QtGui.QHBoxLayout()
        self.save_horizontal = QtGui.QHBoxLayout()
        self.horizontal_run = QtGui.QHBoxLayout()

        for index, value in self.fields.iterrows():
            self.label = QtGui.QLabel(index)
            if any(i == 'date' for i in value):
                exec ('self.textEdit' + index + ' = QtGui.QDateEdit(QtCore.QDate.currentDate().addDays(-1))')
                exec ('self.textEdit' + index + '.setCalendarPopup(True)')
                exec ('self.textEdit' + index + '.setFixedWidth(100)')

            elif any(i == 'csv' for i in value):
                self.upload = QtGui.QPushButton("Upload Codes", self)
                self.upload.setIcon(QtGui.QIcon("upload.ico"))
                self.upload.move(250, 150)
                self.upload.setFixedWidth(100)
                exec ('self.textEdit' + index + ' = QtGui.QHBoxLayout()')
                exec 'self.csv_upload = QtGui.QLineEdit()'
                exec 'self.csv_upload.setReadOnly(True)'
                exec ('self.textEdit' + index + '.addWidget(self.csv_upload)')
                exec ('self.textEdit' + index + '.addWidget(self.upload)')
                self.connect(self.upload, QtCore.SIGNAL("clicked()"), self.upload_codes)

            else:
                exec ('self.textEdit' + index + ' = QtGui.QLineEdit()')

            exec ('self.form.addRow(self.label, self.textEdit' + index + ')')

        self.save_to_label = QtGui.QLabel('Save to: ')
        self.save_to_text = QtGui.QLineEdit()
        self.save_to_text.setReadOnly(True)
        self.save_to = QtGui.QPushButton("Browse", self)
        self.save_to.setIcon(QtGui.QIcon("browse.png"))
        self.save_to.move(250, 150)
        self.save_to.setFixedWidth(100)

        self.save_horizontal.addWidget(self.save_to_text)
        self.save_horizontal.addWidget(self.save_to)

        self.save_form.addRow(self.save_to_label, self.save_horizontal)

        self.run_button = QtGui.QPushButton("Run")
        self.run_button.setFixedWidth(200)
        self.run_button.setGeometry(50, 100, 100, 0)
        self.run_button.setIcon(QtGui.QIcon("run.png"))
        # self.run_button.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        run_button_style(self.run_button)

        self.horizontal_run.addWidget(self.run_button)
        self.horizontal_run.setAlignment(QtCore.Qt.AlignJustify)
        self.vbox = QtGui.QVBoxLayout()
        self.vertical1 = QtGui.QVBoxLayout()
        self.vertical = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.form)
        self.vertical1.addLayout(self.save_form)
        self.vertical1.addLayout(self.horizontal_run)
        self.group.setLayout(self.vbox)
        self.vertical.addWidget(self.group)
        self.vertical.addLayout(self.vertical1)
        self.setLayout(self.vertical)

        self.connect(self.save_to, QtCore.SIGNAL("clicked()"), self.download)
        self.connect(self.run_button, QtCore.SIGNAL("clicked()"), self.display)

    def upload_codes(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', "", 'All Files(*.*);; Csv Files(*.csv);; '
                                                                            'Txt Files(*.txt)')
        try:
            content = open(filename, 'r')
            self.csv_upload.setText(filename)
            self.line = content.readlines()[1:]
            content.close()
        except IOError:
            message = QtGui.QMessageBox(self)
            message.setText("Oops ! You Forgot to insert ICD Codes File.")
            message.setIcon(QtGui.QMessageBox.Critical)
            message.exec_()

    def download(self):
        f = QtGui.QFileDialog(self)
        # f.directory()
        filename = QtGui.QFileDialog.getExistingDirectory(f)

        # for i in ['Eliezer', 'Enosh', 'Elis']:
        #     filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', str(i)+'.csv',
        #                                                  'Csv files(*.csv);; All Files(*.*)')
        #     print filename
        #     # self.save_to_text.setText(filename)
        #
        # --------------------This is Just a dummy Data-------------------------------
        with open('YHOO.csv', 'rb') as f:
            data = list(csv.reader(f))
        # ------------------------------------------------------------------------------------
        #
        for i in ['Eliezer', 'Dajie', 'Luis']:
            with open(str(os.path.join(str(filename), i)) + '.csv', "wb") as f:
                writer = csv.writer(f)
                writer.writerows(data)

    def display(self):
        lst = []
        codes = []

        for index, value in self.fields.iterrows():
            if value.Type == 'date':
                exec ('self.date' + index + ' = self.textEdit' + index + '.date()')
                # lst.append(eval('self.date' + index + '.toPyDate()'))
                mydate = eval('self.date' + index + '.toPyDate()')
                lst.append(str(mydate))

            elif value.Type == 'csv':
                try:
                    print eval('self.csv_upload.text()')
                    for i in self.line:
                        codes.append(i.strip('\n'))

                except:
                    pass

            elif value.Type == 'int':
                try:
                    number = int(eval('self.textEdit' + index + '.text()'))
                    if type(number) == int:
                        lst.append(number)

                except ValueError:
                    QtGui.QMessageBox.about(self, 'Error',
                                            'Insert only numbers for "{0}"'.format(str(index).upper()))
                    lst.append("")
                    # print eval('self.textEdit' + index + '.text()')
                    #
                    # if value.Id == '3':
                    #     try:
                    #         number = int(eval('self.textEdit' + index + '.text()'))
                    #         if type(number) == int:
                    #             print number
                    #
                    #     except ValueError:
                    #         QtGui.QMessageBox.about(self, 'Error',
                    #                                 'Insert only numbers for "{0}"'.format(str(index).upper()))

            else:
                id = eval('self.textEdit' + index + '.text()')

                lst.append(id)

        data_mapping(lst)

        for index, value in self.fields.iterrows():
            if index == 'id':
                id = eval('self.textEdit' + index + '.text()')
                check_existing_tables(tables=self.tableList, codes=codes, id=id)


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    widget = QueryWindow()
    widget.show()
    sys.exit(app.exec_())

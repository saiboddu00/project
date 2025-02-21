import sys
sys.path.append(".")
sys.path.append(r"D:\Main project-2\automatic-classroom-attendance-system-master")
import os
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QHeaderView, QMessageBox, QFileDialog, QPushButton
from PyQt5.QtCore import QModelIndex
from PyQt5 import QtGui
from PyQt5 import uic
import pandas as pd
import numpy as np
import pdfkit
from App.utils import config
from App.widgets.face_recognizer_widget import FaceRecognizerWidget

class ViewAttendance(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(r"D:\Main project-2\automatic-classroom-attendance-system-master\App\ui\viewAttendance.ui", self)

        self.filterComboBox.activated[str].connect(self.filter)
        self.searchBtn.clicked.connect(self.search)
        self.saveAsPdfBtn.clicked.connect(self.saveAsPdf)
        self.backBtn.clicked.connect(self.back)

        self.attendance = config.ATTENDANCE_PATH

        self.df = pd.read_csv(r"D:\Main project-2\automatic-classroom-attendance-system-master\output\attendance.csv", index_col=0)
        self.displayTable()
        # Initialize faceCounter based on DataFrame
        self.faceCounter = {name: 0 for name in self.df["names"]}

        # Create a button to clear data
        self.clearDataBtn = QPushButton("Clear Data", self)
        self.clearDataBtn.clicked.connect(self.clearData)  # Connect clearData method to button click

    def search(self):
        self.df = pd.read_csv(self.attendance, index_col=0)
        if self.searchText.text() == "":
            self.showDialog(icon=QMessageBox.Warning,
                            displayText="Enter student fullname", windowTitle="Search Name")
        else:
            name = self.searchText.text().replace(" ", "_")
            self.df = self.df[self.df["names"] == name]
            if len(self.df) == 0:
                self.showDialog(icon=QMessageBox.Warning, displayText="student with the name {} is not registered".format(
                    name), windowTitle="Search Name")
            else:
                self.displayTable()

    def filter(self, selected):
        self.df = pd.read_csv(self.attendance, index_col=0)
        if selected == "Good":
            attend_frac = self.df.sum(axis=1)/self.df.count(axis=1, numeric_only=True)
            self.df = self.df[attend_frac >= 0.9]
        elif selected == "Warning":
            attend_frac = self.df.sum(axis=1)/self.df.count(axis=1, numeric_only=True)
            self.df =  self.df[(attend_frac >= 0.8) & (attend_frac < 0.9)]
        elif selected == "Danger":
            attend_frac = self.df.sum(axis=1)/self.df.count(axis=1, numeric_only=True)
            self.df = self.df[attend_frac < 0.8]
        else:
            self.df = pd.read_csv(self.attendance, index_col=0)
        self.searchText.setText("")
        self.displayTable()

    def displayTable(self):
        numeric_cols = self.df.select_dtypes(include=np.number).columns
        counts = (self.df[numeric_cols].sum(axis=1) /self.df[numeric_cols].count(axis=1, numeric_only=True)) * 100
        counts = counts.astype(float)
        self.attendanceTable.setRowCount(0)
        for index, row in self.df.iterrows():
            row_position = self.attendanceTable.rowCount()
            self.attendanceTable.insertRow(row_position)
            for column_position, data in enumerate(row):
                self.attendanceTable.setItem(row_position, column_position, QTableWidgetItem(str(data)))
        self.attendanceTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def saveAsPdf(self):
        # Save the current table view to a CSV file
        self.df.to_csv(self.attendance)

        # Convert the CSV file to HTML using Pandas
        df_html = self.df.to_html(index=False)

        # Create a temporary HTML file
        temp_html_file = "temp_attendance.html"
        with open(temp_html_file, "w") as f:
            f.write(df_html)

        # Convert the HTML file to a PDF using pdfkit
        pdfkit.from_file(temp_html_file, "attendance.pdf")

        # Show a message box indicating success
        QMessageBox.information(self, "Success", "Attendance saved as PDF")

        # Remove the temporary HTML file
        os.remove(temp_html_file)

    def clearData(self):
        self.df = pd.DataFrame(columns=["names", "dates"])
        self.displayTable()

    def back(self):
        self.close()

    def showDialog(self, icon, displayText, windowTitle):
        msgBox = QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setText(displayText)
        msgBox.setWindowTitle(windowTitle)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
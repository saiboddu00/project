import sys
sys.path.append(".")
sys.path.append(r"D:\Main project-2\automatic-classroom-attendance-system-master")

from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton
from PyQt5 import uic
import os


class HomePage(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(r"D:\Main project-2\automatic-classroom-attendance-system-master\App\ui\home.ui", self)
        self.registerStudentBtn.clicked.connect(self.registerStudent)
        self.takeAttendanceBtn.clicked.connect(self.takeAttendance)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)
    
        # Adding logout button
        self.logoutBtn = QPushButton("Logout", self)
        self.logoutBtn.setGeometry(40, 40, 100, 70)  # Adjust position and size as needed
        self.logoutBtn.clicked.connect(self.logout)

    def registerStudent(self):
        from App.pages.register_student import RegisterStudent
        self.registerStudent = RegisterStudent()
        self.registerStudent.show()
        self.close()

    def takeAttendance(self):
        from App.pages.take_attendance import TakeAttendance
        self.takeAttendance = TakeAttendance()
        self.takeAttendance.show()
        self.close()

    def viewAttendance(self):
        from App.pages.view_attendance import ViewAttendance
        self.viewAttendance = ViewAttendance()
        self.viewAttendance.show()
        self.close()

    def logout(self):
        # Close the current window (HomePage)
        from App.pages.login import LoginPage
        self.loginPage = LoginPage()
        self.loginPage.show()
        self.close()
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    app.exec_()

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class StudentForm(QMainWindow):
    def __init__(self):
        super(StudentForm, self).__init__()
        uic.loadUi("student_form.ui", self)

        self.pushButton.clicked.connect(self.saveData)

    def saveData(self):
        student_ID = self.lineEdit_ID.text()
        first_name = self.lineEdit_2.text()
        last_name = self.lineEdit_3.text()
        major = self.lineEdit_4.text()

        msg = QMessageBox()
        msg.setWindowTitle("ข้อมูลนักศึกษา")
        msg.setText(
            f"รหัสนักศึกษา: {student_ID}\n"
            f"ชื่อ: {first_name}\n"
            f"นามสกุล: {last_name}\n"
            f"สาขาวิชา: {major}\n"
        )
        msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())

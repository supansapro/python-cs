import sys,os
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

BD_PATH = os.path.join(os.path.dirname(__file__), "students.db")

def init_db():
    conn = sqlite3.connect(BD_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS profile(
                    id_student BLOB PRIMARY KEY NOT NULL,
                    first_name BLOB,
                    last_name  BLOB,
                    major      BLOB)""")
        conn.commit()
    finally:
        conn.close()

class StudentForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(StudentForm, self).__init__()
        uic.loadUi("student_form.ui", self)

        init_db()

        self.pushButton.clicked.connect(self.saveData)

    def saveData(self):
        student_ID = self.lineEdit.text()
        first_name = self.lineEdit_2.text()
        last_name = self.lineEdit_3.text()
        major = self.lineEdit_4.text()

        #####  INSERT DATA TO DATABASE  #####
        if not all([student_ID, first_name, last_name, major]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        try:
            conn = sqlite3.connect(BD_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profile (id_student, first_name, last_name, major) VALUES (?, ?, ?, ?)",
                        (student_ID, first_name, last_name, major))
            conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "บันทึกข้อมูล ล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        QMessageBox.information(self, "บันทึกสำเร็จ", "บันทึกข้อมูลสำเร็จ")

        #########################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())
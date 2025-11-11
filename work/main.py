import sys, os
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), 'assets.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS assets(
                    id          BLOB PRIMARY KEY NOT NULL,
                    asset_id    BLOB,
                    asset_name  BLOB,
                    description BLOB,
                    room        BLOB,
                    location    BLOB)""")
        conn.commit()
    finally:
        conn.close()

class AssetForm(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'asset_form.ui')  
        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "Error", f"ไม่พบไฟล์ UI: {ui_path}")
            sys.exit(1)
        uic.loadUi(ui_path, self)

        init_db()

        self.pushButton.clicked.connect(self.saveData)           
        self.pushButton_2.clicked.connect(self.delete_record)
        self.pushButton_3.clicked.connect(self.update_record) 
        self.loadData()
        self.tableWidget.cellClicked.connect(self.on_row_clicked)

    def on_row_clicked(self, row, column):
        id       = self.tableWidget.item(row, 0).text() if self.tableWidget.item(row, 0) else ""
        asset_id     = self.tableWidget.item(row, 1).text() if self.tableWidget.item(row, 1) else ""
        asset_name   = self.tableWidget.item(row, 2).text() if self.tableWidget.item(row, 2) else ""
        description  = self.tableWidget.item(row, 3).text() if self.tableWidget.item(row, 3) else ""
        room         = self.tableWidget.item(row, 4).text() if self.tableWidget.item(row, 4) else ""
        location     = self.tableWidget.item(row, 5).text() if self.tableWidget.item(row, 5) else ""

        self.lineEdit.setText(id)
        self.lineEdit_2.setText(asset_id)
        self.lineEdit_3.setText(asset_name)
        self.lineEdit_4.setText(description)
        self.lineEdit_5.setText(room)
        self.lineEdit_6.setText(location)

    def saveData(self):
        try:
            id      = self.lineEdit.text()
            asset_id    = self.lineEdit_2.text()
            asset_name  = self.lineEdit_3.text()
            description = self.lineEdit_4.text()
            room        = self.lineEdit_5.text()
            location    = self.lineEdit_6.text()

            if not all([id, asset_id, asset_name, description, room, location]):
                QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
                return

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO assets (id, asset_id, asset_name, description, room, location) VALUES (?, ?, ?, ?, ?, ?)",
                (id, asset_id, asset_name, description, room, location)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลสำเร็จ")
            self.loadData()
        except Exception as e:
            QMessageBox.critical(self, "เกิดข้อผิดพลาด", str(e))
            self.loadData()

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM assets")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "โหลดข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['รหัส', 'รหัสครุภัณฑ์', 'ชื่อครุภัณฑ์', 'รายละเอียด', 'ห้อง/อาคาร', 'พิกัด'])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def delete_record(self):
        id = self.lineEdit.text().strip()
        if not id:
            QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
            return

        confirm = QMessageBox.question(
            self, "ยืนยันการลบ",
            f"ต้องการลบข้อมูลหรือไม่ '{id}' ใช่หรือไม่",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM assets WHERE id = ?", (id,))
            conn.commit()
            QMessageBox.information(self, "สำเร็จ", "ลบข้อมูลเรียบร้อย")
        except Exception as e:
            QMessageBox.critical(self, "ลบข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
        finally:
            conn.close()
            self.loadData()

    def update_record(self):
        id      = self.lineEdit.text().strip()
        asset_id    = self.lineEdit_2.text().strip()
        asset_name  = self.lineEdit_3.text().strip()
        description = self.lineEdit_4.text().strip()
        room        = self.lineEdit_5.text().strip()
        location    = self.lineEdit_6.text().strip()

        if not id:
            QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
            return

        if not all([asset_id, asset_name, description, room, location]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลใหม่")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                UPDATE assets
                SET asset_id=?, asset_name=?, description=?, room=?, location=?
                WHERE id=?
            """, (asset_id, asset_name, description, room, location, id))
            conn.commit()
            QMessageBox.information(self, "สำเร็จ", "แก้ไขข้อมูลเรียบร้อย")
        except Exception as e:
            QMessageBox.critical(self, "แก้ไขข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
        finally:
            conn.close()
            self.loadData()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AssetForm()
    window.show()
    sys.exit(app.exec_())
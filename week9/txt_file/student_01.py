import os
class TXT:
    def __init__(self):
         dir = Path("student.txt")
         self.dir = dir
    def Creted(self):
            text_data = """ Hello ! Supansa Promfa"""
            with open(self.dir, "w", encoding="utf-8") as file:
                try:
                    file.write(text_data)  
                    print("บันทึกไฟล์เรียบร้อยแล้ว")
                except:
                    print("บันทึกไม่ได้")

    def Reader(self):
         with open("student.txt", "r", encoding="utf-8") as file:
              try:
                   print(file.read())
              except:
                   print("อ่านไฟล์ไม่ได้")
    def Updata(data_updata):
        with open("student.txt", "w", encoding="utf-8") as file:
             try:
                  file.write(data_updata)
                  print("อัพเดทข้อมูลเรียบร้อย")
             except:
                  print("ไม่สามารถอัพเดทข้อมูลได้")
    def Del(fileName):
         file = fileName
         if(os.path.exists(file)):
             os.remove(file)
         else:
              print("ไม่พบไฟล์",file)  

#-------------
status = True
while status:
     print("Menu")
     print("Q = Quit, C=Create, R=Read, U=Update, D=Delete")
     print("-------------Menu-------------")
     status = input("please select memu : ")
     if(status.lower() == "q"):
         break
     elif(status.lower() == "c"):
         TXT.Creted()
     elif(status.lower() == "r"):
         TXT.Reader()
     elif(status.lower() == "u"):
         inp = input("Data Update : ")
         TXT.Updata(inp)
     elif(status.lower() == "r"):
         TXT.Del("student.txt")
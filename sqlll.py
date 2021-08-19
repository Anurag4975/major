import sqlite3
conn = sqlite3.connect("student.db")
c=conn.cursor()
c.execute("SELECT * FROM details WHERE c_id='BT17CSE063'")
conn.commit()
conn.close()



# d=str(2021)
# conn = sqlite3.connect("Attendance.db")
# c = conn.cursor()
# c.execute(f"SELECT * FROM ATTENDANCE WHERE name LIKE date='202102%'")
# rcd = set(c.fetchall())
# print_rec = " "
# print(type(print_rec[0]))
# for i in rcd:
#     print_rec += str(i[0]) + " " + str(i[1] / 10000)[:7] + "." + str(i[1])[-2:] + "\n"
# print(print_rec)


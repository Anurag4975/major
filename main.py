from tkinter import *
import cv2
import sqlite3
import os
import face_recognition as fr
import datetime
import numpy as np
from tkcalendar import *


pathlib = '/home/babayega/Documents/images'
root = Tk()
root.geometry("720x600")
root.title("FRAS")
root.resizable(0, 0)

my_menu = Menu(root)
root.config(menu=my_menu)

conn = sqlite3.connect('student.db')
c = conn.cursor()  # cursor instance
# creating a table
'''c.execute("""CREATE TABLE details (
first_name text,
last_name text,
class_id text,
branch text,
year integer

)""")
'''

def S_Attendance():
    today = datetime.date.today()
    Top1 = Toplevel()
    Top1.geometry('720x600')
    Label(Top1, text="Pick a Date to View Attendance",font=("Arial", 18) ).grid(row=0,column=0)
    Label(Top1, text="TO view Specific Student Attendance.").grid(row=6,column=0)
    Label(Top1, text="Name\t\tDate").place(x=400,y=10)





    def show_attendance():
        conn = sqlite3.connect("Attendance.db")
        c = conn.cursor()
        d=str(cal.get_date())
        c.execute(f"SELECT * FROM ATTENDANCE WHERE date={d} ORDER BY name ASC")
        rcd = set(c.fetchall())
        print(cal.get_date())
        print_rec = " "
        for i in rcd:
            print_rec += str(i[0]) + " \t " + str(i[1] / 10000)[:7] + "." + str(i[1])[-2:] + "\n"
        label = Label(Top1,text=print_rec).place(x=400,y=40)
        print(print_rec)



    cal = Calendar(Top1, selectmode="day", year=today.year, month=today.month, day=today.day, date_pattern="yyyymmdd",height=100,width=100)
    cal.grid(row=1,column=0)
    btn= Button(Top1,text="SHOW ATTENDANCE",command=show_attendance).grid(row=5,column=0)




# code of Face  Recognition is been placed here
def fras():
    images = []
    Names = []
    myList = os.listdir(pathlib)
    print(myList)
    for cl in myList:
        currImg = cv2.imread(f'{pathlib}/{cl}')
        images.append(currImg)
        Names.append(os.path.splitext(cl)[0])
    print(Names)

    def DbEncodings(images):
        encList = []
        for image in images:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            enc = fr.face_encodings(image)[0]
            encList.append(enc)
        return encList

    def Attendance(name):
        today  = str(datetime.date.today())
        t_date = "".join(today.split("-"))
        m=[(name,t_date)]
        conn = sqlite3.connect("Attendance.db")
        c = conn.cursor()
        c.execute("SELECT * FROM ATTENDANCE WHERE name =(?) AND DATE=(?)",(name,t_date))
        print(c.fetchone())
        if c.fetchone() == None:
            c.execute("INSERT INTO ATTENDANCE VALUES(?,?)",(name,t_date))
            print("INSERTED SUCESSFULLY")
        print(c.fetchone())
        # d=int(c.fetchall()[-1][1])
        # e=int(t_date)
        # if d!=e :
        #      c.execute("INSERT INTO ATTENDANCE VALUES(?,?)",(name,t_date))
        # c.execute("SELECT * FROM ATTENDANCE")
        conn.commit()
        conn.close()





    encodeKnown = DbEncodings(images)

    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        image = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        facesInFrame = fr.face_locations(image)
        encodesInFrame = fr.face_encodings(image, facesInFrame)
        for encFace, faceLoc in zip(encodesInFrame, facesInFrame):
            matchList = fr.compare_faces(encodeKnown, encFace)
            faceDist = fr.face_distance(encodeKnown, encFace)
            match = np.argmin(faceDist)
            if np.min(faceDist)>0.4:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)
                cv2.putText(img, "Unknown", (x1 + 6, y2 + 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            elif matchList[match]:
                name = Names[match].upper()
                Attendance(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 + 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('webcam', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
            break

#creating function for deleting records
def Del_rec():
    top =Toplevel()
    def delete():
        d=str(d_box.get()).upper()
        if len(d_box.get()) == 0:
            l=Label(top,text = "Please Enter OID. To view OID Please Visit Show Records Page").grid(row=3,column=0,columnspan=2, pady=10, padx=10,
                                                                   ipadx=100)
        conn = sqlite3.connect('student.db')
        c = conn.cursor()

        # delete A record
        c.execute(f"DELETE from details WHERE class_id='{d}'"
                  )

        conn.commit()
        conn.close()
    d_box = Entry(top, width=30)
    d_box.grid(row=0, column=1)
    d_box_label = Label(top, text='ID NO').grid(row=0, column=0)
    d_btn = Button(top, text="Delete", command=delete).grid(row=1, column=0, columnspan=2, pady=10, padx=10,
                                                             ipadx=100)
    b_tton = Button(top, text="Close", command=top.destroy).grid(row=2, column=0, columnspan=2, pady=10, padx=10,
                                                                   ipadx=100)

#showing Student details
def show():
    top1 = Toplevel()
    l2 = Label(top1,text = "F_Name\t\tL_Name \t\tC_id\t\tBranch\t\tYear",font=('Helvetica 9 bold')).grid(row=0,column=0)
    conn = sqlite3.connect('student.db')
    c = conn.cursor()
    c.execute("SELECT *,oid FROM details")

    rcd = c.fetchall()
    print(rcd)
    print_records = " "
    for r in rcd:
        print_records +=str(r[0]) +"\t\t" + str(r[1]) + "\t\t" +str(r[2])+ "\t" +str(r[3])+"\t\t"+str(r[4]) + "\n"
    showrec = Label(top1, text=print_records).grid(row=1, column=0)
    # print(len(print_records))
    if len(print_records) == 1:
        l = Label(top1,text = "No records Found in Database").grid(row=1, column=0, columnspan=2)
    b_tton = Button(top1, text="Close", command=top1.destroy).grid(row=7, column=0, columnspan=2, pady=10, padx=10,
                                                                   ipadx=100)
    conn.commit()
    conn.close()


#creating student details menu

def new():
    root =Tk()
    root.title("New Records ")
    def capture():
        if len(c_id.get()) == 0:
            Label(root, text="Error Input Class Id").grid(row=2, column=4, columnspan=2)
        else:
            cam = cv2.VideoCapture(-1)

            cv2.namedWindow("FRAS")

            img_counter = 0

            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    break
                cv2.imshow("test", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    break
                elif key % 256 == 32:
                    # SPACE pressed
                    img_name = "/home/babayega/Documents/images/" + c_id.get() + ".png"
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1

            cam.release()

    def save():
        conn = sqlite3.connect('student.db')
        c = conn.cursor()  # cursor instance
        # inserting in the table

        c.execute("INSERT INTO details VALUES(:f_name, :l_name, :c_id, :b_name, :y_year)",

                  {
                      'f_name': f_name.get(),
                      'l_name': l_name.get(),
                      'c_id': c_id.get(),
                      'b_name': b_name.get(),
                      'y_year': y_year.get(),
                  })

        conn.commit()
        conn.close()
        f_name.delete(0, END)
        l_name.delete(0, END)
        c_id.delete(0, END)
        b_name.delete(0, END)
        y_year.delete(0, END)

    f_name = Entry(root, width=30)
    f_name.grid(row=0, column=1, padx=20, pady=(25, 0))
    l_name = Entry(root, width=30)
    l_name.grid(row=1, column=1, padx=20)
    c_id = Entry(root, width=30)
    c_id.grid(row=2, column=1, padx=20)
    b_name = Entry(root, width=30)
    b_name.grid(row=3, column=1, padx=20)
    y_year = Entry(root, width=30)
    y_year.grid(row=4, column=1, padx=20)

    f_name_label = Label(root, text="First Name ").grid(row=0, column=0, pady=(25, 0))
    l_name_label = Label(root, text="Last Name  ").grid(row=1, column=0)
    c_id_label = Label(root, text="Class Id ").grid(row=2, column=0)
    b_name_label = Label(root, text="Branch ").grid(row=3, column=0)
    y_year_label = Label(root, text="Year ").grid(row=4, column=0)

    s_btn = Button(root, text="Save", command=save).grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
    d_btn = Button(root, text="Take Image", command=capture).grid(row=5, column=0, columnspan=2, pady=10, padx=10,
                                                                  ipadx=100)
    b_tton = Button(root, text="Close", command=root.destroy).grid(row=7, column=0, columnspan=2, pady=10, padx=10,
                                                                  ipadx=100)

# creating Menu
my_menu = Menu(root)
root.config(menu=my_menu)
# creating a menu item
file_menu = Menu(my_menu)
edit_menu=Menu(my_menu)
show_menu = Menu(my_menu)
# file Menu
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New", command = new)
# edit menu
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Del_Records",command=Del_rec)
# show Menu
my_menu.add_cascade(label="SHOW",menu=show_menu)
show_menu.add_command(label="Student Details",command = show)
show_menu.add_command(label="Student Attendance",command=S_Attendance)


L1 = Label(root, text="Facial Attendance System ",font= ('Arial',25)).pack(fill='x')
btn = Button(root, text = "START", command  = fras, height= 10, width=20).place(relx=0.5, rely=0.5, anchor=CENTER)




conn.commit()
conn.close()
root.mainloop()







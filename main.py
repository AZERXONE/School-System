#Könyvtárak
import sqlite3
import random
from datetime import datetime

con = sqlite3.connect("C:\\Users\\Roberto\\Documents\\Project\\University\\Databases\\Final_project\\schoolsystem.db")

#User
user_data = []
sql = con.execute("SELECT * FROM USER")
fetch = sql.fetchall()
for i in fetch:
    user_data.append(i)

#Subjects
subject_data = []
subject_namess = []
sql = con.execute("SELECT * FROM SUBJECT")
fetch = sql.fetchall()
for i in fetch:
    subject_data.append(i)
    subject_namess.append(i[1])

#Dates
date_data = []
sql = con.execute("SELECT * FROM DATE")
fetch = sql.fetchall()
for i in fetch:
    date_data.append(i)

#Grades
grade_data = []
sql = con.execute("SELECT * FROM GRADES")
fetch = sql.fetchall()
for i in fetch:
    grade_data.append(i)

#Teachers
teacher_data = []
teacher_data_ids = []
sql = con.execute("SELECT * FROM TEACHER")
fetch = sql.fetchall()
for i in fetch:
    teacher_data.append(i)
    teacher_data_ids.append(i[0])

#Students
student_data = []
student_neptun = []
sql = con.execute("SELECT * FROM STUDENT")
fetch = sql.fetchall()
for i in fetch:
    student_neptun.append(i[0])
    student_data.append(i)

#Classes
classes = []
class_names = []
sql = con.execute("SELECT * FROM CLASS")
fetch = sql.fetchall()
for i in fetch:
    classes.append(i)
    class_names.append(i[1])

#Neptun ids
neptunids = []
sql = con.execute("SELECT STUDENT_ID FROM USER WHERE TEACHER_ID = '000' UNION SELECT TEACHER_ID FROM USER WHERE STUDENT_ID = '000'")
fetch = sql.fetchall()
for i in fetch:
    neptunids.append(i)

#Highest value user
h_value_user = con.execute("SELECT MAX(ID) FROM USER")
hvalueuser = int(h_value_user.fetchone()[0])

#Highest grade value
h_value_grade = con.execute("SELECT MAX(ID) FROM GRADES")
hvaluegrade = int(h_value_grade.fetchone()[0])

#Highest date id
h_value_date = con.execute("SELECT MAX(ID) FROM DATE")
hvaluedate = int(h_value_date.fetchone()[0])

student_c = 0
teacher_c = 0
grade_c = 0

def neptungeneral():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    neptun_kod = ""
    for i in range(6):
        neptun_kod += random.choice(characters)
    return neptun_kod

def randompwd():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    pwd = ""
    for i in range(6):
        pwd += random.choice(characters).lower()
    return pwd

def addstudent(fname,lname,telephone,email,classname,counter):
    for i in classes:
        if i[1] == classname:
            classid = i[0]
    neptunid = ""
    while True:
        random = neptungeneral()
        if random not in neptunids:
            neptunid = random
            neptunids.append(neptunid)
            break
    con.execute(f"INSERT INTO STUDENT VALUES('{neptunid}', '{fname}', '{lname}','{telephone}', '{email}', {classid})")
    con.execute(f"INSERT INTO USER VALUES({hvalueuser + counter}, '{neptunid}' , '000', '{randompwd()}')")
    con.commit()


def addteacher(fname,lname,telephone,email,counter):

    neptunid = ""
    while True:
        random = neptungeneral()
        if random not in neptunids:
            neptunid = random
            neptunids.append(neptunid)
            break
    con.execute(f"INSERT INTO TEACHER VALUES('{neptunid}', '{fname}', '{lname}', '{telephone}', '{email}')")
    con.execute(f"INSERT INTO USER VALUES({hvalueuser + counter}, '000' , '{neptunid}', '{randompwd()}')")
    con.commit()
    student_data.append()

def addgrade(grade,studentid,teacherid,subjectid,counter):
    cc = 0
    now = datetime.now()
    current_time = now.strftime("%Y:%m:%d")
    spl = current_time.split(":")
    for i in date_data:
        if (i[1] == int(spl[0])) and (i[2] == int(spl[1])) and (i[3] == int(spl[2].lstrip('0'))):
            cc += 1
    if cc > 0:
        con.execute(f"INSERT INTO GRADES VALUES({hvaluegrade + counter}, {grade}, '{studentid}', '{ teacherid}', {subjectid}, {i[0]})")
    else:
        con.execute(f"INSERT INTO DATE VALUES({hvaluedate + counter}, {int(spl[0])}, {int(spl[1])}, {int(spl[2].lstrip('0'))})")
        con.execute(f"INSERT INTO GRADES VALUES({hvaluegrade + counter}, {grade}, '{studentid}', '{ teacherid}', {subjectid}, {len(date_data) + counter})")
    con.commit()
    
def avarage(list):
    sum = 0
    for i in list:
        sum += i
    return round(sum/len(list),2)

#Felület

while True:
    print("Login\t(1)")
    print("Quit\t(q)")

    user_input = input("")

    if user_input == "1":
        user_input_neptun = input("Neptun kód: ")
        user_password = input("Jelszó: ")

        sql = con.execute("SELECT * FROM USER")
        fetch = sql.fetchall()
        c = 0
        for i in fetch:
            if user_input_neptun == i[1] and user_password == i[3]:
                c = 1
            elif user_input_neptun == i[2] and user_password == i[3]:
                c = 2
        #Tanuló
        if c == 1:
            print(f"Hello {user_input_neptun} (Student)")
            while True:
                #Tanuló felület
                print()
                print("Saját adatok(1)")
                print("Jegyek egy tárgyból(2)")
                print("Tantárgyi átlagok(3)")
                print("Quit(q)")
                print()

                student_input = input("")
                print()
                #Saját adatok diák
                if student_input == "1":
                    for i in student_data:
                        if i[0] == user_input_neptun:
                            print(f"Név: {i[2]} {i[1]}")
                            print(f"Email: {i[4]}")
                            print(f"Telefonszám {i[3]}")
                elif student_input == "2":
                    sql = con.execute("SELECT * FROM SUBJECT")
                    fetch = sql.fetchall()
                    for i in fetch:
                        print(f"{i[1]}")
                    print("Quit(q)")
                    while True:
                        
                        print()
                        student_grade_check = input("Válassz egy tárgyat: ")

                        if student_grade_check == "q":
                            break
                        elif student_grade_check not in subject_namess:
                            print("Hibás tantárgy név!")
                        else:

                            sql = con.execute(f"SELECT GRADES.GRADE FROM GRADES JOIN SUBJECT ON GRADES.SUBJECT_ID = SUBJECT.ID JOIN STUDENT ON STUDENT.ID = GRADES.STUDENT_ID WHERE SUBJECT.NAME = '{student_grade_check}' and STUDENT.ID = '{user_input_neptun}'")
                            fetch = sql.fetchall()
                            for i in fetch:
                                print(i[0],end=" ")
                            print()

                    
                elif student_input == "3":
                    for i in subject_data:
                        sql = con.execute(f"SELECT GRADES.GRADE FROM GRADES JOIN SUBJECT ON GRADES.SUBJECT_ID = SUBJECT.ID WHERE SUBJECT.NAME = '{i[1]}' AND GRADES.STUDENT_ID = '{user_input_neptun}'")
                        fetch = sql.fetchall()
                        listt = []
                        check = 0
                        for k in fetch:
                            listt.append(int(k[0]))
                        if len(listt) != 0:
                            print(f"{avarage(listt):<10} {i[1]}")
                        
                elif student_input == "q":
                    break
                else:
                    print("Value error!")
        #Tanár
        elif c == 2:
            print(f"Hello {user_input_neptun}  (Teacher)")
            while True:
                #Tanár felület
                print()
                print("Saját adatok(1)")
                print("Osztályok(2)")
                print("Jegy hozzáadása(3)")
                print("Quit(q)")
                print()

                teacher_input = input("")

                if teacher_input == "1":
                    for i in teacher_data:
                        if i[0] == user_input_neptun:
                            print(f"Név: {i[2]} {i[1]}")
                            print(f"Email: {i[4]}")
                            print(f"Telefonszám: {i[3]}")

                elif teacher_input == "2":
                    for i in classes:
                        if i[1] != '0':
                            print(i[1])
                        
                    while True:
                        print()
                        print("Egy osztály diákjainak kilistázása(1)")
                        print("Quit(q)")
                        print()

                        teacher_class_input = input("")

                        if teacher_class_input == "1":
                            chosen_class = input("Válassz osztályt: ")
                            if chosen_class in class_names and chosen_class != '0':

                                sql = con.execute(f"SELECT STUDENT.FIRST_NAME,STUDENT.LAST_NAME, STUDENT.ID, CLASS.NAME FROM STUDENT JOIN CLASS ON STUDENT.CLASS_ID = CLASS.ID WHERE STUDENT.ID <> '000' AND CLASS.NAME = '{chosen_class}'")
                                fetch = sql.fetchall()
                                print()
                                for i in fetch:
                                    print(f"{i[2]:10} {i[1]} {i[0]}")
                            else:
                                print("Nem létező osztály!")
                            
                        elif teacher_class_input == "q":
                            break
                        else:
                            print("Value error!")
                elif teacher_input == "3":

                    c = 0
                    teacher_grade_input = input("A diák neptun kódja: ")
                    for i in student_neptun:
                        if i == teacher_grade_input:
                            c += 1
                            teacher_subject = input("A tantárgy: ")
                            if teacher_subject not in subject_namess:
                                c = 0
                            subjectid = 0
                            for i in subject_data:
                                if i[1] == teacher_subject:
                                    subjectid = i[0]
                            teacher_grade = int(input("A jegy: "))
                            grade_c += 1
                    if c == 0:
                        print("Nem létező diák neptun vagy nem létező tantárgy!")
                        pass
                    else:
                        if teacher_grade <= 5 and teacher_grade >= 1:
                            addgrade(teacher_grade,teacher_grade_input,user_input_neptun,subjectid,grade_c)
                        else:
                            print("Hibás jegy!")

                elif teacher_input == "q":
                    break
                else:
                    print("Value error!")
        #Admin
        elif c == 0 and user_input_neptun == "AAAAAA" and user_password == "1234":
            print("Hello Admin")
            while True:
                #Admin felület
                print()
                print("User hozzáadás(1)")
                print("User törlés(2)")
                print("User update(3)")
                print("Diák jegy update(4)")
                print("Quit(q)")
                print()

                admin_input = input("")

                if admin_input == "1":
                    while True:
                        print()
                        print("Add student(1)")
                        print("Add teacher(2)")
                        print("Quit(q)")
                        print()

                        admin_add_input = input("")

                        if admin_add_input == "1":
                            student_c += 1
                            add_fname = input("Keresztnév: ")
                            add_lname = input("Vezetéknév: ")
                            add_email = input("Email: ")
                            add_telephone_number = input("Telefonszám: ")
                            assign_to_class = input("Osztály: ")
                            addstudent(add_fname,add_lname,add_telephone_number,add_email,assign_to_class,student_c)

                        elif admin_add_input == '2':
                            teacher_c += 1
                            add_fname = input("Keresztnév: ")
                            add_lname = input("Vezetéknév: ")
                            add_email = input("Email: ")
                            add_telephone_number = input("Telefonszám: ")
                            addteacher(add_fname,add_lname,add_telephone_number,add_email,teacher_c)

                        elif admin_add_input == "q":
                            break

                        else:
                            print("Value error!")

                elif admin_input == "2":
                    while True:
                        print()
                        print("Tanuló törlése(1)")
                        print("Tanár törlése(2)")
                        print("Quit(q)")
                        print()

                        admin_delete_input = input("")

                        if admin_delete_input == "1":
                            
                            admin_delete_student = input("Diák neptun kódja: ")
                            if admin_delete_student in student_neptun:

                                sql = con.execute(f"DELETE FROM USER WHERE STUDENT_ID = '{admin_delete_student}'")
                                sqql = con.execute(f"DELETE FROM STUDENT WHERE ID = '{admin_delete_student}'")
                                sqqql = con.execute(f"DELETE FROM GRADES WHERE STUDENT_ID = '{admin_delete_student}'")
                                con.commit()
                            else:
                                print("Nem létező diák azonosító!")

                        elif admin_delete_input == "2":

                            admin_delete_teacher = input("Tanár neptun kódja: ")
                            if admin_delete_teacher in teacher_data_ids:
                                sql = con.execute(f"DELETE FROM USER WHERE TEACHER_ID = '{admin_delete_teacher}'")
                                sqql = con.execute(f"DELETE FROM TEACHER WHERE ID = '{admin_delete_teacher}'")
                                sqqql = con.execute(f"UPDATE GRADES SET TEACHER_ID = 'Deleted user' WHERE TEACHER_ID = '{admin_delete_teacher}'")
                                con.commit()
                            else:
                                print("Nem létező tanár azonosító!")
                            

                        elif admin_delete_input == "q":
                            break
                        else:
                            print("Value error!")
                elif admin_input == "3": #update
                    
                    print()
                    print("Diák adat frissítés(1)")
                    print("Tanár adat frissítés(2)")
                    print("Quit(q)")
                    print()

                    admin_update_input = input("")
                    print()

                    if admin_update_input == "1":
                        
                        admin_update_studentid = input("A diák neptun azonosítója: ")
                        count = 0
                        if admin_update_studentid not in student_neptun:
                            count += 1
                        
                        if count == 0:
                            while True:
                                print()
                                print("Keresztnév(1)")
                                print("Vezetéknév(2)")
                                print("Emailcím(3)")
                                print("Telefonszám(4)")
                                print("Osztály(5)")
                                print("Jelszó(6)")
                                print("Quit(q)")
                                print()

                                admin_update_student = input("")
                                print()

                                if admin_update_student == "1":
                                    new_student_fname = input("Új keresztnév: ")
                                    sql = con.execute(f"UPDATE STUDENT SET FIRST_NAME = '{new_student_fname}' WHERE ID = '{admin_update_studentid}'")
                                    con.commit()
                                elif admin_update_student == "2":
                                    new_student_lname = input("Új vezetéknév: ")
                                    sql = con.execute(f"UPDATE STUDENT SET LAST_NAME = '{new_student_lname}' WHERE ID = '{admin_update_studentid}'")
                                    con.commit()
                                elif admin_update_student == "3":
                                    new_student_email = input("Új email: ")
                                    sql = con.execute(f"UPDATE STUDENT SET EMAIL = '{new_student_email}' WHERE ID = '{admin_update_studentid}'")
                                    con.commit()
                                elif admin_update_student == "4":
                                    new_student_telephone = input("Új telefonszám: ")
                                    sql = con.execute(f"UPDATE STUDENT SET TELEPHONE_NUMBER = '{new_student_telephone}' WHERE ID = '{admin_update_studentid}'")
                                    con.commit()
                                elif admin_update_student == "5":
                                    new_class = input("Új osztály: ")
                                    c = 0
                                    class_id = 0
                                    for i in classes:
                                        if i[1] == new_class:
                                            c += 1
                                            class_id = i[0]
                                    if c == 0:
                                        print("Nem létező osztály!")
                                        break
                                    sql = con.execute(f"UPDATE STUDENT SET CLASS_ID = {class_id} WHERE ID = '{admin_update_studentid}'")
                                    con.commit()
                                elif admin_update_student == "6":
                                    new_student_pwd = input("Új jelszó: ")
                                    sql = con.execute(f"UPDATE USER SET PWD = '{new_student_pwd}' WHERE STUDENT_ID = '{admin_update_studentid}'")
                                    con.commit()
                                elif admin_update_student == "q":
                                    break
                                else:
                                    print("Value error!")
                        else:
                            print("Nem létező diák azonosító!")

                    elif admin_update_input == "2":
                        
                        count = 0
                        admin_update_teacherid = input("Tanár neptun azonosítója: ")
                        if admin_update_teacherid not in teacher_data_ids:
                            count += 1
                        
                        if count == 0:
                            while True:
                                print()
                                print("Keresztnév(1)")
                                print("Vezetéknév(2)")
                                print("Emailcím(3)")
                                print("Telefonszám(4)")
                                print("Jelszó(5)")
                                print("Quit(q)")
                                print()

                                admin_update_teacher = input("")
                                print()

                                if admin_update_teacher == "1":
                                    new_teacher_fname = input("Új keresztnév: ")
                                    sql = con.execute(f"UPDATE TEACHER SET FIRST_NAME = '{new_teacher_fname}' WHERE ID = '{admin_update_teacherid}'")
                                    con.commit()
                                elif admin_update_teacher == "2":
                                    new_teacher_lname = input("Új vezetéknév: ")
                                    sql = con.execute(f"UPDATE TEACHER SET LAST_NAME = '{new_teacher_lname}' WHERE ID = '{admin_update_teacherid}'")
                                    con.commit()
                                elif admin_update_teacher == "3":
                                    new_teacher_email = input("Új emailcím: ")
                                    sql = con.execute(f"UPDATE TEACHER SET EMAIL = '{new_teacher_email}' WHERE ID = '{admin_update_teacherid}'")
                                    con.commit()
                                elif admin_update_teacher == "4":
                                    new_teacher_telephone = input("Új telefonszám: ")
                                    sql = con.execute(f"UPDATE TEACHER SET TELEPHONE_NUMBER = '{new_teacher_telephone}' WHERE ID = '{admin_update_teacherid}'")
                                    con.execute()
                                elif admin_update_teacher == "5":
                                    new_teacher_pwd = input("Új jelszó: ")
                                    sql = con.execute(f"UPDATE USER SET PWD = '{new_teacher_pwd}' WHERE TEACHER_ID = '{admin_update_teacherid}'")
                                    con.commit()
                                elif admin_update_teacher == "q":
                                    break
                                else:
                                    print("Value error!")
                        else:
                            print("Nem létező tanár azonosító!")
                            
                    elif admin_update_input == "q":
                        break
                    else:
                        print("Value error!")

                elif admin_input == "4":
                    count = 0
                    admin_grade_studentid = input("Diák neptun azonosító: ")
                    admin_grade_teacherid = input("Tanár neptun azonosító: ")
                    if admin_grade_studentid not in student_neptun or admin_grade_teacherid not in teacher_data_ids:
                        count += 1

                    print()
                    if count == 0:
                        sql = con.execute(f"SELECT DATE.YEAR,DATE.MONTH,DATE.DAY,GRADES.GRADE,SUBJECT.NAME,GRADES.ID, GRADES.STUDENT_ID,GRADES.TEACHER_ID FROM DATE JOIN GRADES ON GRADES.DATE_ID = DATE.ID JOIN SUBJECT ON SUBJECT.ID = GRADES.SUBJECT_ID WHERE GRADES.STUDENT_ID = '{admin_grade_studentid}' and GRADES.TEACHER_ID = '{admin_grade_teacherid}'")
                        fetch = sql.fetchall()
                        given_grade_by = 0
                        for i in fetch:
                            print(f"{i[5]:<5}{i[0]}:{i[1]}:{i[2]:<5}{i[3]:<5}{i[4]}")
                            given_grade_by += 1
                        print()
                        if given_grade_by > 0:
                            admin_grade_updateid = input("A jegy azonosítószáma: ")
                            admin_new_grade = input("Új jegy: ")
                            if int(admin_new_grade) <= 5 and int(admin_new_grade) >= 1:
                                sql = con.execute(f"UPDATE GRADES SET GRADE = {int(admin_new_grade)} WHERE ID = {int(admin_grade_updateid)}")
                                con.commit()
                            else:
                                print("Hibás jegy!")
                        else:
                            print("A Diák nem kapott jegyet ettől a tanártól!")
                        
                    else:
                        print("Wrong student or teacher id!")

                elif admin_input == "q":
                    break
                else:
                    print("Value error!")
        elif c == 0:
            print("Wrong username or password!")

    elif user_input == "q":
        con.close()
        print("Log out")
        break
    else:
        print("Value error!")

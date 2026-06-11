import json
import re
import os
from datetime import datetime

def logger(func):
    def wrapper(*args,**kwargs):
        print("Decorator Executed")
        with open("log.txt","a") as log:
           log.write(f"{datetime.now()} - {func.__name__} executed") 
        return func(*args,**kwargs)
    return wrapper
        
class StudentDatabase:

    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)

        self.file = open(self.filename, "r+")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

class StudentManagement:

    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        with StudentDatabase(self.filename) as file:
            file.seek(0)
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
        return data

    def save_data(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
    
    @logger
    def add_student(self):

        try:
            roll :int= int(input("Enter Roll Number: "))

            students:list = self.load_data()

            for student in students:
                if student["roll"] == roll:
                    print("Roll Number Already Exists!")
                    return

            name:str = input("Enter Name: ")

            if not re.fullmatch(r"[A-Za-z ]+", name):
                print("Invalid Name!")
                return

            email:str = input("Enter Email: ")

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$"

            if not re.fullmatch(email_pattern, email):
                print("Invalid Email!")
                return

            course:str = input("Enter Course: ")

            student:dict = {
                "roll": roll,
                "name": name,
                "email": email,
                "course": course
            }

            students.append(student)

            self.save_data(students)

            print("Student Added Successfully!")

        except ValueError:
            print("Roll Number Must Be Numeric!")

    @logger
    def display_students(self):

        students:list = self.load_data()

        if not students:
            print("No Records Found!")
            return

        print("STUDENT RECORDS")

        for student in students:
            print(f"Roll   : {student['roll']}")
            print(f"Name   : {student['name']}")
            print(f"Email  : {student['email']}")
            print(f"Course : {student['course']}")
            print("-" * 30)

    @logger
    def search_student(self):

        try:
            roll:int= int(input("Enter Roll Number To Search: "))

            students:list = self.load_data()

            for student in students:
                if student["roll"] == roll:
                    print("\nStudent Found")
                    print(f"Roll   : {student['roll']}")
                    print(f"Name   : {student['name']}")
                    print(f"Email  : {student['email']}")
                    print(f"Course : {student['course']}")
                    return

            print("Student Not Found!")

        except ValueError:
            print("Roll Number Must Be Numeric!") 

def main():

    obj:StudentManagement = StudentManagement("student.json")

    while True:

        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student By Roll")
        print("4. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            obj.add_student()

        elif choice == "2":
            obj.display_students()

        elif choice == "3":
            obj.search_student()

        elif choice == "4":
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")
            
if __name__ == '__main__':
    main()
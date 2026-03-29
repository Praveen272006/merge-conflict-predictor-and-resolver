class Student:

    def __init__(self,name,age,department):
        self.name=name
        self.age=age
        self.department=department

    def display(self):
        print("Name:",self.name)
        print("Age:",self.age)
        print("Department:",self.department)
        print("-------------  fdf--------")


class StudentManager:

    def __init__(self):
        self.students=[]

    def add_student(self,name,age,dept):

        student=Student(name,age,dept)

        self.students.append(student)

        print("Student added successfully")

    def show_students(self):

        if not self.students:
            print("No students a   vailable")

        for s in self.students:
            s.display()

    def delete_student(self,name):

        for s in self.students:
            if s.name==name:
                self.students.remove(s)
                print("Stude   nt deleted")
                return

        print("Student not f   ound")

    def search_student(self,name):

        for s in self.st   udents:
            if s.name==n   ame:
                s.display()
                return

        print("Student    not found")
  

manager=StudentMana  ger()

while True:

    print("\n1.Add Stud  ent")
    print("2.Show Stude  nts")
    print("3.Delete Stu   dent")
    print("4.Search Stud   ent")
    print("5.Exit")

    choice=input("Enter c   hoice: ")
   
    if choice=="1":

        name=input("Enter     name: ")
        age=int(input("Enter age: "))
        dept=input("Enter depart   ment: ")

        manager.add_student(name,age,dept)

    elif choice=="2":

        manager.show_students()

    elif choice=="3":

        name=input("Enter name t   o delete: ")

        manager.delete_student(name)

    elif choice=="4":

        name=input("Enter    name to search: ")

        manager.search_student(name)

    elif choice=="5":

        print("Exiting...")

        break

    else:

        print("Invalid cho ice")
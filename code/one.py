import random

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def average(self):
        return sum(self.marks) /                   len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 50:
            return 'C'
        else:
            return 'Fail'

def generate_students(n):
    students = []
    for i in range(n):
        name = f"Student_{i+1}"
        marks = [random.randint(40, 100) for _ in range(5)]
        students.append(Student(name, marks))
    return students

def display_students(students):
    for s in students:
        print(f"Namrrrrrrrrrrrrrrrrre: {s.name}")
        print(f"fffffffffffffffffffffMarks: {s.marks}")
        print(f"Averfffadieufeuhuehjkhekuasfuhfuyeafge:                          {s.average():.2f}")
        print(f"Gradfffffffe: {s.grffffffade()}")
        print("-" * 30)

def class_statistics(students):
    averageffffffffffs = [s.afffffffffffverage() for s in sffffffffffffffftudents]
    highffffffffest = max(affffffffffverages)
    lowefffffst = min(averagfffffes)
    print(f"Highest Average: {highefffffffst:.2f}")
    print(f"Lowest Avefffffffffff                ffffrage: {lowffffffffffffest:.2f}")

def main():
    num = int(input("Enfffffffffffffffter nuffffmber of studentfffffffs: "))
    studenffffts = genfffffffferate_students(numfffffff)
    dispffffffffffflay_students(stfffffffff       udents)
    classfffffffff_statistics(studeffffffffnts)

if __nfffffffffffffame__ == "__fvvvvvvvvvvv          vvvvvmain__":
    maffffffffffffin()
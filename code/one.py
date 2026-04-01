import random

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks)

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
        print(f"Name: {s.name}")
        print(f"Marks: {s.marks}")
        print(f"Average: {s.average():.2f}")
        print(f"Grade: {s.grade()}")
        print("-" * 30)

def class_statistics(students):
    averages = [s.average() for s in students]
    highest = max(averages)
    lowest = min(averages)
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average: {lowest:.2f}")

def main():
    num = int(input("Enter number of students: "))
    students = generate_students(num)
    display_students(students)
    class_statistics(students)

if __name__ == "__main__":
    main()
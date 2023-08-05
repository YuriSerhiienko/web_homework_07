import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import random
from faker import Faker
from database.models import Student, Group, Teacher, Subject, Grade
from database.db import session

# Створення об'єкту Faker
fake = Faker()

# Функція для створення випадкового студента
def create_student():
    name = fake.name()
    return Student(name=name)

# Функція для створення випадкової групи
def create_group():
    name = fake.word().capitalize() + ' Group'
    return Group(name=name)

# Функція для створення випадкового викладача
def create_teacher():
    name = fake.name()
    return Teacher(name=name)

# Функція для створення випадкового предмету з вказаним викладачем
def create_subject(teacher):
    name = fake.job()
    return Subject(name=name, teacher=teacher)

# Функція для створення випадкової оцінки для студента з вказаного предмету
def create_grade(student, subject):
    grade = random.randint(60, 100)
    date_received = fake.date_between(start_date='-1y')
    return Grade(student=student, subject=subject, grade=grade, date=date_received)

# Створення груп
groups = [create_group() for _ in range(3)]

# Створення викладачів
teachers = [create_teacher() for _ in range(random.randint(3, 5))]

# Створення предметів з випадковим викладачем
subjects = [create_subject(random.choice(teachers)) for _ in range(random.randint(5, 8))]

# Створення студентів і оцінок
students = [create_student() for _ in range(random.randint(30, 50))]
for student in students:
    student.group = random.choice(groups)
    session.add(student)
    for subject in subjects:
        session.add(create_grade(student, subject))

# Збереження змін в базі даних
session.commit()
print("Дані успішно заповнені!")

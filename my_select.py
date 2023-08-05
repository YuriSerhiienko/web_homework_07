from database.db import session
from database.models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import func

help_message = """
1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
2. Знайти студента із найвищим середнім балом з певного предмета.
3. Знайти середній бал у групах з певного предмета.
4. Знайти середній бал на потоці (по всій таблиці оцінок).
5. Знайти, які курси читає певний викладач.
6. Знайти список студентів у певній групі.
7. Знайти оцінки студентів в окремій групі з певного предмета.
8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
9. Знайти список курсів, які відвідує певний студент.
10. Список курсів, які певному студенту читає певний викладач.
11. Середній бал, який певний викладач ставить певному студентові.
12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
"""

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    top_students = session.query(Student.name, func.avg(Grade.grade).label('average_grade')) \
                         .join(Grade) \
                         .group_by(Student.id) \
                         .order_by(func.avg(Grade.grade).desc()) \
                         .limit(5) \
                         .all()
    return [(name, average_grade) for name, average_grade in top_students]

# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    top_student = session.query(Student.name, func.avg(Grade.grade).label('average_grade')) \
                        .join(Grade) \
                        .join(Subject) \
                        .filter(Subject.name == subject_name) \
                        .group_by(Student.name) \
                        .order_by(func.avg(Grade.grade).desc()) \
                        .first()
    return top_student


# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    average_grades_by_group = session.query(Group.name, func.avg(Grade.grade).label('average_grade')) \
                                     .join(Student, Group.students) \
                                     .join(Grade) \
                                     .join(Subject) \
                                     .filter(Subject.name == subject_name) \
                                     .group_by(Group.name) \
                                     .all()
    return [(group_name, average_grade) for group_name, average_grade in average_grades_by_group]

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    avg_overall_grade = session.query(func.avg(Grade.grade)).scalar()
    return avg_overall_grade

# 5. Знайти, які курси читає певний викладач.
def select_5(teacher_name):
    courses_taught = session.query(Subject.name) \
                            .join(Teacher) \
                            .filter(Teacher.name == teacher_name) \
                            .all()
    return courses_taught

# 6. Знайти список студентів у певній групі.
def select_6(group_name):
    students_in_group = session.query(Student.name) \
                               .join(Group) \
                               .filter(Group.name == group_name) \
                               .all()
    return students_in_group

# 7. Знайти оцінки студентів в окремій групі з певного предмета.
def select_7(group_name, subject_name):
    grades_in_group_subject = session.query(Student.name, Grade.grade, Grade.date) \
                                    .join(Group) \
                                    .join(Grade) \
                                    .join(Subject) \
                                    .filter(Group.name == group_name, Subject.name == subject_name) \
                                    .all()
    return grades_in_group_subject

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    avg_teacher_grades = session.query(func.avg(Grade.grade).label('average_grade')) \
                                .join(Subject) \
                                .join(Teacher) \
                                .filter(Teacher.name == teacher_name) \
                                .scalar()
    return avg_teacher_grades

# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_name):
    courses_taken_by_student = session.query(Subject.name) \
                                      .join(Grade) \
                                      .join(Student) \
                                      .filter(Student.name == student_name) \
                                      .all()
    return courses_taken_by_student

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    student_courses_by_teacher = session.query(Subject.name) \
                                        .join(Teacher) \
                                        .join(Grade) \
                                        .join(Student) \
                                        .filter(Student.name == student_name, Teacher.name == teacher_name) \
                                        .all()
    return student_courses_by_teacher

# 11. Середній бал, який певний викладач ставить певному студентові.
def select_11(student_name, teacher_name):
    average_grade_by_teacher = session.query(func.avg(Grade.grade).label('average_grade')) \
                                      .select_from(Student) \
                                      .join(Grade, Student.grades) \
                                      .join(Subject) \
                                      .join(Teacher) \
                                      .filter(Student.name == student_name, Teacher.name == teacher_name) \
                                      .scalar()
    return average_grade_by_teacher

# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_name, subject_name):
    subject = session.query(Subject).filter_by(name=subject_name).first()
    group = session.query(Group).filter_by(name=group_name).first()

    if not subject:
        return []

    if not group:
        return []

    grades = session.query(Grade, Student).\
        join(Student, Student.id == Grade.student_id).\
        join(Subject, Subject.id == Grade.subject_id).\
        join(Group, Group.id == Student.group_id).\
        filter(Group.name == group_name).\
        filter(Subject.name == subject_name).all()

    results = [{"grade": grade.grade, "date_received": grade.date, "student_name": student.name} for grade, student in grades]
    return results

if __name__ == '__main__':
    print(help_message)
    while True:
        try:
            select_number = int(input("Введіть номер запиту >>> "))
            if select_number == 1:
                print(select_1())
            elif select_number == 2:
                subject_name = input("Введіть назву предмета >>> ")
                print(select_2(subject_name))
            elif select_number == 3:
                subject_name = input("Введіть назву предмета >>> ")
                print(select_3(subject_name))
            elif select_number == 4:
                print(select_4())
            elif select_number == 5:
                teacher_name = input("Введіть ім'я викладача >>> ")
                print(select_5(teacher_name))
            elif select_number == 6:
                group_name = input("Введіть назву групи >>> ")
                print(select_6(group_name))
            elif select_number == 7:
                group_name = input("Введіть назву групи >>> ")
                subject_name = input("Введіть назву предмета >>> ")
                print(select_7(group_name, subject_name))
            elif select_number == 8:
                teacher_name = input("Введіть ім'я викладача >>> ")
                print(select_8(teacher_name))
            elif select_number == 9:
                student_name = input("Введіть ім'я студента >>> ")
                print(select_9(student_name))
            elif select_number == 10:
                student_name = input("Введіть ім'я студента >>> ")
                teacher_name = input("Введіть ім'я викладача >>> ")
                print(select_10(student_name, teacher_name))
            elif select_number == 11:
                student_name = input("Введіть ім'я студента >>> ")
                teacher_name = input("Введіть ім'я викладача >>> ")
                print(select_11(student_name, teacher_name))
            elif select_number == 12:
                group_name = input("Введіть назву групи >>> ")
                subject_name = input("Введіть назву предмета >>> ")
                print(select_12(group_name, subject_name))
        except ValueError:
            print("Введіть число від 1 до 12!")

#Введіть ім'я студента Susan Sawyer
#Введіть ім'я викладача >>> Martha Burke
#Введіть назву групи >>> Why Group
#Введіть назву предмета >>> Media buyer
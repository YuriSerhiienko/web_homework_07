import argparse
from database.models import Teacher, Student, Subject, Group, Grade
from database.db import session
from datetime import datetime

def create_teacher(name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    print("Вчителя створено успішно.")

def create_group(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print("Групу створено успішно.")

def create_student(name):
    student = Student(name=name)
    session.add(student)
    session.commit()
    print("Студента створено успішно.")

def create_subject(name):
    subject = Subject(name=name)
    session.add(subject)
    session.commit()
    print("Предмет створено успішно.")

def create_grade(student_name, grade_value, grade_date):
    student = session.query(Student).filter_by(name=student_name).first()
    if student:
        grade = Grade(grade=grade_value, date=grade_date)
        grade.student = student
        session.add(grade)
        session.commit()
        print("Оцінку створено успішно.")
    else:
        print("Студента з таким ім'ям не знайдено.")

def list_teachers():
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, Name: {teacher.name}")

def list_groups():
    groups = session.query(Group).all()
    for group in groups:
        print(f"ID: {group.id}, Name: {group.name}")

def list_students():
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}")

def list_subjects():
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(f"ID: {subject.id}, Name: {subject.name}")

def list_grades():
    grades = session.query(Grade).all()
    for grade in grades:
        print(f"ID: {grade.id}, Student: {grade.student.name}, Subject: {grade.subject.name}, Grade: {grade.grade}, Date: {grade.date}")

def update_teacher(teacher_id, name):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        teacher.name = name
        session.commit()
        print("Вчителя оновлено успішно.")
    else:
        print("Вчителя з таким ID не знайдено.")

def update_group(group_id, name):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        group.name = name
        session.commit()
        print("Групу оновлено успішно.")
    else:
        print("Групу з таким ID не знайдено.")

def update_student(student_id, name):
    student = session.query(Student).filter_by(id=student_id).first()
    if student:
        student.name = name
        session.commit()
        print("Студента оновлено успішно.")
    else:
        print("Студента з таким ID не знайдено.")

def update_subject(subject_id, name):
    subject = session.query(Subject).filter_by(id=subject_id).first()
    if subject:
        subject.name = name
        session.commit()
        print("Предмет оновлено успішно.")
    else:
        print("Предмет з таким ID не знайдено.")

def update_grade(grade_id, grade_value, grade_date):
    grade = session.query(Grade).filter_by(id=grade_id).first()
    if grade:
        grade.grade = grade_value
        grade.date = grade_date
        session.commit()
        print("Оцінку оновлено успішно.")
    else:
        print("Оцінку з таким ID не знайдено.")
        
def remove_group(group_name):
    group = session.query(Group).filter_by(name=group_name).first()

    if group:
        session.delete(group)
        session.commit()
        print("Групу видалено успішно.")
    else:
        print("Групу не знайдено.")

def remove_teacher(identifier):
    teacher = None
    if identifier.isdigit():
        teacher = session.query(Teacher).filter_by(id=int(identifier)).first()
    else:
        teacher = session.query(Teacher).filter_by(name=identifier).first()

    if teacher:
        session.delete(teacher)
        session.commit()
        print("Вчителя видалено успішно.")
    else:
        print("Вчителя не знайдено.")

def remove_student(identifier):
    try:
        student = session.query(Student).filter(
            (Student.id == identifier) | (Student.name == identifier)).first()

        if student:
            session.delete(student)
            session.commit()
            print(f"Студента {student.name} було успішно видалено.")
        else:
            print(f"Студента з ID або ім'ям {identifier} не знайдено.")

    except Exception as e:
        session.rollback()
        print("Під час видалення студента сталася помилка:", e)

def remove_subject(identifier):
    try:
        subject = session.query(Subject).filter(
            (Subject.id == identifier) | (Subject.name == identifier)).first()

        if subject:
            session.delete(subject)
            session.commit()
            print(f"Предмет {subject.name} було успішно видалено.")
        else:
            print(f"Предмет з ID або назвою {identifier} не знайдено.")

    except Exception as e:
        session.rollback()
        print("Під час видалення предмета сталася помилка:", e)

def remove_grade(grade_id):
    try:
        grade = session.query(Grade).filter(Grade.id == grade_id).first()

        if grade:
            session.delete(grade)
            session.commit()
            print(f"Оцінку з ID {grade_id} було успішно видалено.")
        else:
            print(f"Оцінку з ID {grade_id} не знайдено.")

    except Exception as e:
        session.rollback()
        print("Під час видалення оцінки сталася помилка:", e)

def main():
    parser = argparse.ArgumentParser(description="CLI for CRUD operations with the database.")
    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True, help="CRUD action (create, list, update, remove)")
    parser.add_argument("-m", "--model", choices=["Teacher", "Student", "Subject", "Group", "Grade"], required=True, help="Model name for CRUD operation")
    parser.add_argument("-n", "--name", help="Name of the entity to create or update")
    parser.add_argument("-i", "--id", help="ID of the entity to update or remove")

    args = parser.parse_args()

    if args.action == "create":
        if args.model == "Teacher":
            create_teacher(args.name)
        elif args.model == "Student":
            create_student(args.name)
        elif args.model == "Subject":
            create_subject(args.name)
        elif args.model == "Group":
            create_group(args.name)
        elif args.model == "Grade":
            # Зчитуємо додаткові параметри для оцінки
            grade_value = float(input("Введіть значення оцінки: "))
            grade_date_str = input("Введіть дату отримання оцінки у форматі (рррр-мм-дд): ")
            grade_date = datetime.strptime(grade_date_str, "%Y-%m-%d")
            create_grade(args.name, grade_value, grade_date)

    elif args.action == "list":
        if args.model == "Teacher":
            list_teachers()
        elif args.model == "Student":
            list_students()
        elif args.model == "Subject":
            list_subjects()
        elif args.model == "Group":
            list_groups()
        elif args.model == "Grade":
            list_grades()

    elif args.action == "update":
        if args.model == "Teacher":
            update_teacher(args.id, args.name)
        elif args.model == "Student":
            update_student(args.id, args.name)
        elif args.model == "Subject":
            update_subject(args.id, args.name)
        elif args.model == "Group":
            update_group(args.id, args.name)
        elif args.model == "Grade":
            # Зчитуємо додаткові параметри для оновлення оцінки
            grade_value = float(input("Введіть нове значення оцінки: "))
            grade_date_str = input("Введіть нову дату отримання оцінки у форматі (рррр-мм-дд): ")
            grade_date = datetime.strptime(grade_date_str, "%Y-%m-%d")
            update_grade(args.id, grade_value, grade_date)

    elif args.action == "remove":
        if args.model == "Teacher":
            if not args.id and not args.name:
                print("Для видалення вчителя потрібно вказати ID (-i) або ім'я (-n).")
            else:
                remove_teacher(args.id or args.name)
        elif args.model == "Student":
            if not args.id and not args.name:
                print("Для видалення студента потрібно вказати ID (-i) або ім'я (-n).")
            else:
                remove_student(args.id or args.name)
        elif args.model == "Subject":
            if not args.id and not args.name:
                print("Для видалення предмета потрібно вказати ID (-i) або ім'я (-n).")
            else:
                remove_subject(args.id or args.name)
        elif args.model == "Group":
            if not args.id and not args.name:
                print("Для видалення групи потрібно вказати ID (-i) або ім'я (-n).")
            else:
                remove_group(args.id or args.name)
        elif args.model == "Grade":
            if not args.id:
                print("Для видалення оцінки потрібно вказати ID (-i).")
            else:
                remove_grade(args.id)
    else:
        print("Недійсна модель. Виберіть одну з наступних: Teacher, Student, Subject, Group, Grade.")


if __name__ == "__main__":
    main()

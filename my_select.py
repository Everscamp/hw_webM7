from sqlalchemy import select, literal_column
from sqlalchemy.sql import func
from sqlalchemy import desc
from connect_db import session
from models import Tutor, Subject, Group, Student,Marks
import argparse

parser = argparse.ArgumentParser(description='Sorting folder')

parser.add_argument("one", nargs='?', default=44)
parser.add_argument("two", nargs='?', default=None)
args = vars(parser.parse_args())

var1 = args.get("one")
var2 = args.get("two")


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1(): 
    q = session.execute(
        select(Student.name, func.round(func.avg(Marks.mark)).label("average"))
        .join(Marks).group_by(Student.id).order_by(desc('average')).limit(5)
          ).mappings().all()

    return q

# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(): 
    subquery  = (
        select(func.round(func.avg(Marks.mark)).label("average"), Student.name.label('students'), Subject.name.label('subjects'))
        .join(Student).join(Subject).group_by(Student.name, Subject.name)
          ).subquery()

    q = session.execute(
        select(func.max(subquery.c.average).label("maxAverage"), subquery.c.subjects, subquery.c.students)
        .group_by(subquery.c.subjects, subquery.c.students).order_by(desc('maxAverage'))
          ).mappings().all()

    return q

# Знайти середній бал у групах з певного предмета.
def select_3(): 
    q = session.execute(
        select(func.round(func.avg(Marks.mark)).label("average"), Subject.name.label('subject'), Group.name.label('group'))
        .join(Subject, Marks.subject_id == Subject.id)
        .join(Student, Marks.student_id == Student.id)
        .join(Group, Student.group_id == Group.id).group_by('subject', 'group').order_by(desc('group'))
        .where(Subject.id == var1) #тут потрібно ввести відповідний номер
          ).mappings().all()

    return q

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4(): 

    q = session.execute(
        select(func.round(func.avg(Marks.mark)).label("average"))
          ).mappings().all()

    return q

# Знайти які курси читає певний викладач.
def select_5(): 
    q = session.execute(
        select(Subject.name.label('subject'), Tutor.name.label('tutor'))
        .join(Tutor)
        .where(Tutor.id == var1) #тут потрібно ввести відповідний номер
        .group_by(Subject.name, Tutor.name).order_by(Tutor.name)
          ).mappings().all()

    return q

# Знайти список студентів у певній групі.
def select_6(): 
    q = session.execute(
        select(Group.name.label('group'), Student.name)
        .join(Student)
        .where(Group.id == var1) #тут потрібно ввести відповідний номер
        .group_by(Student.id, Group.id).order_by('group')
          ).mappings().all()

    return q

#Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(): 
    q = session.execute(
        select(Marks.mark, Subject.name, Group.name, Student.name)
        .join(Subject, Marks.subject_id == Subject.id)
        .join(Student, Marks.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .where(Group.id == var1, Subject.id == var2)
          ).mappings().all()

    return q

#Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(): 
    q = session.execute(
        select(func.round(func.avg(Marks.mark)).label("average"), Subject.name.label('subject'), Tutor.name.label('tutor'))
        .join(Subject, Marks.subject_id == Subject.id)
        .join(Tutor, Subject.tutor_id == Tutor.id)
        .where(Tutor.id == var1) #тут потрібно ввести відповідний номер
        .group_by(Subject.name, Tutor.name)
          ).mappings().all()

    return q

#Знайти список курсів, які відвідує студент.
def select_9(): 
    q = session.execute(
        select(Subject.name.label('subject'), Student.name.label('student'))
        .join(Marks, Marks.subject_id == Subject.id)
        .join(Student, Marks.student_id == Student.id)
        .where(Student.id == var1) #тут потрібно ввести відповідний номер
        .group_by(Subject.name, Student.name)
          ).mappings().all()

    return q

#Список курсів, які певному студенту читає певний викладач.
def select_10(): 
    q = session.execute(
        select(Subject.name.label('subject'), Student.name.label('student'), Tutor.name.label('student'))
        .join(Marks, Marks.subject_id == Subject.id)
        .join(Student, Marks.student_id == Student.id)
        .join(Tutor, Subject.tutor_id == Tutor.id)
        .where(Student.id == var1, Tutor.id == var2) #тут потрібно ввести відповідний номер
        .group_by(Subject.name, Student.name, Tutor.name)
          ).mappings().all()

    return q

# Середній бал, який певний викладач ставить певному студентові.
def select_extra_1(): 
    q = session.execute(
        select(func.round(func.avg(Marks.mark)).label("average"), Student.name.label('student'), Tutor.name.label('tutor'))
        .join(Subject, Marks.subject_id == Subject.id)
        .join(Student, Marks.student_id == Student.id)
        .join(Tutor, Subject.tutor_id == Tutor.id)
        .where(Tutor.id == var1, Student.id == var2) #тут потрібно ввести відповідний номер
        .group_by(Student.name, Tutor.name)
          ).mappings().all()

    return q

# -- Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_extra_2(): 
    q = session.execute(
        select(Marks.mark, Subject.name.label('subjects'), Group.name.label('group'), Student.name.label('student'), \
            func.max(Marks.date).label("lastDate"))
            .join(Student, Marks.student_id == Student.id)
            .join(Subject, Marks.subject_id == Subject.id)
            .join(Group, Student.group_id == Group.id)
            .where(Group.id == var1, Subject.id == var2) #тут потрібно ввести відповідний номер
            .group_by(Student.name, Marks.mark, 'subjects', 'group')
            ).mappings().all()

    return q

if __name__ == '__main__':
    print(select_1())
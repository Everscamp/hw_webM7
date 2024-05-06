import random
from datetime import datetime
from psycopg2 import DatabaseError

import faker

from connect_db import session
from models import Tutor, Subject, Group, Student,Marks

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_TUTORS = 5
NUMBER_SUBJECTS = 8
NUMBER_MARKS = 20

fake_data = faker.Faker()

def make_tutors():    
    for i in range(NUMBER_TUTORS):
        tutor = Tutor(name = fake_data.name())
        session.add(tutor)
    session.commit()
    

def make_subjects():
    tutors = session.query(Tutor).all()
    for i in range(NUMBER_SUBJECTS):
        subject = Subject(name = fake_data.job(),
            tutor_id = random.choice(tutors).id
            )
        session.add(subject)
    session.commit()

def make_groups():
    for i in range(NUMBER_GROUPS):
        group = Group(name = f'{fake_data.random_number(1,50)} {fake_data.random_uppercase_letter()}')
        session.add(group)
    session.commit()

def make_students():
    groups = session.query(Group).all()
    for i in range(NUMBER_STUDENTS):
        student = Student(name = fake_data.name(),
            group_id = random.choice(groups).id
            )
        session.add(student)
    session.commit()
    
 
def make_marks():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    for i in range(1, (len(list(students)))+1):
            for m in range(1, NUMBER_MARKS+1):
                mark = Marks(mark = random.randint(1, 5),
                subject_id = random.choice(subjects).id,
                student_id = random.choice(students).id,
                date = fake_data.date_time_between(datetime(2019,1,1), datetime.today())
            )
 
            session.add(mark)
    session.commit()


if __name__ == '__main__':
    try:
        make_tutors()
        make_subjects()
        make_groups()
        make_students()
        make_marks()
        session.commit()
    except DatabaseError as e:
        print(e)
        session.rollback()
    finally:
        session.close()

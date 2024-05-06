import argparse
import random
from sqlalchemy import select, update, delete
from psycopg2 import DatabaseError

from connect_db import session
from models import Tutor, Subject, Group, Student,Marks

models = {
    'tutor': Tutor,
    'subject': Subject,
    'group': Group,
    'student': Student,
    'mark': Marks
} 

parser = argparse.ArgumentParser(description='Queries')
parser.add_argument('--a', '--action', required=True)
parser.add_argument('--m', '--model', required=True)
parser.add_argument('--n', '--name', default=None)
parser.add_argument('--id', default=None)
parser.add_argument('--mark', default=None)
parser.add_argument('--t_id', '--tutor_id', default=None)
parser.add_argument('--sub_id', '--subject_id', default=None)
parser.add_argument('--s_id', '--student_id', default=None)
parser.add_argument('--g_id', '--group_id', default=None)

args = vars(parser.parse_args())

def run_query():
    if args['a'] == 'list':
        model = args['m']
        q = session.execute(
            select(models.get(model))
            ).mappings().all()
        return q

    if args['a'] == 'create':
        model = args['m']
        if model == 'subject' and args['n'] != None:
            tutors = session.query(Tutor).all()
            subject = Subject(name = args['n'],
            tutor_id = args['id'] if args['id'] else random.choice(tutors).id
            )
            session.add(subject)
            session.commit()

        elif model == 'student' and args['n'] != None:
            groups = session.query(Group).all()
            student = Student(name = args['n'],
            group_id = args['id'] if args['id'] else random.choice(groups).id
            )
            session.add(student)
            session.commit()

        elif model == 'mark' and args['mark'] != None:
            students = session.query(Student).all()
            subjects = session.query(Subject).all()
            mark = Marks(mark = args['mark'],
            student_id = args['id'] if args['id'] else random.choice(students).id,
            subject_id = args['id'] if args['id'] else random.choice(subjects).id
            )
            session.add(mark)
            session.commit()

        elif args['n'] != None:
            modelName = models.get(model)
            modelType = modelName(name = args['n'])
            session.add(modelType)
            session.commit()

        q = session.execute(
            select(models.get(model))
            ).mappings().all()
        return q

    if args['a'] == 'update':
        model = args['m']

        if model == 'mark' and args['mark'] != None:
            session.execute(update(models.get(model))
            .where(models.get(model).id == args['id'])
            .values(mark = args['mark'])
            )
            session.commit()
# цю частину можна іще розширити додавши можливість редагувати не тільки назви/імена 
# а й зовнішні ключі груп для студентів і вчителів для предметів
        elif args['id'] != None and args['n'] != None:
            session.execute(update(models.get(model))
            .where(models.get(model).id == args['id'])
            .values(name = args['n'])
            )
            session.commit()

        q = session.execute(
            select(models.get(model))
            ).mappings().all()
        return q

    if args['a'] == 'remove':
        model = args['m']
        if args['id'] != None:
            session.execute(delete(models.get(model))
            .where(models.get(model).id == args['id'])
            )
            session.commit()

        q = session.execute(
            select(models.get(model))
            ).mappings().all()
        return q


if __name__ == "__main__":
    try:
        print(run_query())

    except DatabaseError as e:
        print(e)
        session.rollback()
    finally:
        session.close()

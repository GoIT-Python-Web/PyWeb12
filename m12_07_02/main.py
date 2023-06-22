from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from database.db import session
from database.models import Student, Teacher, Contact, TeacherStudent


def get_students_join():
    students = session.query(Student).join(Student.teachers).all()
    for s in students:
        columns = ["id", "fullname", "teachers"]
        rd = [dict(zip(columns, (s.id, s.fullname, [(t.id, t.fullname) for t in s.teachers])))]
        print(rd)


def get_students():
    students = session.query(Student).options(joinedload(Student.teachers)).limit(5).offset(5).all()
    for s in students:
        columns = ["id", "fullname", "teachers"]
        rd = [dict(zip(columns, (s.id, s.fullname, [(t.id, t.fullname) for t in s.teachers])))]
        print(rd)


def get_teachers():
    teachers = session.query(Teacher).options(joinedload(Teacher.students, innerjoin=True)).order_by(Teacher.id).all()
    for t in teachers:
        columns = ["id", "fullname", "students"]
        rd = [dict(zip(columns, (t.id, t.fullname, [(s.id, s.fullname) for s in t.students])))]
        print(rd)


def get_teachers_join():
    teachers = session.query(Teacher).outerjoin(Teacher.students).order_by(Teacher.id).all()
    for t in teachers:
        columns = ["id", "fullname", "students"]
        rd = [dict(zip(columns, (t.id, t.fullname, [(s.id, s.fullname) for s in t.students])))]
        print(rd)


def get_teachers_filter():
    teachers = session.query(Teacher).options(joinedload(Teacher.students, innerjoin=True)) \
        .filter(and_(Teacher.start_work > datetime(year=2022, month=2, day=24),
                     Teacher.start_work < datetime(year=2023, month=6, day=22)
                     )).order_by(Teacher.id).all()

    for t in teachers:
        columns = ["id", "fullname", "students"]
        rd = [dict(zip(columns, (t.id, t.fullname, [(s.id, s.fullname) for s in t.students])))]
        print(rd)


def get_students_join_next():
    students = session.query(Student).join(Student.teachers).join(Student.contacts).all()
    for s in students:
        columns = ["id", "fullname", "teachers", "contacts"]
        rd = [dict(zip(columns, (
            s.id, s.fullname, [(t.id, t.fullname) for t in s.teachers], [(c.id, c.fullname) for c in s.contacts])))]
        print(rd)


def custom_get_students_join_next():
    students = session.query(Student.id, Student.fullname, Teacher.fullname.label("teacher_fullname"),
                             Contact.fullname.label("contact_fullname"))\
        .select_from(Student).join(TeacherStudent).join(Teacher).join(Contact).all()

    for s in students:
        columns = ["id", "fullname", "teachers", "contacts"]
        rd = [dict(zip(columns, (
            s.id, s.fullname, s.teacher_fullname, s.contact_fullname)))]
        print(rd)


if __name__ == '__main__':
    # get_students_join()
    get_students()
    # get_teachers()
    # print('----------------')
    # get_teachers_join()
    # get_teachers_filter()
    # get_students_join_next()
    # custom_get_students_join_next()

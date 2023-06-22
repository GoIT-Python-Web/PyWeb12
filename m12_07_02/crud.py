from typing import List

from faker import Faker
from sqlalchemy import select

from database.db import session
from database.models import Student, Teacher

fake = Faker()


def add_student(teachers):
    student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            teachers=teachers
        )
    session.add(student)
    session.commit()
    return student


def update_student(student_id, teachers: List[Teacher]):
    student = session.query(Student).filter_by(id=student_id).first()
    student.teachers = teachers
    session.commit()
    return student


def remove_student(student_id):
    # student = session.query(Student).filter_by(id=student_id).first()
    student = session.execute(select(Student).filter_by(id=student_id)).scalar_one_or_none()
    session.delete(student)
    session.commit()


if __name__ == '__main__':
    teachers = session.query(Teacher).filter(Teacher.id.in_([1, 2, 3])).all()
    st = add_student(teachers)
    print(st.fullname)
    new_teachers = session.query(Teacher).filter(Teacher.id.in_([4, 5, 3])).all()
    st = update_student(st.id, new_teachers)
    print(st.fullname)
    remove_student(st.id)
    session.close()
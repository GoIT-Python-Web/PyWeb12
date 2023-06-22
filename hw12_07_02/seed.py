from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session

'''
Создаем свою ф-цию для получения списка дат, в которые происходит учебный процесс.
Для упрощения выбрасываем только дни, которые попадают на выходные.
'''


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


'''
Функция создания БД, в качестве параметра - передаем путь к файлу с SQL скриптом
'''

'''Функция генерации фейковых данных и заполнения ими БД'''


def fill_data():
    # Не все данные будут динамические. Создаем списки предметов и групп
    disciplines = ['Вища математика', 'Хімія', 'Економіка підприємства', 'Обчислювальна математика', 'Історія України',
                   'Теоретична механіка', 'Менеджмент організацій', 'Системне програмування']

    groups = ['ВВ1', 'ДД33', 'АА5']

    # Создаем объект библиотеки Faker. В качестве параметра передаем local 'uk-UA'
    # Больше - https://faker.readthedocs.io/en/master/locales.html
    fake = faker.Faker()
    number_of_teachers = 5
    number_of_students = 50

    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        # дата начала учебного процесса
        start_date = datetime.strptime("2020-09-01", "%Y-%m-%d")
        # дата окончания учебного процесса
        end_date = datetime.strptime("2021-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:  # пройдемся по каждой дате
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]
            # проходимся по списку "везучих" студентов, добавляем их в результирующий список
            # и генерируем оценку
            for student_id in random_ids_student:
                grade = Grade(grade=randint(1, 12), date_of=d, student_id=student_id,
                              discipline_id=random_id_discipline)
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == '__main__':
    fill_data()

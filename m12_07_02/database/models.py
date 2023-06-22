from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, event, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    email = Column(String(100))
    phone = Column("cell_phone", String(120))
    address = Column(String(120))
    start_work = Column(Date, nullable=False)
    students = relationship(
        "Student", secondary="teachers_to_students", back_populates="teachers"
    )

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Student(Base):
    __tablename__ = "students"
    id = Column("id", Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    email = Column(String(100))
    phone = Column("cell_phone", String(120))
    address = Column(String(120))
    teachers = relationship(
        "Teacher", secondary="teachers_to_students", back_populates="students"
    )

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Contact(Base):
    __tablename__ = "contacts"
    id = Column("id", Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    email = Column(String(100))
    phone = Column("cell_phone", String(120))
    address = Column(String(120))
    student_id = Column('student_id', ForeignKey("students.id", ondelete="CASCADE", onupdate="CASCADE"))
    student = relationship("Student", backref="contacts")

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class TeacherStudent(Base):
    __tablename__ = "teachers_to_students"
    id = Column("id", Integer, primary_key=True)
    teacher_id = Column(
        Integer, ForeignKey("teachers.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    student_id = Column(
        Integer, ForeignKey("students.id", ondelete="CASCADE", onupdate="CASCADE")
    )

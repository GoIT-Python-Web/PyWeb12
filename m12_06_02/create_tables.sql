DROP TABLE IF EXISTS [groups];
CREATE TABLE [groups] (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING UNIQUE
);

DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname STRING
);

DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname STRING,
    group_id REFERENCES [groups] (id)
);

DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING UNIQUE,
    teacher_id REFERENCES teachers (id)
);

DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id REFERENCES students(id),
    subject_id REFERENCES subjects(id),
    grade INTEGER NOT NULL,
    date_of DATE
);

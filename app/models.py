import sys
sys.path.append('../venv/Lib/site-packages')
import pymysql
from . import db
from datetime import datetime, timedelta

Student_Course = db.Table("Student_Course",
                          db.Column('id', db.INTEGER, primary_key=True, autoincrement=True),
                          db.Column('student_sno', db.String(20), db.ForeignKey('Student.sno')),
                          db.Column('Course_sno', db.String(20), db.ForeignKey('Course.sno')))
Teacher_Course = db.Table("Teacher_Course",
                          db.Column('id', db.INTEGER, primary_key=True, autoincrement=True),
                          db.Column('teacher_sno', db.String(20), db.ForeignKey('Teacher.sno')),
                          db.Column('Course_sno', db.String(20), db.ForeignKey('Course.sno')))
# Tools_Course = db.Table("Tools_Course",
#                           db.Column('id', db.INTEGER, primary_key=True, autoincrement=True),
#                           db.Column("Tools_sno", db.String(20), db.ForeignKey('Tools.sno')),
#                           db.Column('course_sno', db.String(64), db.ForeignKey('Course.sno'))
# )

#创建学生表
class Student(db.Model):
    __tablename__ = "Student"
    sno = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False, default=sno)
    classes = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(11))
    email = db.Column(db.String(64))
    course = db.relationship('Course', secondary=Student_Course, backref=db.backref("Student", lazy='dynamic'))

class Teacher(db.Model):
    __tablename__ = "Teacher"
    sno = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False, default=sno)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    office = db.Column(db.String(64))
    course = db.relationship('Course', secondary=Teacher_Course, backref=db.backref("Teacher", lazy='dynamic'))


class Course(db.Model):
    __tablename__ = "Course"
    sno = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False, default=start_time+2)


class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    sno = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False, default=sno)
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))



class Tools(db.Model):
    __tablename__ = "Tools"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    sno = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(64), nullable=False)
  #  course = db.relationship('Course', secondary=Tools_Course, backref=db.backref("Tools", lazy='dynamic'))


class Booking_student(db.Model):
    __tablename__ = "Booking_student"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    course_sno = db.Column(db.String(20), db.ForeignKey("Course.sno"))

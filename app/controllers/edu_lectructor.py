from flask import request
from app import db
from sqlalchemy import delete
from app.models import User_Role, Role_Permission, Lecturer_Assignment

def get_lecturers():
    result = db.session.query(User_Role)\
         .join(Role_Permission, User_Role.role_id == Role_Permission._id)\
         .filter(Role_Permission.role_name == "講師").all()
    r = {}
    for row in result:
        r[row.emp_id] = row.emp.name
    return r
def get_lecturer_assignments():
    result = db.session.query(Lecturer_Assignment).all()
    r = {}
    for row in result:
        course_info = {
            'id': row.course._id,
            'name': row.course.name,
            'engaged_emp_num': row.course.engaged_emp_num,
            'start_date': row.course.course_start_date.strftime("%Y-%m-%d"),
            'end_date': row.course.course_end_date.strftime("%Y-%m-%d"),
            'start_time': row.course.course_start_time.strftime("%H:%M:%S"),
            'end_time': row.course.course_end_time.strftime("%H:%M:%S")
            }
        lecturer_info = {
            'id': row.emp._id,
            'name': row.emp.name,
            'rating':row.lecturer_rating
        }
        r[row._id] = {'course': course_info,
                      'lecturer': lecturer_info,}
    return r
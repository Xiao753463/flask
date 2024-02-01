from flask import Flask, request, redirect, url_for, send_from_directory
from app import app, db
from app.models import Course, Product, Department, Unit, Course_assignment
from sqlalchemy import delete, func
from werkzeug.utils import secure_filename
import sys, os
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_class(class_name):
    return getattr(sys.modules[__name__], class_name)
def cre_courses():
    name = request.args.get('name')
    duration = request.args.get('duration')
    dept = request.args.get('dept')
    prod = request.args.get('prod')
    unit = request.args.get('unit')
    knowledge_point = request.args.get('knowledge_point')
    desc = request.args.get('desc')
    file = request.files['file']
    course = Course(
        name = name,
        duration = duration,
        dept = dept,
        prod = prod,
        unit = unit,
        knowledge_point = knowledge_point,
        desc = desc
    )
    db.session.add(course)
    db.session.flush()
    db.session.refresh(course)
    course_folder = os.path.join(app.root_path, 'static', str(course._id))
    if not os.path.exists(course_folder):
        os.makedirs(course_folder)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(course_folder, filename))
    try:
        db.session.commit()
        return ('Course create successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course create error!')
        raise
    else:
        db.session.commit()
def get_courses():
    result = db.session.query(Course._id, Course.name, func.count(Course_assignment.eid).label('enrollment_count')) \
    .join(Course_assignment) \
    .group_by(Course._id) \
    .all()
    r = {}
    for row in result:
        r[row._id]= {'name': row.name,
           'enrollment_count': row.enrollment_count,
           }
    return r
def del_courses():
    numbers = request.args.getlist('nums[]')
    sql = delete(Course).where(Course._id.in_(numbers))
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course deleted error!')
        raise
    else:
        db.session.commit()
def upd_courses():
    numbers = request.args.getlist('nums[]')
    sql = delete(Course).where(Course.number.in_(numbers) )
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course deleted error!')
        raise
    else:
        db.session.commit()

def get_info():
    table = request.args.get('table')
    result = db.session.query(get_class(table)).all()
    return result

   
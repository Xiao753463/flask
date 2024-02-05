from flask import Flask, request
from app import db
from app.models import Course, Item_1, Item_2, Item_3, Product, Department, Unit, Course_Assignment, Course_Document, Lecturer_Assignment, Role_Permission, User_Role
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr
import sys, json

class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Row):
            data = {}
            for obj in o:
                data.update(self.parse_sqlalchemy_object(obj))
            return data
        if isinstance(o.__class__, DeclarativeMeta):
            return self.parse_sqlalchemy_object(o)
        return json.JSONEncoder.default(self, o)

    def parse_sqlalchemy_object(self, o):
        data = {}
        fields = o.__json__() if hasattr(o, '__json__') else dir(o)
        for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class', 'registry']]:
            value = o.__getattribute__(field)
            try:
                json.dumps(value)
                data[field] = value
            except TypeError:
                data[field] = None
        return data


        return json.JSONEncoder.default(self, obj)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_class(class_name):
    return getattr(sys.modules[__name__], class_name)
def cre_courses():
    item_1_id = request.args.get('item_1_id')
    name = request.args.get('name')
    duration = request.args.get('duration')
    dept = request.args.get('dept')
    unit = request.args.get('unit')
    desc = request.args.get('desc')
    course = Course(
        item_1_id = item_1_id,
        name = name,
        duration = duration,
        dept = dept,
        unit = unit,
        desc = desc,
    )
    db.session.add(course)
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
    # result = db.session.query(Course, Course_Assignment).join(Course_Assignment, full=True).filter(Course._id == Course_Assignment.cid).all()
    # json_object = json.dumps(result, cls=AlchemyEncoder, ensure_ascii=False).encode('utf8')
    # return json_object
    result = db.session.query(Course, func.count(Course_Assignment.eid).label('enrollment_count')) \
        .outerjoin(Course_Assignment, Course._id == Course_Assignment.cid) \
        .options(joinedload(Course.course_ca)).group_by(Course._id) \
        .all()

    r = {}
    for row in result:
        course_details = {
            'name': row.Course.name,
            'item1': row.Course.item_1.name,
            'duration': row.Course.duration,
            'department': row.Course.dept.name,
            'unit': row.Course.unit.name,
            # 'product': row.Course.prod.name,
            'description': row.Course.desc,
            'enrollment_count': row.enrollment_count,
            'engaged_emp_num': row.Course.engaged_emp_num,
            'course_start_date': row.Course.course_start_date.strftime("%Y-%m-%d"),
            'course_end_date': row.Course.course_end_date.strftime("%Y-%m-%d"),
            'course_start_time': row.Course.course_start_time.strftime("%H:%M:%S"),
            'course_end_time': row.Course.course_end_time.strftime("%H:%M:%S")
        }

        # Include the enrollment details if available
        if row.Course.course_ca:
            enrollment_list = [
                {'employee_id': enrollment.emp._id, 'employee_code': enrollment.emp.code, 'employee_name': enrollment.emp.name}
                for enrollment in row.Course.course_ca
            ]
            course_details['enrollment_list'] = enrollment_list

        r[row.Course._id] = course_details

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
def upd_course():
    id = request.args.get('id')
    iid = request.args.get('iid')
    name = request.args.get('name')
    duration = request.args.get('duration')
    did = request.args.get('did')
    uid = request.args.get('uid')
    desc = request.args.get('desc')
    course = Course.query.get(id)
    course.name = name
    course.duration = duration
    course.item_1_id = iid
    course.did = did
    course.uid = uid
    course.desc = desc
    try:
        db.session.commit()
        return ('Course updated successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course updated error!')
        raise
    else:
        db.session.commit()


def add_course():
    id = request.args.get('id') 
    emp_id = request.args.get('emp_id')
    engaged_emp_num = request.args.get('engaged_emp_num')
    course_start_date = request.args.get('course_start_date')
    course_end_date = request.args.get('course_end_date')
    course_start_time = request.args.get('course_start_time')
    course_end_time = request.args.get('course_end_time')
    rating = request.args.get('rating')
    course = Course.query.get(id)
    course.engaged_emp_num = engaged_emp_num
    course.course_start_date = course_start_date
    course.course_end_date = course_end_date
    course.course_start_time = course_start_time
    course.course_end_time = course_end_time
    assign = Lecturer_Assignment(
        emp_id = emp_id,
        course_id = id,
        rating = rating
    )
    db.session.add(assign)
    try:
        db.session.commit()
        return ('Assignment create successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Assignment create error!')
        raise
    else:
        db.session.commit()
def del_element(table):
    id = request.args.get('id')
    sql = delete(get_class(table)).where(get_class(table)._id == id)
    db.session.execute(sql)
    try:
        db.session.commit()
        return (table + ' deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return (table + ' deleted error!')
        raise
    else:
        db.session.commit()
def get_item_1():
    result = db.session.query(Item_1).all()
    r = {}
    for row in result:
        r[row._id] = row.name
    return r
def add_member():
    eid = request.args.get('eid')
    cid = request.args.get('cid')
    ca = Course_Assignment(
        eid = eid,
        cid = cid,
    )
    db.session.add(ca)
    try:
        db.session.commit()
        return ('Member assign successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Member assign error!')
        raise
    else:
        db.session.commit()
def remove_member():
    eid = request.args.get('eid')
    cid = request.args.get('cid')
    sql = delete(Course_Assignment).where(Course_Assignment.eid == eid).where(Course_Assignment.cid == cid)
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course_Assignment deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course_Assignment deleted error!')
        raise
    else:
        db.session.commit()
    

   
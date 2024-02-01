from app import app, db
from dataclasses import dataclass
# Creating the Inserttable for inserting data into the database
@dataclass
class Product(db.Model):
    __tablename__ = 'product'
    _id:int = db.Column('product_id', db.Integer, primary_key=True)
    name:str = db.Column('product_name', db.String(30))
    prod_c = db.relationship("Course", backref="prod", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name):
        self.name = name

@dataclass
class Department(db.Model):
    __tablename__ = 'department'
    _id:int = db.Column('department_id', db.Integer, primary_key=True)
    name:str = db.Column('department_name', db.String(30))
    dept_c = db.relationship("Course", backref="dept", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name):
        self.name = name

@dataclass
class Unit(db.Model):
    __tablename__ = 'unit'
    _id:int = db.Column('unit_id', db.Integer, primary_key=True)
    name:str = db.Column('unit_name', db.String(30))
    unit_c = db.relationship("Course", backref="unit", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name):
        self.name = name


@dataclass
class Course(db.Model):
    __tablename__ = 'course'
    _id:int = db.Column('course_id', db.Integer, primary_key=True)
    name:str = db.Column('course_name', db.String(30))
    duration:int = db.Column('course_duration', db.Integer)
    did:int = db.Column('department_id', db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    pid:int = db.Column('product_id', db.Integer, db.ForeignKey('product.product_id', ondelete="CASCADE"))
    uid:int = db.Column('unit_id', db.Integer, db.ForeignKey('unit.unit_id', ondelete="CASCADE"))
    knowledge_point:str = db.Column('knowledge_point', db.String(100))
    desc:str = db.Column('course_description', db.String(900), nullable=True)
    course_ca = db.relationship("Course_assignment", backref="course", cascade="all, delete", passive_deletes=True,)
    def __init__(self, name, duration, did, pid, uid, knowledge_point, desc):
        self.name = name
        self.duration = duration
        self.did = did
        self.pid = pid
        self.uid = uid
        self.knowledge_point = knowledge_point
        self.desc = desc

@dataclass
class Employee(db.Model):
    __tablename__ = 'employee_static_info'
    _id:int = db.Column('emp_id', db.Integer, primary_key=True)
    code:str = db.Column('emp_code', db.String(10))
    name:str = db.Column('emp_name', db.String(30))
    dept:int = db.Column('department_id', db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    pos:str = db.Column('position', db.String(30))
    gender:str = db.Column('gender', db.String(10))
    birth:str = db.Column('birth', db.Date)
    address:str = db.Column('address', db.String(50))
    phone:str = db.Column('phone', db.String(10))
    mobilephone:str = db.Column('mobilephone', db.String(10))
    email:str = db.Column('email', db.String(30))
    account_enabled:str = db.Column('account_enabled', db.String(10))
    emp_ca = db.relationship("Course_assignment", backref="emp", cascade="all, delete", passive_deletes=True,)

    def __init__(self, code, name):
        self.code = code
        self.name = name

@dataclass  
class Course_assignment(db.Model):
    __tablename__ = 'course_assignment'
    _id:int = db.Column('assignment_id', db.Integer, primary_key=True)
    eid:int = db.Column('emp_id', db.Integer, db.ForeignKey('employee_static_info.emp_id', ondelete="CASCADE"))
    cid:int = db.Column('course_id', db.Integer, db.ForeignKey('course.course_id', ondelete="CASCADE"))

    def __init__(self, eid, cid):
        self.eid = eid
        self.cid = cid
# 新增產品
# p1 = Employee('8888', 'Isacc')
# p2 = Employee('9999', 'Dennis')
# p3 = Employee('7777', 'Joey')
 
# 新增使用者
app.app_context().push()
cascade_setting = Course.course_ca.property.cascade
print("Cascade setting:", cascade_setting)

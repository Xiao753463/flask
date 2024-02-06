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
class Item_1(db.Model):
    __tablename__ = 'item_1'
    _id:int = db.Column('item_1_id', db.Integer, primary_key=True)
    name:str = db.Column('name', db.String(10))

    Item_1_c = db.relationship("Course", backref="item_1", cascade="all, delete", passive_deletes=True,)
    Item_1 = db.relationship("Item_2", backref="item_1", cascade="all, delete", passive_deletes=True,)
    def __init__(self, name):
        self.name = name
    def get_item_3_list(self):
        # Retrieve all associated Item_3 instances through Item_2
        item_3_list = [item_2.Item_2 for item_2 in self.Item_1]
        return item_3_list
@dataclass
class Item_2(db.Model):
    __tablename__ = 'item_2'
    _id:int = db.Column('item_2_id', db.Integer, primary_key=True)
    item_1_id:int = db.Column('item_1_id', db.Integer, db.ForeignKey('item_1.item_1_id', ondelete="CASCADE"))
    name:str = db.Column('name', db.String(10))

    Item_2 = db.relationship("Item_3", backref="item_2", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, name, item_1_id):
        self.name = name
        self.item_1_id = item_1_id
@dataclass
class Item_3(db.Model):
    __tablename__ = 'item_3'
    _id:int = db.Column('item_3_id', db.Integer, primary_key=True)
    item_2_id:int = db.Column('item_2_id', db.Integer, db.ForeignKey('item_2.item_2_id', ondelete="CASCADE"))
    name:str = db.Column('name', db.String(10))

    
    def __init__(self, name, item_2_id):
        self.name = name
        self.item_2_id = item_2_id
@dataclass
class Course(db.Model):
    __tablename__ = 'course'
    _id:str = db.Column('course_id', db.String(10), primary_key=True)
    item_1_id:int = db.Column('item_1_id', db.Integer, db.ForeignKey('item_1.item_1_id', ondelete="CASCADE"))
    name:str = db.Column('course_name', db.String(30))
    duration:int = db.Column('course_duration', db.Integer)
    did:int = db.Column('department_id', db.Integer, db.ForeignKey('department.department_id', ondelete="CASCADE"))
    pid:int = db.Column('product_id', db.Integer, db.ForeignKey('product.product_id', ondelete="CASCADE"), nullable=True)
    uid:int = db.Column('unit_id', db.Integer, db.ForeignKey('unit.unit_id', ondelete="CASCADE"))
    desc:str = db.Column('course_description', db.String(900), nullable=True)
    engaged_emp_num:int = db.Column(db.Integer)
    course_start_date:str = db.Column(db.Date)
    course_end_date:str = db.Column(db.Date)
    course_start_time:str = db.Column(db.Time)
    course_end_time:str = db.Column(db.Time)
    course_ca = db.relationship("Course_Assignment", backref="course", cascade="all, delete", passive_deletes=True,)
    course_la = db.relationship("Lecturer_Assignment", backref="course", cascade="all, delete", passive_deletes=True,)
    course_doc = db.relationship("Course_Document", backref="course", cascade="all, delete", passive_deletes=True,)
    
    def __init__(self, _id, item_1_id, name, duration, did, uid,  desc, engaged_emp_num=None, 
                 course_start_date=None, course_end_date=None, 
                 course_start_time=None, course_end_time=None):
        self._id = _id
        self.item_1_id = item_1_id
        self.name = name
        self.duration = duration
        self.did = did
        self.uid = uid
        self.desc = desc
        self.engaged_emp_num = engaged_emp_num
        self.course_start_date = course_start_date
        self.course_end_date = course_end_date
        self.course_start_time = course_start_time
        self.course_end_time = course_end_time

@dataclass
class Course_Document(db.Model):
    __tablename__ = 'course_document'
    _id:int = db.Column('course_document_id', db.Integer, primary_key=True)
    cid:str = db.Column('course_id', db.String(10), db.ForeignKey('course.course_id', ondelete="CASCADE"))
    name:str = db.Column('course_document_name', db.String(30))
    time:str = db.Column('update_time', db.Date)
    editor:str = db.Column('editor', db.String(10), db.ForeignKey('employee_static_info.emp_code', ondelete="CASCADE"))
    desc:str = db.Column('document_description', db.String(900))

    def __init__(self, cid, name, time, editor, desc):
        self.cid = cid
        self.name = name
        self.time = time
        self.editor = editor
        self.desc = desc
@dataclass
class Employee(db.Model):
    __tablename__ = 'employee_static_info'
    _id:int = db.Column('emp_id', db.Integer, primary_key=True)
    code:str = db.Column('emp_code', db.String(10), unique=True)
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
    emp_ca = db.relationship("Course_Assignment", backref="emp", cascade="all, delete", passive_deletes=True)
    emp_ur = db.relationship("User_Role", backref="emp", cascade="all, delete", passive_deletes=True)
    emp_la = db.relationship("Lecturer_Assignment", backref="emp", cascade="all, delete", passive_deletes=True)

    def __init__(self, code, name, dept, pos, gender, birth):
        self.code = code
        self.name = name
        self.dept = dept
        self.pos = pos
        self.gender = gender
        self.birth = birth
@dataclass
class Role_Permission(db.Model):
    __tablename__ = 'role_permission'
    _id = db.Column('role_permission_id', db.Integer, primary_key=True)
    role_name = db.Column(db.String(30))
    role_description = db.Column(db.String(900))
    permission_name = db.Column(db.String(30))
    permission = db.Column(db.String(30))

    def __init__(self, role_name, role_description, permission_name, permission):
        self.role_name = role_name
        self.role_description = role_description
        self.permission_name = permission_name
        self.permission = permission

@dataclass
class User_Role(db.Model):
    __tablename__ = 'user_role'
    _id:int = db.Column('relation_id', db.Integer, primary_key=True)
    role_id:int = db.Column(db.Integer, db.ForeignKey('role_permission.role_permission_id'))
    emp_code:str = db.Column(db.String(10), db.ForeignKey('employee_static_info.emp_code', ondelete="CASCADE"))
    emp_role_start:str = db.Column(db.Date, nullable=True)
    emp_role_end:str = db.Column(db.Date, nullable=True)

    def __init__(self, role_id, emp_code, emp_role_start = None, emp_role_end = None):
        self.role_id = role_id
        self.emp_code = emp_code
        self.emp_role_start = emp_role_start
        self.emp_role_end = emp_role_end

@dataclass
class Lecturer_Assignment(db.Model):
    __tablename__ = 'lecturer_assignment'
    _id:int = db.Column('lecturer_assignment_id', db.Integer, primary_key=True)
    emp_code:str = db.Column(db.String(10), db.ForeignKey('employee_static_info.emp_code', ondelete="CASCADE"))
    course_id:str = db.Column(db.String(10), db.ForeignKey('course.course_id', ondelete="CASCADE"))
    lecturer_rating:int = db.Column(db.Integer, nullable=True)
    
    def __init__(self, emp_code, course_id, rating=None):
        self.emp_code = emp_code
        self.course_id = course_id
        self.rating = rating
@dataclass  
class Course_Assignment(db.Model):
    __tablename__ = 'course_assignment'
    _id:int = db.Column('assignment_id', db.Integer, primary_key=True)
    emp_code:str = db.Column(db.String(10), db.ForeignKey('employee_static_info.emp_code', ondelete="CASCADE"))
    cid:str = db.Column('course_id', db.String(10), db.ForeignKey('course.course_id', ondelete="CASCADE"))
    def __init__(self, emp_code, cid):
        self.emp_code = emp_code
        self.cid = cid
# 新增產品
app.app_context().push()
db.drop_all()
db.create_all()
i1_1 = Item_1("test1-1")
i1_2 = Item_1("test1-2")
i2_1 = Item_2("test2-1", 1)
i2_2 = Item_2("test2-2", 2)
i2_3 = Item_2("test2-3", 2)
i3_1 = Item_3("test3-1", 3)
i3_2 = Item_3("test3-2", 1)
i3_3 = Item_3("test3-3", 1)
p1 = Employee("E001",	"人員A",	"3",	"A",	"男",	"1992-05-22")
p2 = Employee("E002",	"人員B",	"2",	"B",	"女",	"1998-10-13")
p3 = Employee("E003",	"人員C",	"1",	"C",	"女",	"1954-07-26")
prod1 = Product("產品A")
prod2 = Product("產品B")
prod3 = Product("產品C")
prod4 = Product("產品D")
prod5 = Product("產品E")
u1 = Unit("單位A")
u2 = Unit("單位B")
u3 = Unit("單位C")
u4 = Unit("單位D")
u5 = Unit("單位E")
d1 = Department("部門A")
d2 = Department("部門B")
d3 = Department("部門C")
d4 = Department("部門D")
d5 = Department("部門E")
c1 = Course('C001', 1, "課程A", 2, 3, 3, "desc", 30, "2024-02-04", "2024-03-30", "09:00:00","12:00:00")
c2 = Course('C002', 2, "課程B", 4, 2, 1, "desc", 30, "2024-02-04", "2024-03-30", "09:00:00","12:00:00")
c3 = Course('C003', 2, "課程C", 3, 1, 1, "desc", 30, "2024-02-04", "2024-03-30", "09:00:00","12:00:00")
ca1 = Course_Assignment('E001','C001')
ca2 = Course_Assignment('E001','C002')
ca3 = Course_Assignment('E002','C002')
ca4 = Course_Assignment('E003','C002')
la1 = Lecturer_Assignment('E001','C002')
la2 = Lecturer_Assignment('E001','C001')
la3 = Lecturer_Assignment('E002','C003')
rp = Role_Permission('講師', '講師描述', '課程管理模組', 'r')
ur = User_Role(1,'E001')
db.session.add_all([i1_1,i1_2,i2_1,i2_2,i2_3,i3_1,i3_2,i3_3,p1,p2,p3,prod1,prod2,prod3,prod4,prod5,u1,u2,u3,u4,u5,d1,d2,d3,d4,d5,c1,c2,c3,ca1,ca2,ca3,ca4,rp,ur,la1,la2,la3])
db.session.commit()
db.session.close()
# p2 = Employee('9999', 'Dennis')
# p3 = Employee('7777', 'Joey')
 
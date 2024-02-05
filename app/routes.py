from app import app
from flask import jsonify
from app.controllers.edu_course import del_element, cre_courses, get_courses, upd_course, get_item_1, remove_member, add_member
from app.controllers.edu_lectructor import get_lecturers,get_lecturer_assignments
from app.controllers.edu_document import get_file, upl_file, del_file

@app.route('/api/')
def index():
    return 'Hello, world'

@app.route('/api/item1', methods=['GET'])
def getItem1():
    items = get_item_1()
    return items 

@app.route('/api/course', methods=['GET'])
def getCourse():
    courses = get_courses()
    return courses 
@app.route('/api/course', methods=['PUT'])
def updateCourse():
    courses = upd_course()
    return jsonify(courses)  
@app.route('/api/course', methods=['POST'])
def createCourse():
    return cre_courses()
@app.route('/api/course', methods=['DELETE'])
def deleteCourse():
    return del_element("Course")

@app.route('/api/course-file', methods=['GET'])
def getFile():
    return get_file()
@app.route('/api/course-file', methods=['POST'])
def uploadFile():
    return upl_file()
@app.route('/api/course-file', methods=['DELETE'])
def removeFile():
    return del_file()

@app.route('/api/lecturerAssignment', methods=['GET'])
def gotLecturerAssignments():
    return jsonify(get_lecturer_assignments())
@app.route('/api/lecturerAssignment', methods=['DELETE'])
def delLecturerAssignment():
    return del_element("Lecturer_Assignment")

@app.route('/api/lecturers', methods=['GET'])
def gotLecturers():
    return get_lecturers()

@app.route('/api/memberAssignment', methods=['POST'])
def addMember():
    return add_member()
@app.route('/api/memberAssignment', methods=['DELETE'])
def removeMember():
    return remove_member()
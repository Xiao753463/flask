from flask import request
from app import app, db
from sqlalchemy import delete
from app.models import Course_Document
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file():
    cid = request.args.get('cid')
    result = db.session.query(Course_Document).where(Course_Document.cid == cid).all()
    return result
def upl_file():
    cid = request.args.get('cid')
    time = request.args.get('time')
    editor = request.args.get('editor')
    desc = request.args.get('desc')
    file = request.files['file']
    course_folder = os.path.join(app.root_path, 'static', cid)
    if not os.path.exists(course_folder):
        os.makedirs(course_folder)
    if file and allowed_file(file.filename):
        counter = 1
        filename = secure_filename(file.filename)
        path = course_folder + "/" + filename
        temp_filename, extension = os.path.splitext(filename)
        while os.path.exists(path):
            filename = temp_filename + " (" + str(counter) + ")" + extension
            path = course_folder + "/" + filename
            counter += 1
        file.save(os.path.join(course_folder, filename))
        name = filename
        pass
    else:
        return ('File uploaded error!')
    doc = Course_Document(
        cid = cid,
        name = name,
        time = time,
        editor = editor,
        desc = desc
    )
    db.session.add(doc)
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
    
def del_file():
    cid = request.args.get('cid')
    name = request.args.get('name')
    course_folder = os.path.join(app.root_path, 'static', cid)
    try:
        os.remove(os.path.join(course_folder, name))
        pass
    except:
        return ('Cannot find the file you want delete')
    sql = delete(Course_Document).where(Course_Document.cid == cid).where(Course_Document.name == name)
    db.session.execute(sql)
    try:
        db.session.commit()
        return ('Course document deleted successfully!')
    # do something with the session
    except:                   # * see comment below
        db.session.rollback()
        return ('Course deleted error!')
        raise
    else:
        db.session.commit()
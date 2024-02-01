from app import app
from flask import render_template, jsonify, send_from_directory, redirect, url_for
from app.controllers.edu_course import get_info,del_courses,cre_courses, get_courses
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return 'Hello, world'


@app.route('/course', methods=['GET'])
def get_course():
    courses = get_info()
    return jsonify(courses)  
@app.route('/course', methods=['POST'])
def create_course():
    return cre_courses()
@app.route('/course', methods=['DELETE'])
def del_course():
    return del_courses()
@app.route('/test', methods=['GET'])
def test():
    courses = get_courses()
    return jsonify(courses)  
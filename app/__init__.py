from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
username=os.getenv("DB_USERNAME")
password=os.getenv("DB_PASSWORD")
port=os.getenv("PORT")
table=os.getenv("TABLE")
app.json.ensure_ascii = False  # <-- this line saves the day
app.json.mimetype = "application/json; charset=utf-8" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+username+":"+password+"@localhost:"+port+"/"+table
UPLOAD_FOLDER = '/temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db = SQLAlchemy(app)
# 導入其他的程式模組
from app import routes, models
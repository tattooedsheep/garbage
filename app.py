from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///' + os.path.join(basedir, "app.sqlite")

CORS(app)
db= SQLAlchemy(app)

class Student(db.Model):
    __tablename__= "students"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String(), nullable = False)
    special_skill = db.Column(db.String(), nullable = False)
    birth_date = db.Column(db.String(), nullable = False)


    def __init__(self, first_name, last_name, special_skill, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.special_skill = special_skill
        self.birth_date = birth_date
        

@app.route("/students", methods=["POST"])
def add_student():
    if request.content_type == "application/json":
        post_data = request.get_json()
        first_name = post_data.get("first_name")
        last_name = post_data.get("last_name")
        birth_date = post_data.get("birth_date")
        special_skill = post_data.get("special_skill")
        record = Student(first_name, last_name, special_skill, birth_date)
        db.session.add(record)
        db.session.commit()
        return jsonify("data posted")
    return jsonify("data failed")
    
@app.route("/student/all", methods=["GET"])
def get_all():
    all_students = db.session.query(Student.id, Student.first_name, Student.last_name, Student.special_skill, Student.birth_date).all()
    array= []
    for student in all_students:
        array.append({
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "special_skill": student.special_skill,
            "birth_date": student.birth_date
        })
    return jsonify(array)

    
    
if __name__ == "__main__":
    app.debug = True
    app.run()
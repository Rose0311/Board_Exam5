from flask import Flask, render_template, request
from models import db, Student, School, AnswerSheet, Examiner, Invigilator
from sqlalchemy import func, extract

app = Flask(__name__)
app.config.from_object('config')  # Load configuration from config.py

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def student_data():
    results = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'student_count_by_school':
            results = db.session.query(
                School.school_name, func.count(Student.student_rollno).label('student_count')
            ).join(School, Student.school_id == School.school_id).group_by(School.school_name).all()
        elif action == 'students_sorted_by_marks':
            results = db.session.query(
                Student.stdf_name, AnswerSheet.mark_assigned
            ).join(AnswerSheet, Student.student_rollno == AnswerSheet.student_rollno).order_by(AnswerSheet.mark_assigned.desc()).all()
    return render_template('student_data.html', results=results)

@app.route('/schools', methods=['GET', 'POST'])
def school_data():
    results = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'school_student_joins':
            results = db.session.query(
                Student.stdf_name, School.school_name
            ).join(School, Student.school_id == School.school_id).all()
        elif action == 'school_with_max_students':
            results = db.session.query(
                School.school_name, func.count(Student.student_rollno).label('student_count')
            ).join(School, Student.school_id == School.school_id).group_by(School.school_name).order_by(func.count(Student.student_rollno).desc()).first()
    return render_template('school_data.html', results=results)

@app.route('/examiners', methods=['GET', 'POST'])
def examiner_data():
    results = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'formatted_exam_dates':
            results = db.session.query(
                func.to_char(Invigilator.exam_date, 'Month DD, YYYY').label('formatted_date')
            ).all()
        elif action == 'examiner_teaching_experience':
            results = db.session.query(
                Examiner.exmf_name, Examiner.exmm_name, Examiner.exml_name, Examiner.teaching_experience
            ).all()
    return render_template('examiner_data.html', results=results)

@app.route('/test_connection')
def test_connection():
    try:
        db.session.execute('SELECT 1')
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"


if __name__ == '__main__':
    app.run(debug=True)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    student_rollno = db.Column(db.Integer, primary_key=True)
    stdf_name = db.Column(db.String(50), nullable=False)
    stdm_name = db.Column(db.String(50))
    stdl_name = db.Column(db.String(50))
    class_ = db.Column(db.String(10), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.school_id'), nullable=False)

    def __repr__(self):
        return f"<Student {self.student_rollno}, {self.stdf_name}>"

class School(db.Model):
    __tablename__ = 'school'
    school_id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    students = db.relationship('Student', backref='school', lazy=True)

    def __repr__(self):
        return f"<School {self.school_id}, {self.school_name}>"

class AnswerSheet(db.Model):
    __tablename__ = 'answer_sheet'
    answer_bookid = db.Column(db.Integer, primary_key=True)
    student_rollno = db.Column(db.Integer, db.ForeignKey('student.student_rollno'), nullable=False)
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiner.examiner_id'), nullable=False)
    mark_assigned = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<AnswerSheet {self.answer_bookid}, Mark: {self.mark_assigned}>"

class Examiner(db.Model):
    __tablename__ = 'examiner'
    examiner_id = db.Column(db.Integer, primary_key=True)
    exmf_name = db.Column(db.String(50), nullable=False)
    exmm_name = db.Column(db.String(50))
    exml_name = db.Column(db.String(50))
    teaching_experience = db.Column(db.Integer, nullable=False)
    invigilations = db.relationship('Invigilator', backref='examiner', lazy=True)

    def __repr__(self):
        return f"<Examiner {self.examiner_id}, {self.exmf_name}>"

class Invigilator(db.Model):
    __tablename__ = 'invigilator'
    examiner_id = db.Column(db.Integer, db.ForeignKey('examiner.examiner_id'), primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.school_id'), primary_key=True)
    exam_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Invigilator Examiner: {self.examiner_id}, School: {self.school_id}>"

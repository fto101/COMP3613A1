from App.models.user import User
from App.database import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    student = db.relationship('Student', backref='requests', foreign_keys=[student_id])
    staff = db.relationship('Staff', backref='reviews', foreign_keys=[staff_id])

    def __init__(self, student_id, description, hours, status='pending', staff_id=None):
        self.student_id = student_id
        self.description = description
        self.hours = hours
        self.status = status
        self.staff_id = staff_id
        

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'description': self.description,
            'hours': self.hours,
            'status': self.status,
            'staff_id': self.staff_id
        }
    
    def __repr__(self):
        if self.staff_id:
            return f'Request {self.id} by Student {self.student.username}, reviewed by Staff {self.staff_id}, Status: {self.status} description: {self.description}, Hours: {self.hours}'
        else:
            return f'Request {self.id} by Student {self.student.username}, Status: {self.status} description: {self.description}, Hours: {self.hours}'
   
    def view_details(self):
        if self.staff_id:
            return f'Request ID: {self.id}\nStudent: {self.student.fname} {self.student.lname}\nStudent Id: {self.student_id}\nDescription: {self.description}\nHours: {self.hours}\nStatus: {self.status}\nReviewed by Staff ID: {self.staff_id}'
        else:
            return f'Request ID: {self.id}\nStudent: {self.student.fname} {self.student.lname}\nStudent Id: {self.student_id}\nDescription: {self.description}\nHours: {self.hours}\nStatus: {self.status}\nNot yet reviewed by staff.'
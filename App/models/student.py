from App.database import db
from App.models.user import User

class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    degree = db.Column(db.String(50), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    accolades = db.Column(db.String(200), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, fname, lname, password, degree, hours):
        super().__init__(username, fname, lname, password)
        self.degree = degree
        self.hours = hours
        if self.hours >= 15:
            self.accolades = "Bronze"
        if self.hours >= 25:
            self.accolades = "Silver"
        if self.hours >= 50:
            self.accolades = "Gold"

    def get_json(self):
        user_json = super().get_json()
        user_json.update({
            'hours': self.hours,
            'degree': self.degree,
            'accolades': self.accolades,
            'fname': self.fname,
            'lname': self.lname
        })
        return user_json
    
    def staff_view(self):
        return f'ID: {self.id}\nUsername: {self.username}\nFirst Name: {self.fname}\nLast Name: {self.lname}\nDegree: {self.degree}\nHours: {self.hours}\nAccolades: {self.accolades if self.accolades else "None"}'
        
    
    def __repr__(self):
        return f'Student {self.username}, Degree: {self.degree}, Hours: {self.hours}, Accolades: {self.accolades if self.accolades else "None"}'
    
    def view_details(self):
        return f'Username: {self.username}\nFirst Name: {self.fname}\nLast Name: {self.lname}\nDegree: {self.degree}\nHours: {self.hours}\nAccolades: {self.accolades if self.accolades else "None"}'
    
    def update_hours(self, additional_hours):
        self.hours += additional_hours
        db.session.commit()
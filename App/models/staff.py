from App.models.user import User
from App.database import db

class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, username, password, fname, lname):
        super().__init__(username, fname, lname, password, )
        
        
    def get_json(self):
        user_json = super().get_json()
        
        return user_json
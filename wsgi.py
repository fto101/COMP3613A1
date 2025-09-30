import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import *
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    db.drop_all()
    db.create_all()
    
    student1 = Student(username='bob', fname='Bob', lname='Smith', password='bobpass', degree='Computer Science', hours=10)
    staff = Staff(username='admin', fname='Admin', lname='User', password='adminpass')
    db.session.add(student1)
    db.session.add(staff)
    student2 = Student(username='alice', fname='Alice', lname='Johnson', password='alicepass', degree='Mathematics', hours=20)
    db.session.add(student2)
    student3 = Student(username='charlie', fname='Charlie', lname='Brown', password='charliepass', degree='Physics', hours=30)
    db.session.add(student3)
    db.session.commit()
    request1 = Request(student_id=student1.id, description='Community service', hours=5)
    request2 = Request(student_id=student2.id, description='Library assistance', hours=3)
    db.session.add(request2)
    request3 = Request(student_id=student3.id, description='Event organization', hours=4)
    db.session.add(request3)
    db.session.add(request1)
    db.session.commit()

    
    print('database intialized')

'''
User Commands
'''

user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("create_user", help="Create a new user")
@click.argument("type", default="student")
def create_user_command(type):
    username = input("Enter username: ")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    password = input("Enter password: ")
    if type == 'student':
        degree = input("Enter degree: ")
        hours = int(input("Enter initial hours: "))
        new_user = Student(username=username, fname=fname, lname=lname, password=password, degree=degree, hours=hours)
    elif type == 'staff':
        new_user = Staff(username=username, fname=fname, lname=lname, password=password)
    else:
        print("Invalid user type. Use 'student' or 'staff'.")
        return
    db.session.add(new_user)
    db.session.commit()
    print(f'{type.capitalize()} {username} created!')


app.cli.add_command(user_cli) # add the group to the cli



# Staff Commands

staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("view_requests", help="View all requests")
def view_requests_command():
    requests = Request.query.all()
    for request in requests:
        print(request)
    request_id = input("Enter request ID to review: ")
    request = Request.query.get(request_id)
    if request:
        print(request.view_details())
    else:
        print("Request not found.")
        exit()
    status = input("Enter new status (approved/rejected). Enter 'no' to skip.: ")
    if status in ['approved', 'rejected']:
        staff_id = input("Enter your staff ID: ")
        staff = Staff.query.get(staff_id)
        if staff:
            if status == 'approved':
                request.status = 'approved'
                student = Student.query.get(request.student_id)
                student.update_hours(request.hours)
                request.staff_id = staff.id
                db.session.commit()    
                print("Request approved.")
            elif status == 'rejected':
                request.status = 'rejected'
                request.staff_id = staff.id
                db.session.commit()    
                print("Request rejected.")
        else:
            print("Staff not found.")
            exit()
    elif status.lower() == 'no':
        print("No changes made to the request.")
    else:
        print("Invalid status. No changes made to the request.")
    
    
    

@staff_cli.command("view_lb", help="View leaderboard")
def view_leaderboard_command():
    students = Student.query.order_by(Student.hours.desc()).all()
    for idx, student in enumerate(students, start=1):
        print(f'{idx}. {student.username} - {student.hours} hours')
    student_idx = input("Enter student index to view details (Enter '0' to skip): ")
    if student_idx.isdigit() and 0 < int(student_idx) <= len(students):
        student = students[int(student_idx)-1]
        print(student.staff_view())
    
   


app.cli.add_command(staff_cli)


#Student Commands
student_cli = AppGroup('student', help='Student object commands')

@student_cli.command("view_requests", help="View your requests")
def view_student_requests_command():
    student_id = input("Enter your student ID: ")
    student = Student.query.get(student_id)
    if student:
        requests = Request.query.filter_by(student_id=student.id).all()
        for request in requests:
            print(request)
    else:
        print("Student not found.")
        exit()
    next_action = input("Do you want to submit a new request? (yes/no): ")
    if next_action.lower() == 'yes':
        description = input("Enter request description: ")
        hours = int(input("Enter number of hours: "))
        new_request = Request(student_id=student.id, description=description, hours=hours)
        db.session.add(new_request)
        db.session.commit()
        print("Request submitted.")



@student_cli.command("view_lb", help="View leaderboard")
def view_leaderboard_command():
    students = Student.query.order_by(Student.hours.desc()).all()
    for idx, student in enumerate(students, start=1):
        print(f'{idx}. {student.username} - {student.hours} hours')


@student_cli.command("view_details", help="View your details")
def view_details_command():
    student_id = input("Enter your student ID: ")
    student = Student.query.get(student_id)
    if student:
        print(student.view_details())
    else:
        print("Student not found.")


@student_cli.command("view_accolades", help="View your accolades")
def view_accolades_command():
    student_id = input("Enter your student ID: ")
    student = Student.query.get(student_id)
    if student:
        print(f'Accolades: {student.accolades if student.accolades else "None"}')
        print(f'Accolades criteria:\nBronze: 15+ hours\nSilver: 25+ hours\nGold: 50+ hours')
    else:
        print("Student not found.")



app.cli.add_command(student_cli)
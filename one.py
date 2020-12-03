# from workbook
import bcrypt
from functools import wraps
from flask import Flask
######################
from flask import Flask, url_for, request, render_template, redirect, session, flash, jsonify
# to set up database I'll use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# to create json from database
from flask_marshmallow import Marshmallow
# to set up an automatic data in the database when creating a new entry
from datetime import datetime
# new to use login
# , login_user, login_required, logout_user, current_user
from flask_login import LoginManager, UserMixin
##from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# where the database is located, the database is called test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#####
app.secret_key = 'THISisMYsecretKey009'
valid_email = 'admin@a.com'
valid_pwhash = bcrypt.hashpw('secretpass'.encode('utf-8'), bcrypt.gensalt())


def check_auth(email, password):
    if (email == valid_email and valid_pwhash == bcrypt.hashpw(password.encode('utf-8'), valid_pwhash)):
        return True
    return False


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect('/admin/')
        return f(*args, **kwargs)
    return decorated


@app.route('/admin/logout/')
def admin_logout():
    session['logged_in'] = False
    return 'admin'


@app.route('/admin/account/')
@requires_login
def account():

    return 'account.html'


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        user = request.form['email1']
        pw = request.form['pwd']

        if check_auth(user, pw):
            session['logged_in'] = True
            return 'logged'
    return 'not logged'

    ##


class Admin(UserMixin, db.Model):
    # table for admin
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    sname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# creating a class here - a model


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # to retrieve what has been created; to get from the database the task and it's id
    def __repr__(self):
        return '<Task %r>' % self.id


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo


@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        # get what is in input field called content and sent to the db
        task_content = request.form['content']
        # create Todo object
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        # render all the tasks which are currently in the db ---> pierwszy == .first()
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
# to delete a task from the list/db
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
# to update a task from the list/db
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # update logic
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with updating the task'

    else:
        return render_template('update.html', task=task)


# ponizej sa rozne cwiczenia z workbooka (hello + admin sa spoko)
# add an image
@app.route('/static/img')
def static_example_img():
    start = '<img src="'
    url = url_for('static', filename='vmask.jpg')
    end = '" >'
    return start+url+end, 200

# to jest errorhandler - displays a custom error page


@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the page you requested.", 404


# this is page with html - link
@app.route('/hello/')
def hello():
    return '''<html><body>
            <p>this is my hello page </p>
            <br>
            <a href="../account">Account</a>
            </body></html>'''

# this is how to use template


@app.route('/template/')
@app.route('/template/<name>')
def template(name=None):
   # user = {'name': name}
    return render_template('hello.html', name=name)


#this is gopdbye
@app.route("/goodbye/")
def goodbye():
    return "this is my goodbye page"

# this is account page


# @app.route("/account/", methods=['GET', 'POST'])
# def account():
#     if request.method == 'POST':
#         print(request.form)
#         name = request.form['name']
#         return "Hello %s" % name
#     else:
#         page = '''
#         <html><body>
#             <form action ="" method="post" name="form">
#                 <label for="name">Name:</label>
#                 <input type="text" name ="name" id="name"/>
#                 <input type="submit" name="submit" id="submit"/>
#             </form>
#         </body></html> '''

#         return page


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

from flask import Flask, url_for, request, render_template, redirect
# to set up database I'll use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# to set up an automatic data in the database when creating a new entry
from datetime import datetime

app = Flask(__name__)
# where the database is located, the database is called test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# creating a class here - a model


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # to retrieve what has been created; to get from the database the task and it's id
    def __repr__(self):
        return '<Task %r>' % self.id

    # add methods POST and GET to handle data flow to and from the database


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
        pass
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


@app.route("/account/", methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        return "Hello %s" % name
    else:
        page = '''
        <html><body>
            <form action ="" method="post" name="form">
                <label for="name">Name:</label>
                <input type="text" name ="name" id="name"/>
                <input type="submit" name="submit" id="submit"/>
            </form>
        </body></html> '''

        return page


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

from flask import Flask, url_for, request, render_template
app = Flask(__name__)

#@app.route('/')
#def one_function():
   #return 'Hello, this is new text, and more characters'

@app.route('/')
def root():
    return "this is my main page"

#add an image
@app.route('/static/img')
def static_example_img():
    start = '<img src="'
    url = url_for('static', filename='vmask.jpg')
    end = '" >'
    return start+url+end, 200

#to jest errorhandler - displays a custom error page
@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the page you requested.", 404


#this is page with html - link
@app.route('/hello/')
def hello():
    return '''<html><body>
            <p>this is my hello page </p>
            <br>
            <a href="../account">Account</a>
            </body></html>'''

#this is how to use template
@app.route('/template/')
@app.route('/template/<name>')
def template(name=None):
   # user = {'name': name}
    return render_template('hello.html', name=name)



#this is gopdbye
@app.route("/goodbye/")
def goodbye():
    return "this is my goodbye page"

#this is account page
@app.route("/account/", methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        print (request.form)
        name = request.form['name']
        return "Hello %s" % name
    else:
        page= '''
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

    

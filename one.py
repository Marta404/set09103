from flask import Flask, url_for
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


@app.route('/hello/')
def hello():
    return "this is my hello page"

@app.route("/goodbye/")
def goodbye():
    return "this is my goodbye page"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

    

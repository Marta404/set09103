from flask import Flask, render_template
app = Flask(__name__)


@app.route('/game/')
def game ():
    return render_template('topnav.html')



if __name__ == "__main__":
    app.rum(host='0.0.0.0', debug=True)

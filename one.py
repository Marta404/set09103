from flask import Flask
app = Flask(__name__)

@app.route('/')
def one_function():
    return 'Hello Napier'


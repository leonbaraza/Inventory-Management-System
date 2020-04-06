# importing
# import <filename>
# from filename import <.....>
from flask import Flask, render_template

# calling/ instanciating
app = Flask(__name__)

# Creating of endpoints/ routes
# 1. declaration of a route
# 2. a function embedded to the route
@app.route('/')
def hello_world():
    return '<h1>Welcome to web development</h1>'

@app.route('/home')
def home():
    return '<h1>Welcome to Home Page</h1>'


# @app.route('/name/<name>')
# def my_name(name):
#     # return f'My name is {name}'
#     # return 'My name is {}'.format(name)
#     return 'My name is ' +name


# add two numbers dynamically
@app.route('/add/<a>/<b>')
def adding(a, b):
    sum = int(a)+int(b)
    return str(sum)


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact_us')
def contact():
    return render_template('contact.html')

@app.route('/service') 
def service():
    return render_template('service.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/inventories')
def inventories():
    return render_template('inventories.html')


# Run your app
if __name__ == '__main__':
    app.run()

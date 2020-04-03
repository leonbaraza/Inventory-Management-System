# importing
# import <filename>
# from filename import <.....>
from flask import Flask, url_for

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


@app.route('/name/<name>')
def my_name(name):
    # return f'My name is {name}'
    # return 'My name is {}'.format(name)
    return 'My name is ' +name


# add two numbers dynamically
@app.route('/add/<a>/<b>')
def adding(a, b):
    sum = int(a)+int(b)
    return str(sum)

# divide
# multiply
# output : your story(name, age, town)

with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('home'))
    print(url_for('my_name'))
    print(url_for('adding'))


# Run your app
if __name__ == '__main__':
    app.run()

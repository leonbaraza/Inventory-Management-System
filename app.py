# importing
# import <filename>
# from filename import <.....>
from flask import Flask, render_template, request, redirect, url_for

import pygal

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


@app.route('/inventories', methods=['GET', 'POST'])
def inventories():

    # recieve from a form
    
    if request.method == 'POST':
        name = request.form['name']
        inv_type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)

        return redirect(url_for('inventories'))
 
    return render_template('inventories.html')


# A ROUTE TO RECIEVE STOCK DATA FROM ADD STOCK MODAL

@app.route('/add_stock', methods=['POST'])
def add_stock():

    # check if the method is post
    if request.method == 'POST':
        stock = request.form['stock']
        print(stock)

        return redirect(url_for('inventories'))


@app.route('/make_sale', methods=['POST'])
def make_sale():

    if request.method == 'POST':
        quantity = request.form['quantity']
        print(quantity)

        return redirect(url_for('inventories'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():

    # recieve from a form
    
    if request.method == 'POST':
        name = request.form['name']
        inv_type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)

        return redirect(url_for('inventories'))
 

@app.route('/data_visualization')
def data_visualization():
    ''' 
    Add components to your pie chart
     1. add title
     2. Partition your pie chart
     '''

    # Initialize your pie chart
    pie_chart = pygal.Pie()

    pie_chart.title = 'Distribution of corona virus in kenya'
    pie_chart.add('Nairobi', 63)
    pie_chart.add('Mombasa', 20)
    pie_chart.add('Kilifi', 17)
    pie_chart.add('Machakos', 30)
    pie_chart.add('Kiambu', 7)

    pie_data = pie_chart.render_data_uri()

    # end of piechart

    # start of line graph

    line_graph = pygal.Line()

    line_graph.title = 'Browser usage evolution (in %)'
    line_graph.x_labels = map(str, range(2002, 2013))
    line_graph.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_graph.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_graph.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_graph.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

    line_data = line_graph.render_data_uri()

    '''
    x = "tech"
    y = x
    y = x = 'tech'

    '''
    return render_template('charts.html', pie=pie_data, line=line_data)


# Run your app
if __name__ == '__main__':
    app.run()

# importing
# import <filename>
# from filename import <.....>
from flask import Flask, render_template, request, redirect, url_for

import pygal

import psycopg2

from flask_sqlalchemy import SQLAlchemy

from Config.Config import Development,Production


''' 
    We have two ways for connecting to the database in flask
    1. psycopg2 - Here you write SQL statements
    2. Flask-SQLAlchemy - Here you use ORM(Object Relational Mapper)

    PSYCOPG2
    Its a python library that helps write queries in flask
    HOW TO USE IT
    1. install it

    2. set up a connection to your database 
        - username
        - password
        - port
        - root
        - dbname

    3. connect to using cursor
    4. execute an SQL Statement
    5. Fetch your records
'''


'''
    FLASK-SQLALCHEMY
    Library that helps us write classes object to communicate to our database without
    writing sql statements

    EXAMPLE 
    INSERT INTO sales VALUES (inv_id=1, quantity=10, created=now())

    create a class and it SalesModel
    then create function that inserts records
    then insert

    class SalesModel():
        def insert_sales(self):
            db.session.add()
        
    query

        def query_sales(self):
            self.query.all()

        select * from sales


    STEPS TO USE FLASK-SQLALCHEMY
    1. install it
    2. use it
        - create a connection to the db
        - load configurations
        - create an instance of FLASK-SQLALCHEMY by passing in the app


'''


# calling/ instanciating
app = Flask(__name__)

# Load configuration
app.config.from_object(Development)

# calling/ instanciating of SQLAlchemy
# alway comes with functions and helpers to create our tables
db = SQLAlchemy(app)

# Creating of endpoints/ routes
# 1. declaration of a route
# 2. a function embedded to the route


# creating tables
from models.Inventory import InventoryModel


@app.before_first_request
def create_tables():
    db.create_all()    



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


    conn = psycopg2.connect(" dbname='test' user='postgres' host='localhost' port='5432' password='123456' ")

    cur = conn.cursor()

    cur.execute("""
        SELECT type, count(type)
        FROM public.inventories
        GROUP BY type;    
    """)

    product_service = cur.fetchall()

    # print(product_service)

    # Initialize your pie chart
    pie_chart = pygal.Pie()


    # my_pie_data = [
    #     ('Nairobi', 63),
    #     ('Mombasa', 20),
    #     ('Kilifi', 17),
    #     ('Machakos', 30),
    #     ('Kiambu', 7)
    # ]


    pie_chart.title = 'Ratio of product and service'
    for each in product_service:
        pie_chart.add(each[0], each[1])

    # pie_chart.add('Nairobi', 63)
    # pie_chart.add('Mombasa', 20)
    # pie_chart.add('Kilifi', 17)
    # pie_chart.add('Machakos', 30)
    # pie_chart.add('Kiambu', 7)

    pie_data = pie_chart.render_data_uri()

    # end of piechart

    # start of line graph

    # represennts sales made in every month

    cur.execute("""
        SELECT EXTRACT(MONTH FROM s.created_at) as sales_month, sum(quantity * selling_price) as total_sales
        from sales as s
        join inventories as i on s.inv_id = i.id
        GROUP BY sales_month
        ORDER BY sales_month
    """)

    monthly_sales=cur.fetchall()
    # print(monthly_sales)

    data = [
        {'month': 'January', 'total': 22},
        {'month': 'February', 'total': 27},
        {'month': 'March', 'total': 23},
        {'month': 'April', 'total': 20},
        {'month': 'May', 'total': 12},
        {'month': 'June', 'total': 32},
        {'month': 'July', 'total': 42},
        {'month': 'August', 'total': 72},
        {'month': 'September', 'total': 52},
        {'month': 'October', 'total': 42},
        {'month': 'November', 'total': 92},
        {'month': 'December', 'total': 102}
    ]
    x = []
    sales = []

    for each in  monthly_sales:
        x.append(each[0])
        sales.append(each[1])
    
    # print(x)
    # print(sales)

    line_graph = pygal.Line()

    line_graph.title = 'Total sales made in every month in the year 2019'
    line_graph.x_labels = map(str, x)
    # line_graph.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1, 42.8])
    # line_graph.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3, 23.8])
    # line_graph.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1, 26.6])
    # line_graph.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5, 26.6])
    line_graph.add('Total Sales', sales)

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

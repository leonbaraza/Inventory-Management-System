# importing
# import <filename>
# from filename import <.....>
from flask import Flask, render_template, request, redirect, url_for, flash

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

# psycopg2 connection
conn = psycopg2.connect(" dbname='test' user='postgres' host='localhost' port='5432' password='' ")
cur = conn.cursor()

# creating tables
from models.Inventory import InventoryModel
from models.Sales import SalesModel
from models.Stock import StockModel

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

    inventories = InventoryModel.fetch_all_inventories()

    cur.execute("""
    
    SELECT inv_id, sum(quantity) as "remaining_stock"
		FROM (SELECT st.inv_id, sum(stock) as "quantity"
		FROM public.new_stock as st
		GROUP BY inv_id
			
			union all
			 
			SELECT sa.inv_id, - sum(quantity) as "quantity"
		FROM public.new_sales as sa
		GROUP BY inv_id) as stsa
		GROUP BY inv_id
		ORDER BY inv_id;

    """)

    rs = cur.fetchall()
    
    # recieve from a form
    
    if request.method == 'POST':
        name = request.form['name']
        inv_type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        '''
        STEPS TO INSERT RECORDS
        1. create your model object
        
        '''

        new_inv = InventoryModel(name=name, inv_type=inv_type, buying_price=buying_price, selling_price=selling_price)
        new_inv.add_inventories()
        # InventoryModel.add_inventories(new_inv)

        flash(u'Inventory added successfully.', 'error')

        return redirect(url_for('inventories'))
 
    return render_template('inventories.html', inventories=inventories, remaining_stock=rs)


# A ROUTE TO RECIEVE STOCK DATA FROM ADD STOCK MODAL

@app.route('/add_stock/<inv_id>', methods=['POST'])
def add_stock(inv_id):
    # print(inv_id)
    # check if the method is post
    if request.method == 'POST':
        stock = request.form['stock']
        new_stock = StockModel(inv_id=inv_id, stock=stock)
        new_stock.add_stock()

        return redirect(url_for('inventories'))


@app.route('/make_sale/<inv_id>', methods=['POST'])
def make_sale(inv_id):

    if request.method == 'POST':
        quantity = request.form['quantity']
        new_sale = SalesModel(inv_id=inv_id, quantity=quantity)
        new_sale.add_sales()

        return redirect(url_for('inventories'))


@app.route('/edit/<inv_id>', methods=['GET', 'POST'])
def edit(inv_id):

    record = InventoryModel.query.filter_by(id=inv_id).first()

    # recieve from a form
    
    if request.method == 'POST':
        name = request.form['name']
        inv_type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        if record:
            record.name = name
            record.inv_type = inv_type
            record.buying_price=buying_price
            record.selling_price=selling_price

            db.session.commit()

        return redirect(url_for('inventories'))
 

@app.route('/data_visualization')
def data_visualization():
    ''' 
    Add components to your pie chart
     1. add title
     2. Partition your pie chart
     '''

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


@app.route('/view_sales/<inv_id>')
def view_sales(inv_id):

    cur.execute(f"""
    
    SELECT inv_id, sum(quantity) as "remaining_stock"
		FROM (SELECT st.inv_id, sum(stock) as "quantity"
		FROM public.new_stock as st
		GROUP BY inv_id
			
			union all
			 
			SELECT sa.inv_id, - sum(quantity) as "quantity"
		FROM public.new_sales as sa
		GROUP BY inv_id) as stsa
		WHERE inv_id={inv_id}
		GROUP BY inv_id;
    
    """)

    rec = cur.fetchall()
    print(rec)


    sales = SalesModel.get_sales_by_id(inv_id)
    inv_name = InventoryModel.fetch_by_id(inv_id)

    return render_template('view_sales.html', sales=sales, 
                            inv_name=inv_name)


@app.route('/delete/<inv_id>')
def delete_inventory(inv_id):
    
    record = InventoryModel.query.filter_by(id=inv_id).first()

    # all - get all records based on the cond and return for me in a list
            # always use indexing or loops
            # record[1].name
            # [<InventoryModel1>]
            

    # first - return the first obj based on the cond
            # record.name
            # <InventoryModel1>
            # user authentication


    if record:
        db.session.delete(record)
        db.session.commit()

    else:
        print('Record does not exist')

    flash(u"Recorded deleted", 'danger')

    return redirect(url_for('inventories'))


# Run your app
if __name__ == '__main__':
    app.run()

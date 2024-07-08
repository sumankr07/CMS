from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
mydb = mysql.connect(
    host="localhost",
    user="root",
    password="77777777",
    database="cafe_management_system"
)
db_cursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        menu_option = request.form['menu']
        if menu_option == '1':
            return redirect(url_for('new_order'))
        elif menu_option == '2':
            return redirect(url_for('existing_customer'))
        elif menu_option == '3':
            return redirect(url_for('existing_customer'))
        elif menu_option == '4':
            return redirect(url_for('existing_customer'))
    return render_template('index.html')

@app.route('/new_order', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        customer_option = request.form['customer_option']
        if customer_option == '1':
            return redirect(url_for('new_customer', customer_option=customer_option))
        elif customer_option == '2':
            return redirect(url_for('existing_customer', customer_option=customer_option))
        
    return render_template('new_order.html')

@app.route('/new_customer/<customer_option>', methods=['GET', 'POST'])
def new_customer(customer_option):

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phoneNo = request.form['customer_phoneNo']

        db_cursor.execute("SELECT Customer_ID FROM customer")
        total_row_in_customer_table_in_list = db_cursor.fetchall()
        customer_id = len(total_row_in_customer_table_in_list) + 1 if total_row_in_customer_table_in_list else 1

        return redirect(url_for('product_type_selection', customer_option=customer_option, customer_id=customer_id,
                                 customer_name=customer_name, customer_phoneNo=customer_phoneNo))
    return render_template('new_customer.html')

@app.route('/existing_customer/<customer_option>', methods=['GET', 'POST'])
def existing_customer(customer_option):

    if request.method == 'POST':
        customer_id = request.form['customer_id']

        db_cursor.execute(f"SELECT * FROM customer WHERE Customer_ID = {customer_id}")
        customer_data = db_cursor.fetchone()
        if customer_data:
            customer_name = customer_data[1]
            customer_phoneNo = customer_data[2]
            return redirect(url_for('product_type_selection', customer_option=customer_option,customer_id=customer_id,
                                     customer_name=customer_name, customer_phoneNo=customer_phoneNo))
        else:
            flash(f"No customer found with Customer ID {customer_id}. Please try again.")
            return redirect(url_for('existing_customer', customer_option=customer_option))
    return render_template('existing_customer.html')

@app.route('/product_type_selection/<customer_option>/<customer_id>/<customer_name>/<customer_phoneNo>', methods=['GET', 'POST'])
def product_type_selection(customer_option, customer_id, customer_name, customer_phoneNo):

    db_cursor.execute("SELECT DISTINCT Product_Type FROM product")
    all_product_type = db_cursor.fetchall()
    if all_product_type:
        if request.method == 'POST':
            product_type_name = request.form['product_type']

            return redirect(url_for('product_name_selection', customer_option=customer_option, customer_id=customer_id,
                                     customer_name=customer_name, customer_phoneNo=customer_phoneNo, product_type_name = product_type_name))

        return render_template('product_type_selection.html', all_product_type=all_product_type)
    else:
        flash('There are no products in your database! Please add product in your database')
        return redirect(url_for('home'))

@app.route('/product_name_selection/<customer_option>/<customer_id>/<customer_name>/<customer_phoneNo>/<product_type_name>', methods=['GET', 'POST'])
def product_name_selection(customer_option, customer_id, customer_name, customer_phoneNo, product_type_name):

    db_cursor.execute(f"SELECT Product_Name, Product_Price FROM product WHERE Product_Type = '{product_type_name}'")
    all_product_name = db_cursor.fetchall()
    if request.method == 'POST':
        product_name = request.form['product_name']

        db_cursor.execute(f"SELECT * FROM product WHERE Product_Name = '{product_name}'")
        order_item_in_list = db_cursor.fetchall()
        order_item = order_item_in_list[0]
        product_id = order_item[0]
        product_price = order_item[3]

        return redirect(url_for('order_confirmation', customer_option=customer_option, customer_id=customer_id,
                                 customer_name=customer_name, customer_phoneNo=customer_phoneNo, product_id=product_id,
                                 product_type_name=product_type_name, product_name=product_name, product_price=product_price))
    
    return render_template('product_name_selection.html', all_product_name=all_product_name)
    

@app.route('/order_confirmation/<customer_option>/<customer_id>/<customer_name>/<customer_phoneNo>/<product_id>/<product_type_name>/<product_name>/<product_price>', methods=['GET', 'POST'])
def order_confirmation(customer_option, customer_id, customer_name, customer_phoneNo, product_id, product_type_name, product_name, product_price):

    if request.method == 'POST':
        quantity = request.form['quantity']
        product_price_in_int = int(product_price)
        quantity_in_int = int(quantity)
        total_amount = quantity_in_int*product_price_in_int

        return redirect(url_for('payment_page', customer_option=customer_option, customer_id=customer_id,
                                 customer_name=customer_name, customer_phoneNo=customer_phoneNo, product_id=product_id, 
                                 product_type_name=product_type_name, product_name=product_name, product_price=product_price, 
                                 quantity=quantity, total_amount=total_amount))
    
    return render_template('order_confirmation.html', customer_id=customer_id, customer_name=customer_name, customer_phoneNo=customer_phoneNo,
            product_id=product_id, product_type_name=product_type_name, product_name=product_name, product_price=product_price)

@app.route('/payment_page/<customer_option>/<customer_id>/<customer_name>/<customer_phoneNo>/<product_id>/<product_type_name>/<product_name>/<product_price>/<quantity>/<total_amount>', methods=['GET', 'POST'])
def payment_page(customer_option, customer_id, customer_name, customer_phoneNo,product_id, product_type_name, product_name,product_price,quantity,total_amount):

    now = datetime.datetime.now()
    order_date = now.strftime("%Y-%m-%d")
    order_time = now.strftime("%H:%M:%S")

    db_cursor.execute("SELECT Order_ID FROM cafe_order")
    total_row_in_cafe_order_table_in_list = db_cursor.fetchall()
    order_id = len(total_row_in_cafe_order_table_in_list) + 1 if total_row_in_cafe_order_table_in_list else 1

    if request.method == 'POST':
        payment_method = request.form['payment_method']

        return redirect(url_for('finalize_order', customer_option=customer_option, order_id=order_id, order_date=order_date, order_time=order_time,
            customer_id=customer_id, customer_name=customer_name, customer_phoneNo=customer_phoneNo, product_id=product_id,
            product_type_name=product_type_name, product_name=product_name, product_price=product_price, quantity=quantity, total_amount=total_amount, payment_method=payment_method))

    return render_template('payment_page.html', customer_id=customer_id, customer_name=customer_name, customer_phoneNo=customer_phoneNo,
            product_id=product_id, product_type_name=product_type_name, product_name=product_name, product_price=product_price, total_amount=total_amount)

@app.route('/finalize_order/<customer_option>/<order_id>/<order_date>/<order_time>/<customer_id>/<customer_name>/<customer_phoneNo>/<product_id>/<product_type_name>/<product_name>/<product_price>/<quantity>/<total_amount>/<payment_method>', methods=['GET', 'POST'])
def finalize_order(customer_option, order_id, order_date, order_time, customer_id, customer_name, customer_phoneNo,product_id, product_type_name, product_name,product_price,quantity,total_amount,payment_method):

    db_cursor.execute("""
        INSERT INTO cafe_order (
            Order_ID, Order_Date, Order_Time, Customer_ID, Customer_Name, Phone_No,
            Product_ID, Product_Type, Product_Name, Product_Price, Quantity,
            Total_Amount, Payment_Method, Order_Status, Remarks
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (order_id, order_date, order_time, customer_id, customer_name, customer_phoneNo, product_id, product_type_name, product_name, product_price, quantity, total_amount, payment_method, 'Order Delivered', ''))
    mydb.commit()

    if customer_option == '1':
        db_cursor.execute("""
            INSERT INTO customer (Customer_ID, Customer_Name, Phone_No)
            VALUES (%s, %s, %s)
        """, (customer_id, customer_name, customer_phoneNo))
        mydb.commit()

    flash("Order recorded successfully!")
    
    return render_template('finalize_order.html', order_id=order_id, order_date=order_date, order_time=order_time, customer_id=customer_id, customer_name=customer_name, customer_phoneNo=customer_phoneNo,
            product_id=product_id, product_type_name=product_type_name, product_name=product_name, product_price=product_price, quantity=quantity, total_amount=total_amount, payment_method=payment_method)

if __name__ == '__main__':
    app.run(debug=False)
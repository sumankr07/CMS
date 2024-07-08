cafe_name = "Namaste Cafe"  # Define the name of the cafe

# Database connection parameters
db_hostname = "localhost"
db_user_name = "root"
db_password = "77777777"
db_database_name = "cafe_management_system"

import datetime
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import sys

try:
    # Establishing connection to the MySQL database
    mydb = mysql.connect(
        host=db_hostname,
        user=db_user_name,
        password=db_password,
        database=db_database_name
    )

    # Creating a cursor object to interact with the database
    db_cursor = mydb.cursor()
    print(f'\n------- Welcome to {cafe_name} -------\n')

    # Displaying the main menu options to the user
    print('Press 1 for New Order')
    print('Press 2 for Update/Cancel Order')
    print('Press 3 for Setting')
    print('Press 4 for View/Export Data')

    # Taking user input for menu selection
    main_menu1 = input('\nPlease select option :- ')

    try:
        # Converting the input to an integer
        main_menu = int(main_menu1)
    except:
        # Handling invalid input
        print("\nYou have entered the wrong value! Please try again")
        sys.exit()

    # Handling different menu options based on user selection
    if main_menu == 1:  # Handling the "New Order" option
        print(f'\n------- New Order -------\n')

        # Fetching all Order_IDs from the cafe_order table
        db_cursor.execute("select Order_ID from cafe_order")
        total_row_in_cafe_order_table_in_list = db_cursor.fetchall()

        # Determining the new order ID
        if total_row_in_cafe_order_table_in_list:
            total_row_in_cafe_order = len(total_row_in_cafe_order_table_in_list)
            order_id = total_row_in_cafe_order + 1
        else:
            order_id = 1

        now = datetime.datetime.now()  # Getting the current date and time

        # Formatting the current date and time
        order_date = now.strftime("%Y-%m-%d")
        order_time = now.strftime("%H:%M:%S")

        # Displaying customer options
        print("Press 1 for New Customer")
        print("Press 2 for Existing Customer")

        customer_menu1 = input("\nPlease select option :- ")

        try:
            # Converting the input to an integer
            customer_menu = int(customer_menu1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        if customer_menu == 1:  # Handling the "New Customer" option
            # Fetching all Customer_IDs from the customer table
            db_cursor.execute("select Customer_ID from customer")
            total_row_in_customer_table_in_list = db_cursor.fetchall()

            # Determining the new customer ID
            if total_row_in_customer_table_in_list:
                total_row_in_customer = len(total_row_in_customer_table_in_list)
                customer_id = total_row_in_customer + 1
            else:
                customer_id = 1

            customer_name1 = input("\nEnter your Name :- ")

            # Validating the customer name
            if all(char.isalpha() or char.isspace() for char in customer_name1) and len(customer_name1) >= 3:
                customer_name = customer_name1
            else:
                print("\nYou have entered the wrong name or lessthen 3 alphabet! Please try again")
                sys.exit()

            customer_phoneNo1 = input("Enter your Phone No. :- ")

            # Validating the phone number
            if customer_phoneNo1.isdigit() and len(customer_phoneNo1) == 10:
                customer_phoneNo = int(customer_phoneNo1)
                customer_phoneNo = customer_phoneNo1
            else:
                print("\nYou have entered the wrong phone no.! Please try again")
                sys.exit()

            # Displaying customer details
            print("\nName:", customer_name)
            print("Phone No.:", customer_phoneNo)

        elif customer_menu == 2:  # Handling the "Existing Customer" option
            customer_id1 = input("\nEnter your Customer ID :- ")

            try:
                # Converting the input to an integer
                customer_id = int(customer_id1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            # Fetching the customer details based on Customer_ID
            db_cursor.execute(f"select * from customer where Customer_ID = {customer_id};")
            product_data = db_cursor.fetchall()

            if product_data:
                # Extracting the customer details from the fetched data
                product_data_in_tuple = product_data[0]
                customer_id = product_data_in_tuple[0]
                customer_name = product_data_in_tuple[1]
                customer_phoneNo = product_data_in_tuple[2]

                # Displaying customer details
                print("\nName:", customer_name)
                print("Phone No.:", customer_phoneNo)
            else:
                print("\nNo customer found with Customer ID", customer_id, "! Please try again")
                sys.exit()

        else:
            # Handling invalid customer menu selection
            print("\nYour option is invalid! Please try again")
            sys.exit()

        # Fetching distinct product types from the product table
        db_cursor.execute("select distinct Product_Type from product;")
        all_product_type = db_cursor.fetchall()

        if all_product_type:
            print()

            # Displaying product type options
            for i, j in enumerate(all_product_type):
                total_product_type = i + 1
                print("Press ", total_product_type, " for :- ", j[0])

            product_type_response1 = input("\nPlease select product type :- ")

            try:
                # Converting the input to an integer
                product_type_response = int(product_type_response1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if total_product_type >= product_type_response >= 1:
                # Fetching the selected product type details
                product_type_index = product_type_response - 1
                product_type_name_in_tuple = all_product_type[product_type_index]
                product_type_name = product_type_name_in_tuple[0]

                # Fetching products based on selected product type
                db_cursor.execute(f"select Product_Name, Product_Price from product where Product_Type = '{product_type_name}';")
                all_product_name = db_cursor.fetchall()
                print(type(all_product_type))
                print(all_product_type)

                # Displaying product options
                for i, j in enumerate(all_product_name):
                    total_product_name = i + 1
                    print("Press ", total_product_name, " for :- ", j[0], "  ₹", j[1])

                product_name_response1 = input("\nPlease select product :- ")

                try:
                    # Converting the input to an integer
                    product_name_response = int(product_name_response1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if total_product_name >= product_name_response >= 1:
                    # Fetching the selected product details
                    product_name_index = product_name_response - 1
                    product_name_in_tuple = all_product_name[product_name_index]
                    product_name_for_search = product_name_in_tuple[0]
                else:
                    # Handling invalid product selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()
    
            else:
                # Handling invalid product type selection
                print("\nYour option is invalid! Please try again")
                sys.exit()
        else:
            print("\nThere are no products in your database! Please try again")
            sys.exit()

        # Fetching the product details based on product name
        db_cursor.execute(f"select * from product where Product_Name = '{product_name_for_search}';")
        product_data = db_cursor.fetchall()

        if product_data:
            # Extracting product details from the fetched data
            product_data_in_tuple = product_data[0]
            product_id = product_data_in_tuple[0]
            product_type = product_data_in_tuple[1]
            product_name = product_data_in_tuple[2]
            product_price = product_data_in_tuple[3]
        else:
            print("\nUnable to extract product data")
            sys.exit()

        quantity1 = input("\nEnter Quantity :- ")

        try:
            # Converting the input to an integer
            quantity = int(quantity1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        if quantity == 0:
            # Handling invalid quantity input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        # Calculating the total amount
        total_amount = product_price * quantity

        # Displaying order details
        print("\nProduct ID:", product_id)
        print("Product Type:", product_type)
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Total Amount:", total_amount)

        print("\nPlease confirm that you want to continue this order")

        print("\nPress 1 for Yes")
        print("Press 2 for No")

        order_confirmation1 = input("\nPlease select option :- ")

        try:
            # Converting the input to an integer
            order_confirmation = int(order_confirmation1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        if order_confirmation == 1:  # Handling order confirmation
            # Displaying payment method options
            print("\nPress 1 for Cash")
            print("Press 2 for UPI")
            print("Press 3 for Debit Card")
            print("Press 4 for Credit Card")

            option_for_payment1 = input("\nPlease Select Payment Method :- ")

            try:
                # Converting the input to an integer
                option_for_payment = int(option_for_payment1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            # Determining the selected payment method
            if option_for_payment == 1:
                payment_method = "Cash"
            elif option_for_payment == 2:
                payment_method = "UPI"
            elif option_for_payment == 3:
                payment_method = "Debit Card"
            elif option_for_payment == 4:
                payment_method = "Credit Card"
            else:
                # Handling invalid payment method selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

            order_status = "Order Delivered"  # Setting order status
            remarks = ""  # Initializing remarks

            # Inserting the new order details into the cafe_order table
            db_cursor.execute("""
                insert into cafe_order (
                    Order_ID,
                    Order_Date,
                    Order_Time,
                    Customer_ID,
                    Customer_Name,
                    Phone_No,
                    Product_ID,
                    Product_Type,
                    Product_Name,
                    Product_Price,
                    Quantity,
                    Total_Amount,
                    Payment_Method,
                    Order_Status,
                    Remarks
                ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (order_id, order_date, order_time, customer_id, customer_name, customer_phoneNo, product_id, product_type, product_name, product_price, quantity, total_amount, payment_method, order_status, remarks))

            mydb.commit()  # Committing the transaction

            if customer_menu == 1:  # Handling new customer insertion
                db_cursor.execute("""
                    insert into customer (
                        Customer_ID,
                        Customer_Name,
                        Phone_No
                    ) values(%s ,%s ,%s)
                """, (customer_id, customer_name, customer_phoneNo))
                
                mydb.commit()  # Committing the transaction

            # Displaying the final order details
            print("\nOrder ID:", order_id)
            print("Order Date:", order_date)
            print("Order Time:", order_time)

            print("Customer ID:", customer_id)
            print("Name:", customer_name)
            print("Phone No.:", customer_phoneNo)

            print("Product ID:", product_id)
            print("Product Type:", product_type)
            print("Product Name:", product_name)
            print("Product Price:", product_price)

            print("Quantity:", quantity)
            print("Total Amount:", total_amount)
            print("Payment Method:", payment_method)
            print("Order Status:", order_status)
            print("Remarks:", remarks)

            print("\nOrder Recorded!")  # Confirming the order recording

        elif order_confirmation == 2:  # Handling order cancellation
            print("\nYour order has been not generated!")
            sys.exit()

        else:
            # Handling invalid order confirmation selection
            print("\nYour option is invalid! Please try again")
            sys.exit()

    elif main_menu == 2:  # Handling the "Update/Cancel Order" option
        print(f'\n------- Update/Cancel Order -------\n')

        # Prompting the user to enter the Order ID they want to update or cancel
        order_id1 = input("Enter your Order ID which you want to update/cancel :- ")
        try:
            # Converting the input to an integer
            order_id = int(order_id1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        # Fetching the order details based on the Order ID
        db_cursor.execute(f"select * from cafe_order where Order_ID = {order_id};")
        order_data = db_cursor.fetchall()

        if order_data:
            # Extracting order details from the fetched data
            order_data_in_tuple = order_data[0]

            order_id = order_data_in_tuple[0]
            order_date = order_data_in_tuple[1]
            order_time = order_data_in_tuple[2]

            customer_id = order_data_in_tuple[3]
            customer_name = order_data_in_tuple[4]
            customer_phoneNo = order_data_in_tuple[5]

            product_id = order_data_in_tuple[6]
            product_type = order_data_in_tuple[7]
            product_name = order_data_in_tuple[8]
            product_price = order_data_in_tuple[9]

            quantity = order_data_in_tuple[10]
            total_amount = order_data_in_tuple[11]
            payment_method = order_data_in_tuple[12]
            order_status = order_data_in_tuple[13]
            remarks = order_data_in_tuple[14]

        else:
            # Handling the case where no order is found with the provided Order ID
            print("\nNo order found with Order ID", order_id, "! Please try again")
            sys.exit()

        # Displaying the existing order details
        print("\nOrder ID:", order_id)
        print("Order Date:", order_date)
        print("Order Time:", order_time)

        print("Customer ID:", customer_id)
        print("Name:", customer_name)
        print("Phone No.:", customer_phoneNo)

        print("Product ID:", product_id)
        print("Product Type:", product_type)
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Quantity:", quantity)
        print("Total Amount:", total_amount)
        print("Payment Method:", payment_method)
        print("Order Status:", order_status)
        print("Remarks:", remarks)

        # Prompting the user to choose between updating or canceling the order
        print("\nPress 1 for Update Order")
        print("Press 2 for Cancel Order")
        order_menu1 = input("\nPlease select option :- ")

        try:
            # Converting the input to an integer
            order_menu = int(order_menu1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        if order_menu == 1:  # Handling the "Update Order" option
            # Fetching distinct product types from the product table
            db_cursor.execute("select distinct Product_Type from product;")
            all_product_type = db_cursor.fetchall()
            print()

            # Displaying product type options
            for i, j in enumerate(all_product_type):
                total_product_type = i + 1
                print("Press ", total_product_type, " for :- ", j[0])

            product_type_response1 = input("\nPlease select product type :- ")

            try:
                # Converting the input to an integer
                product_type_response = int(product_type_response1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if total_product_type >= product_type_response >= 1:
                # Fetching the selected product type details
                product_type_index = product_type_response - 1
                product_type_name_in_tuple = all_product_type[product_type_index]
                product_type_name = product_type_name_in_tuple[0]

                # Fetching products based on selected product type
                db_cursor.execute(f"select Product_Name, Product_Price from product where Product_Type = '{product_type_name}';")
                all_product_name = db_cursor.fetchall()
                print()

                # Displaying product options
                for i, j in enumerate(all_product_name):
                    total_product_name = i + 1
                    print("Press ", total_product_name, " for :- ", j[0], "  ₹", j[1])

                product_name_response1 = input("\nPlease select product :- ")

                try:
                    # Converting the input to an integer
                    product_name_response = int(product_name_response1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if total_product_name >= product_name_response >= 1:
                    # Fetching the selected product details
                    product_name_index = product_name_response - 1
                    product_name_in_tuple = all_product_name[product_name_index]
                    product_name_for_search = product_name_in_tuple[0]
                else:
                    # Handling invalid product selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()
            else:
                # Handling invalid product type selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

            # Fetching the product details based on product name
            db_cursor.execute(f"select * from product where Product_Name = '{product_name_for_search}';")
            product_data = db_cursor.fetchall()

            if product_data:
                # Extracting product details from the fetched data
                product_data_in_tuple = product_data[0]
                product_id = product_data_in_tuple[0]
                product_type = product_data_in_tuple[1]
                product_name = product_data_in_tuple[2]
                product_price = product_data_in_tuple[3]
            else:
                # Handling the case where product data extraction fails
                print("\nUnable to extract product data")
                sys.exit()

            # Prompting the user to enter the quantity
            quantity1 = input("\nEnter Quantity :- ")

            try:
                # Converting the input to an integer
                quantity = int(quantity1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if quantity == 0:
                # Handling invalid quantity input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            # Calculating the total amount
            total_amount = product_price * quantity

            # Displaying the updated order details
            print("\nProduct ID:", product_id)
            print("Product Type:", product_type)
            print("Product Name:", product_name)
            print("Product Price:", product_price)
            print("Total Amount:", total_amount)

            print("\nPlease confirm that you want to continue this order")

            print("\nPress 1 for Yes")
            print("Press 2 for No")

            order_confirmation1 = input("\nPlease select option :- ")

            try:
                # Converting the input to an integer
                order_confirmation = int(order_confirmation1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if order_confirmation == 1:  # Handling order confirmation
                # Displaying payment method options
                print("\nPress 1 for Cash")
                print("Press 2 for UPI")
                print("Press 3 for Debit Card")
                print("Press 4 for Credit Card")

                option_for_payment1 = input("\nPlease Select Payment Method :- ")

                try:
                    # Converting the input to an integer
                    option_for_payment = int(option_for_payment1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                # Determining the selected payment method
                if option_for_payment == 1:
                    payment_method = "Cash"
                elif option_for_payment == 2:
                    payment_method = "UPI"
                elif option_for_payment == 3:
                    payment_method = "Debit Card"
                elif option_for_payment == 4:
                    payment_method = "Credit Card"
                else:
                    # Handling invalid payment method selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()

                # Updating the order details in the cafe_order table
                db_cursor.execute("""
                    update cafe_order
                    set Product_ID = %s,
                        Product_Type = %s,
                        Product_Name = %s,
                        Product_Price = %s,
                        Quantity = %s,
                        Total_Amount = %s,
                        Payment_Method = %s
                    where Order_ID = %s
                """, (product_id, product_type, product_name, product_price, quantity, total_amount, payment_method, order_id))

                mydb.commit()  # Committing the transaction

                # Displaying the updated order details
                print("\nOrder ID:", order_id)
                print("Order Date:", order_date)
                print("Order Time:", order_time)

                print("Customer ID:", customer_id)
                print("Name:", customer_name)
                print("Phone No.:", customer_phoneNo)

                print("Product ID:", product_id)
                print("Product Type:", product_type)
                print("Product Name:", product_name)
                print("Product Price:", product_price)

                print("Quantity:", quantity)
                print("Total Amount:", total_amount)
                print("Payment Method:", payment_method)
                print("Order Status:", order_status)
                print("Remarks:", remarks)

                print("\nOrder Details Updated!!")

            elif order_confirmation == 2:  # Handling order update cancellation
                print("\nYour order has been not updated!")
                sys.exit()
            else:
                # Handling invalid order confirmation selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

        elif order_menu == 2:  # Handling the "Cancel Order" option
            print(f"\nPlease confirm that you want to cancel the order ID {order_id}")

            print("\nPress 1 for Yes")
            print("Press 2 for No")

            order_cancellation1 = input("\nPlease select option :- ")

            try:
                # Converting the input to an integer
                order_cancellation = int(order_cancellation1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if order_cancellation == 1:  # Handling order cancellation confirmation
                order_status = "Order Cancelled"
                # Prompting the user to provide a reason for order cancellation
                remarks = input("Why you want to cancel order: :- ")

                # Updating the order status and remarks in the cafe_order table
                db_cursor.execute("""
                    update cafe_order
                    set Order_Status = %s,
                        Remarks = %s
                    where Order_ID = %s
                """, (order_status, remarks, order_id))

                mydb.commit()  # Committing the transaction

                # Displaying the order cancellation confirmation message
                print(f"\nYour order id {order_id} has been canceled due to \"{remarks}\".")

            elif order_cancellation == 2:  # Handling order cancellation rejection
                print("\nYour order has been not cancelled!")
                sys.exit()
            else:
                # Handling invalid order cancellation selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

        else:
            # Handling invalid main menu selection
            print("\nYour option is invalid! Please try again")
            sys.exit()

    elif main_menu == 3:  # Handling the "Setting" option
        print(f'\n------- Setting -------\n')

        # Displaying setting options
        print('Press 1 for Add Customer')
        print('Press 2 for Update Customer')
        print('Press 3 for Add Product')
        print('Press 4 for Update Product')
        print('Press 5 for Create table in Database')
        print('Press 6 for Custom SQL Query')

        setting_menu1 = input('\nPlease select option :- ')

        try:
            # Converting the input to an integer
            setting_menu = int(setting_menu1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        if setting_menu == 1:  # Handling the "Add Customer" option
            # Fetching existing customer IDs
            db_cursor.execute("select Customer_ID from customer")
            total_row_in_customer_table_in_list = db_cursor.fetchall()

            if total_row_in_customer_table_in_list:
                # Determining the next customer ID
                total_row_in_customer = len(total_row_in_customer_table_in_list)
                customer_id = total_row_in_customer + 1
            else:
                customer_id = 1

            # Prompting the user to enter the customer's name
            customer_name1 = input("\nEnter your Name :- ")

            if all(char.isalpha() or char.isspace() for char in customer_name1) and len(customer_name1) >= 3:
                customer_name = customer_name1
            else:
                # Handling invalid name input
                print("\nYou have entered the wrong name or less than 3 alphabets! Please try again")
                sys.exit()

            # Prompting the user to enter the customer's phone number
            customer_phoneNo1 = input("Enter your Phone No. :- ")

            if customer_phoneNo1.isdigit() and len(customer_phoneNo1) == 10:
                customer_phoneNo = int(customer_phoneNo1)
                customer_phoneNo = customer_phoneNo1
            else:
                # Handling invalid phone number input
                print("\nYou have entered the wrong phone no.! Please try again")
                sys.exit()

            # Inserting the new customer into the customer table
            db_cursor.execute("""
                insert into customer (
                    Customer_ID,
                    Customer_Name,
                    Phone_No
                ) values(%s ,%s ,%s)
            """, (customer_id, customer_name, customer_phoneNo))

            mydb.commit()  # Committing the transaction

            # Displaying the new customer details
            print("\nCustomer ID", customer_id)
            print("Name:", customer_name)
            print("Phone No.:", customer_phoneNo)
            print("\nCustomer added successfully")

        elif setting_menu == 2:  # Handling the "Update Customer" option
            # Prompting the user to enter the Customer ID to be updated
            customer_id1 = input("\nEnter your Customer ID :- ")
            try:
                customer_id = int(customer_id1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            # Fetching the customer details based on the Customer ID
            db_cursor.execute(f"select * from customer where Customer_ID = {customer_id};")
            product_data = db_cursor.fetchall()

            if product_data:
                # Extracting customer details from the fetched data
                product_data_in_tuple = product_data[0]
                customer_id = product_data_in_tuple[0]
                customer_name = product_data_in_tuple[1]
                customer_phoneNo = product_data_in_tuple[2]

                # Displaying the existing customer details
                print("\nCustomer ID:", customer_id)
                print("Name:", customer_name)
                print("Phone No.:", customer_phoneNo)
            else:
                # Handling the case where no customer is found with the provided Customer ID
                print("\nNo customer found with Customer ID", customer_id, "! Please try again")
                sys.exit()

            # Prompting the user to confirm the update
            print(f"\nPlease confirm that you want to update customer ID {customer_id}")
            print("\nPress 1 for Yes")
            print("Press 2 for No")

            customer_update1 = input("\nPlease select option :- ")

            try:
                # Converting the input to an integer
                customer_update = int(customer_update1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if customer_update == 1:  # Handling update confirmation
                # Prompting the user to enter the new name
                customer_name1 = input("\nEnter your Name :- ")

                if all(char.isalpha() or char.isspace() for char in customer_name1) and len(customer_name1) >= 3:
                    customer_name = customer_name1
                else:
                    # Handling invalid name input
                    print("\nYou have entered the wrong name or less than 3 alphabets! Please try again")
                    sys.exit()

                # Prompting the user to enter the new phone number
                customer_phoneNo1 = input("Enter your Phone No. :- ")

                if customer_phoneNo1.isdigit() and len(customer_phoneNo1) == 10:
                    customer_phoneNo = int(customer_phoneNo1)
                    customer_phoneNo = customer_phoneNo1
                else:
                    # Handling invalid phone number input
                    print("\nYou have entered the wrong phone no.! Please try again")
                    sys.exit()

                # Updating the customer details in the cafe_order table
                db_cursor.execute("""
                    update cafe_order
                    set Customer_Name = %s,
                        Phone_No = %s
                    where Customer_ID = %s
                """, (customer_name, customer_phoneNo, customer_id))

                mydb.commit()  # Committing the transaction

                # Updating the customer details in the customer table
                db_cursor.execute("""
                    update customer
                    set Customer_Name = %s,
                        Phone_No = %s
                    where Customer_ID = %s
                """, (customer_name, customer_phoneNo, customer_id))

                mydb.commit()  # Committing the transaction

                # Displaying the updated customer details
                print("\nCustomer ID:", customer_id)
                print("Name:", customer_name)
                print("Phone No.:", customer_phoneNo)
                print("\nYour details have been updated!")

            elif customer_update == 2:  # Handling update rejection
                print("\nYour customer has not been updated!")
                sys.exit()
            else:
                # Handling invalid update confirmation selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

        elif setting_menu == 3:  # Handling the "Add Product" option
            # Fetching existing product IDs
            db_cursor.execute("select Product_ID from product")
            total_row_in_product_table_in_list = db_cursor.fetchall()

            if total_row_in_product_table_in_list:
                # Determining the next product ID
                total_row_in_product = len(total_row_in_product_table_in_list)
                product_id = total_row_in_product + 1
            else:
                product_id = 1

            # Prompting the user to enter the product type
            product_type = input("\nEnter Product Type :- ")

            # Prompting the user to enter the product name
            product_name = input("Enter Product Name :- ")

            # Prompting the user to enter the product price
            product_price1 = input("Enter Product Price :- ")

            try:
                # Converting the input to an integer
                product_price = int(product_price1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            # Inserting the new product into the product table
            db_cursor.execute("""
                insert into product (
                    Product_ID,
                    Product_Type,
                    Product_Name,
                    Product_Price
                ) values(%s ,%s ,%s ,%s)
            """, (product_id, product_type, product_name, product_price))

            mydb.commit()  # Committing the transaction

            # Displaying the new product details
            print("\nProduct ID:", product_id)
            print("Product Type:", product_type)
            print("Product Name:", product_name)
            print("Product Price:", product_price)
            print("\nProduct added successfully!")

        elif setting_menu == 4:  # Handling the "Update Product" option
            # Prompting the user to enter the Product ID to be updated
            product_id1 = input("\nEnter your Product ID :- ")

            try:
                # Converting the input to an integer
                product_id = int(product_id1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            # Fetching the product details based on the Product ID
            db_cursor.execute(f"select * from product where product_ID = {product_id};")
            product_data = db_cursor.fetchall()

            if product_data:
                # Extracting product details from the fetched data
                product_data_in_tuple = product_data[0]
                product_id = product_data_in_tuple[0]
                product_type = product_data_in_tuple[1]
                product_name = product_data_in_tuple[2]
                product_price = product_data_in_tuple[3]

                # Displaying the existing product details
                print("\nProduct Type:", product_type)
                print("Product Name:", product_name)
                print("Product Price:", product_price)
            else:
                # Handling the case where no product is found with the provided Product ID
                print("\nNo product found with Product ID", product_id, "! Please try again")
                sys.exit()

            # Prompting the user to confirm the update
            print(f"\nPlease confirm that you want to update product ID {product_id}")
            print("\nPress 1 for Yes")
            print("Press 2 for No")

            create_table1 = input("\nPlease select option :- ")

            try:
                # Converting the input to an integer
                create_table = int(create_table1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if create_table == 1:  # Handling update confirmation
                # Prompting the user to enter the new product type
                product_type = input("\nEnter Product Type :- ")

                # Prompting the user to enter the new product name
                product_name = input("Enter Product Name :- ")

                # Prompting the user to enter the new product price
                product_price1 = input("Enter Product Price :- ")

                try:
                    # Converting the input to an integer
                    product_price = int(product_price1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                # Updating the product details in the product table
                db_cursor.execute("""
                    update product
                    set Product_Type = %s,
                        Product_Name = %s,
                        Product_Price = %s
                    where Product_ID = %s
                """, (product_type, product_name, product_price, product_id))

                mydb.commit()  # Committing the transaction

                # Displaying the updated product details
                print("\nProduct ID:", product_id)
                print("Product Type:", product_type)
                print("Product Name:", product_name)
                print("Product Price:", product_price)
                print("\nYour details have been updated!")

            elif create_table == 2:  # Handling update rejection
                print("\nYour product has not been updated!")
                sys.exit()
            else:
                # Handling invalid update confirmation selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

        elif setting_menu == 5:  # Handling the "Create table in Database" option
            # Prompting the user to confirm the creation of new tables
            print(f"\nPlease confirm that you want to create table in {db_database_name}")
            print("\nPress 1 for Yes")
            print("Press 2 for No")

            create_table1 = input("\nPlease select option :- ")

            try:
                # Converting the input to an integer
                create_table = int(create_table1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if create_table == 1:  # Handling table creation confirmation
                try:
                    # Creating the customer1 table
                    db_cursor.execute("""
                        create table customer (
                            Customer_ID INT,
                            Customer_Name VARCHAR(40),
                            Phone_No BIGINT
                        )
                    """)

                    # Creating the product1 table
                    db_cursor.execute("""
                        create table product (
                            Product_ID INT,
                            Product_Type VARCHAR(40),
                            Product_Name VARCHAR(40),
                            Product_Price INT
                        )
                    """)

                    # Creating the cafe_order1 table
                    db_cursor.execute("""
                        create table cafe_order (
                            Order_ID INT,
                            Order_Date DATE,
                            Order_Time TIME,
                            Customer_ID INT,
                            Customer_Name VARCHAR(40),
                            Phone_No BIGINT,
                            Product_ID INT,
                            Product_Type VARCHAR(40),
                            Product_Name VARCHAR(40),
                            Product_Price INT,
                            Quantity INT,
                            Total_Amount INT,
                            Payment_Method VARCHAR(20),
                            Order_Status VARCHAR(20),
                            Remarks VARCHAR(200)
                        )
                    """)
                    print("\nTable Created!")
                except:
                    # Handling errors during table creation
                    print("\nSomething went wrong!")
                    sys.exit()

            elif create_table == 2:  # Handling table creation rejection
                print("\nExit!")
                sys.exit()
            else:
                # Handling invalid table creation confirmation selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

        elif setting_menu == 6:  # Handling the "Custom SQL Query" option
            print(f"\nThis is very risky. Please confirm that you want to make changes to your database.")

            print("\nPress 1 for Yes")
            print("Press 2 for No")

            custom_query1 = input("\nPlease select option :- ")

            try:
                # Converting the input to an integer
                custom_query = int(custom_query1)
            except:
                # Handling invalid input
                print("\nYou have entered the wrong value! Please try again")
                sys.exit()

            if custom_query == 1:  # Handling custom query confirmation
                # Prompting the user to enter a custom SQL query 
                custom_sqlcmd = input("\nEnter the MySQL query for the change you want to make to the database in single line:- ")

                try:
                        db_cursor.execute(f"{custom_sqlcmd}")
                        mydb.commit() # Committing the Query
                        print("\nQuery successfully executed!")

                except:
                    # Handling invalid SQL query
                    print("\nYou have entered the wrong Query! Please try again")
                    sys.exit()

            elif custom_query == 2:  # Handling custom query rejection
                print("\nExit!")
                sys.exit()

            else:
                # Handling invalid custom query confirmation selection
                print("\nYour option is invalid! Please try again")
                sys.exit()

        else:
            # Handling invalid main menu selection
            print("\nYour option is invalid! Please try again")
            sys.exit()

    elif main_menu == 4:  # Handling the "View/Export Data" option
        print(f'\n------- View/Export Data -------\n')

        # Displaying view/export data options
        print('Press 1 for View Customer Data')
        print('Press 2 for View Product Data')
        print('Press 3 for View Cancel Cafe Order Data')
        print('Press 4 for View Cafe Order Data')
        print('Press 5 for View Custom Data')

        view_data_menu1 = input('\nPlease select option :- ')

        try:
            # Converting the input to an integer
            view_data_menu = int(view_data_menu1)
        except:
            # Handling invalid input
            print("\nYou have entered the wrong value! Please try again")
            sys.exit()

        if view_data_menu == 1:  # Handling the "View Customer Data" option
            db_cursor.execute("select * from product")
            product_data = db_cursor.fetchall()

            print("")

            if product_data:
                # Displaying product data
                for i in product_data:
                    print(i)
                
                print(f"\nPlease confirm that you want to export in excel")

                print("\nPress 1 for Yes")
                print("Press 2 for No")

                create_table1 = input("\nPlease select option :- ")

                try:
                    # Converting the input to an integer
                    create_table = int(create_table1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if create_table == 1:  # Handling export confirmation
                    try:
                        # Creating and saving the Excel file
                        df = pd.DataFrame(product_data, columns=["ID", "Category", "Name", "Price"])
                        file_path = "product.xlsx"
                        df.to_excel(file_path, index=False)
                        print(f"\nExcel file saved as \"{file_path}\"")
                    except:
                        # Handling errors during export
                        print("\nUnable to export in excel!")
                        sys.exit()

                elif create_table == 2:  # Handling export rejection
                    print("\nExit!")
                    sys.exit()

                else:
                    # Handling invalid export confirmation selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()

            else:
                # Handling no data found
                print("\nNo Data found! Please try again")
                sys.exit()

        elif view_data_menu == 2:  # Handling the "View Product Data" option
            db_cursor.execute("select * from customer")
            customer_data = db_cursor.fetchall()

            print("")

            if customer_data:
                # Displaying customer data
                for i in customer_data:
                    print(i)
                
                print(f"\nPlease confirm that you want to export in excel")

                print("\nPress 1 for Yes")
                print("Press 2 for No")

                customer_export1 = input("\nPlease select option :- ")

                try:
                    # Converting the input to an integer
                    customer_export = int(customer_export1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if customer_export == 1:  # Handling export confirmation
                    try:
                        # Creating and saving the Excel file
                        df = pd.DataFrame(customer_data, columns=["ID", "Name", "Phone No."])
                        file_path = "customer.xlsx"
                        df.to_excel(file_path, index=False)
                        print(f"\nExcel file saved as \"{file_path}\"")
                    except:
                        # Handling errors during export
                        print("\nUnable to export in excel!")
                        sys.exit()

                elif customer_export == 2:  # Handling export rejection
                    print("\nExit!")
                    sys.exit()

                else:
                    # Handling invalid export confirmation selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()

            else:
                # Handling no data found
                print("\nNo product found! Please try again")
                sys.exit()

        elif view_data_menu == 3:  # Handling the "View Cancel Cafe Order Data" option
            db_cursor.execute("select * from cafe_order where Order_Status = 'Order Cancelled';")
            cafe_cancel_order_data = db_cursor.fetchall()

            print("")

            if cafe_cancel_order_data:
                # Displaying canceled order data
                for i in cafe_cancel_order_data:
                    print(i)
                
                print(f"\nPlease confirm that you want to export in excel")

                print("\nPress 1 for Yes")
                print("Press 2 for No")

                cafe_cancel_order_export1 = input("\nPlease select option :- ")

                try:
                    # Converting the input to an integer
                    cafe_cancel_order_export = int(cafe_cancel_order_export1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if cafe_cancel_order_export == 1:  # Handling export confirmation
                    try:
                        # Creating and saving the Excel file
                        df = pd.DataFrame(cafe_cancel_order_data, columns=["Order ID", "Order Date", "Order Time", "Customer ID", "Customer Name", "Phone No.", "Product ID", "Product Type", "Product Name", "Price", "Quantity", "Total Amount", "Payment Method","Order Status","Remarks"])
                        file_path = "cafe_cancel_order.xlsx"
                        df.to_excel(file_path, index=False)
                        print(f"\nExcel file saved as \"{file_path}\"")
                    except:
                        # Handling errors during export
                        print("\nUnable to export in excel!")
                        sys.exit()

                elif cafe_cancel_order_export == 2:  # Handling export rejection
                    print("\nExit!")
                    sys.exit()

                else:
                    # Handling invalid export confirmation selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()

            else:
                # Handling no data found
                print("\nNo Data found! Please try again")
                sys.exit()

        elif view_data_menu == 4:  # Handling the "View Cafe Order Data" option
            db_cursor.execute("select * from cafe_order where Order_Status = 'Order Delivered';")
            cafe_order_data = db_cursor.fetchall()

            print("")

            if cafe_order_data:
                # Displaying delivered order data
                for i in cafe_order_data:
                    print(i)
                
                print(f"\nPlease confirm that you want to export in excel")

                print("\nPress 1 for Yes")
                print("Press 2 for No")

                cafe_order_export1 = input("\nPlease select option :- ")

                try:
                    # Converting the input to an integer
                    cafe_order_export = int(cafe_order_export1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if cafe_order_export == 1:  # Handling export confirmation
                    try:
                        # Creating and saving the Excel file
                        df = pd.DataFrame(cafe_order_data, columns=["Order ID", "Order Date", "Order Time", "Customer ID", "Customer Name", "Phone No.", "Product ID", "Product Type", "Product Name", "Price", "Quantity", "Total Amount", "Payment Method","Order Status","Remarks"])
                        file_path = "cafe_order.xlsx"
                        df.to_excel(file_path, index=False)
                        print(f"\nExcel file saved as \"{file_path}\"")
                    except:
                        # Handling errors during export
                        print("\nUnable to export in excel!")
                        sys.exit()

                elif cafe_order_export == 2:  # Handling export rejection
                    print("\nExit!")
                    sys.exit()

                else:
                    # Handling invalid export confirmation selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()

            else:
                # Handling no data found
                print("\nNo Data found! Please try again")
                sys.exit()

        elif view_data_menu == 5:  # Handling the "View Custom Data" option
            # Prompting the user to enter a custom SQL query
            sqlcmd = input("\nEnter the MySQL query you want to view:- ")

            try:
                # Executing the custom SQL query
                db_cursor.execute(f"{sqlcmd}")
                custom_data = db_cursor.fetchall()
            except:
                # Handling invalid SQL query
                print("\nYou have entered the wrong Query! Please try again")
                sys.exit()

            print("")

            if custom_data:
                # Displaying custom data
                for i in custom_data:
                    print(i)
                
                print(f"\nPlease confirm that you want to export in excel")

                print("\nPress 1 for Yes")
                print("Press 2 for No")

                custom_data_export1 = input("\nPlease select option :- ")

                try:
                    # Converting the input to an integer
                    custom_data_export = int(custom_data_export1)
                except:
                    # Handling invalid input
                    print("\nYou have entered the wrong value! Please try again")
                    sys.exit()

                if custom_data_export == 1:  # Handling export confirmation
                    try:
                        # Creating and saving the Excel file
                        df = pd.DataFrame(custom_data)
                        file_path = "custom.xlsx"
                        df.to_excel(file_path, index=False)
                        print(f"\nExcel file saved as \"{file_path}\"")
                    except:
                        # Handling errors during export
                        print("\nUnable to export in excel!")
                        sys.exit()

                elif custom_data_export == 2: # Handling export rejection
                    print("\nExit!")
                    sys.exit()
                else:
                    # Handling invalid export confirmation selection
                    print("\nYour option is invalid! Please try again")
                    sys.exit()

            else:
                # Handling no data found
                print("\nNo Data found! Please try again")
                sys.exit()

        else:
            # Handling invalid menu option
            print("\nYour option is invalid! Please try again")
            sys.exit()

    else:
        # Handling invalid menu selection
        print("\nYour option is invalid! Please try again")
        sys.exit()

except Error as e:
    # Printing MySQL error message
    print(f"\nMySQL Error :- {e}")

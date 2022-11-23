from mysql.connector import connect

# connection information
hostname = "localhost"
user_name = "root"
pwd = "147!@#rewqSQL"
base = "essential_books"


def execute_and_commit_query(query):
    """Creates connection and cursor for a query.
    :param:
        query - MYSQL query for desired information"""
    # Create connection object with connection info
    with connect(host=hostname, user=user_name, password=pwd, database=base) as mysql_connection_object:
        # Create a cursor object
        with mysql_connection_object.cursor() as mysql_cursor:
            # Execute the statement
            mysql_cursor.execute(query)
            # Commit Change
            mysql_connection_object.commit()


def add_customer(l_name: str, email: str, phone: str, delivery_address: str, postal_code: str):
    """
    Try to execute MYSQL query for inserting a customer into the customer table
    :param:
        l_name : str
            Customer last name
        email : str
            Customer email
        phone : str
            Customer Phone number
        delivery_address : str
            Customer address
        postal_code : str
            Customer Postal code
    """
    try:
        add_customer_insert_statement = f"""INSERT INTO customer (l_name, email, phone, delivery_address, postal_code)
                                        VALUES
                                        ("{l_name}", "{email}", "{phone}", "{delivery_address}", "{postal_code}");"""
        execute_and_commit_query(add_customer_insert_statement)
        # error handling if insert statement does not work correctly
    except Exception as e:
        return str(e)
    else:
        return 0


def lookup_customer(customer_detail):
    """
    MYSQL SELECT query for finding a customer's customer_id based on l_name, email or phone number
    :param:
        customer_detail : str
            Customer detail to lookup - either an l_name, email or phone
    """
    return get_result(f"""SELECT customer_id FROM customer 
                            WHERE customer.l_name="{customer_detail}" 
                                OR customer.email="{customer_detail}"
                                OR customer.phone="{customer_detail}";""")


def update_inventory(isbn: str, change_amount: int):
    """
    MYSQL SELECT query to find current stock and UPDATE query to update inventory if enough stock.
    Raises value error if not enough stock
    :param:
        isbn : str
            book isbn
        change_amount : int
            Amount stock should be changed by
    """
    find_stock_statement = f"""SELECT book.stock FROM book WHERE book.isbn = "{isbn}";"""
    stock = get_result(find_stock_statement)
    print(stock)
    new_stock = stock[0][0] + change_amount
    if new_stock < 0:
        raise ValueError(f"Cannot have negative stock. Current Stock: {stock} Change Requested: {change_amount}")
    try:
        update_inventory_statement = f"""UPDATE book SET book.stock = {new_stock}
                                         WHERE book.isbn = "{isbn}";"""
        execute_and_commit_query(update_inventory_statement)
    except Exception as e:
        return str(e)  # not ideal
    else:
        return 0


def get_result(query):
    """
    Creates MYSQL connection and cursor for returning result
    :param:
        query
            MYSQL SELECT query
    """
    with connect(host=hostname, user=user_name, password=pwd, database=base) as mysql_connection_object:
        with mysql_connection_object.cursor() as mysql_cursor:
            mysql_cursor.execute(query)
            result = mysql_cursor.fetchall()
            mysql_cursor.close()
        mysql_connection_object.commit()
    return result


def list_zero_stock():
    """MYSQL SELECT query for finding books with stock = 0"""
    return get_result(f"""SELECT ISBN, title FROM book WHERE book.stock = 0;""")


def list_all_stock():
    """MYSQL SELECT query for finding all books"""
    return get_result(f"""SELECT ISBN, title, stock FROM book;""")


def get_active_customers():
    """MYSQL SELECT query for finding customers active within the last month"""
    return get_result(f"""SELECT DISTINCT customer.l_name, customer.email, customer.phone
                                FROM customer INNER JOIN the_order
                                ON customer.customer_id = the_order.customer_id
                                INNER JOIN invoice ON the_order.order_id = invoice.order_id
                                WHERE sale_date BETWEEN NOW() - INTERVAL 31 DAY AND NOW();""")


def start_new_order(customer_id: int):
    """
    Try to insert new record in the_order table with customer_id, and return the auto_incremented order_id
    :param:
        customer_id : int
            ID associated with customer. can be found by using lookup_customer
    """
    try:
        start_new_order_insert_statement = f"""INSERT INTO the_order (customer_id)
                                            VALUES ("{customer_id}");"""
        execute_and_commit_query(start_new_order_insert_statement)
        return get_result(f"""SELECT MAX(order_id) FROM the_order WHERE customer_id = "{customer_id}";""")
    except Exception as e:
        return str(e)


def add_to_order(order_id: int, isbn: str, count: int):
    """
    Try to insert book details into the book_order table for the associated order
    :param:
        order_id : int
            order_id of the order
        isbn: str
            isbn of book
        count: int
            number of this book being ordered
    """
    try:
        add_to_order_insert_statement = f"""INSERT INTO book_order (order_id, isbn, count)
                                            VALUES ("{order_id}", "{isbn}", "{count}");"""
        execute_and_commit_query(add_to_order_insert_statement)
    except Exception as e:
        return str(e)
    else:
        return 0


def generate_invoice(order_id: int):
    """
    Try to insert invoice info into the invoice table for the associated order
    :param:
        order_id : int
            order_id of the order
    """
    try:
        fill_invoice_insert_statement = f"""INSERT INTO invoice (order_id, total, num_items, sale_date)
                                            VALUES ("{order_id}", (SELECT SUM(item_cost) FROM 
                                            (SELECT book_order.count * book.price as item_cost, book_order.count FROM book_order
                                            INNER JOIN book ON book.isbn = book_order.isbn WHERE book_order.order_id = "{order_id}") as x), (SELECT sum(count) FROM 
                                            (SELECT book_order.count * book.price as item_cost, book_order.count FROM book_order
                                            INNER JOIN book ON book.isbn = book_order.isbn WHERE book_order.order_id = "{order_id}") as y), now());"""
        execute_and_commit_query(fill_invoice_insert_statement)
    except Exception as e:
        return str(e)
    else:
        return 0


def display_invoice(order_id: int):
    """
    returns the results of the SELECT statement for the invoice data and associated customer data for an order
    :param:
        order_id : int
            order_id of the order
    """
    return get_result(f"""SELECT invoice.*, customer.* FROM invoice 
                            INNER JOIN the_order ON invoice.order_id = the_order.order_id
                            INNER JOIN customer ON the_order.customer_id = customer.customer_id
                            WHERE invoice.order_id = {order_id};""")


if __name__ == '__main__':
    pass
    # update_inventory("854795lo6584", -10)
    # print(list_all_stock())
    # print(list_zero_stock())
    # print(display_invoice(1))
    # #generate_invoice(1)
    # #start_new_order(1)
    # #add_to_order(3, "4ce5sc5ascr45", 5)
    # print(generate_invoice(3))
    # print("Display Invoice:", display_invoice(1)[0])
    # print("Display Invoice2:", display_invoice(1)[0][4])
    # print(lookup_customer("Power"))
    # print(get_active_customers())
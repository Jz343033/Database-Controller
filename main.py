import tkinter as tk
from tkinter import ttk
import controller3 as db1
from tkinter.messagebox import showinfo

# window
root = tk.Tk()
root.title("Book Store")
root.geometry("1200x700")
root['bg'] = "lightgrey"
root.resizable(width=False, height=False)

# Main frame
customer_frame = tk.Frame(root)
customer_frame['bg'] = 'lightblue'
customer_frame.pack(expand=True, fill='both')

# --------------Customer Column------------------
# Customer Info
customer_lab = tk.Label(customer_frame, text="Customer Info", font=30, bg="lightblue")
customer_lab.grid(column=0, row=0, columnspan=3)


# All Customers last Month
def get_last_month_customers():
    """Accesses results from database and appends each result to a list. Checks for no results"""
    list1 = []
    result = db1.get_active_customers()
    print("Active Cutomers: ", result)
    if result:
        for i in result:
            list1.append(f"LName:{i[0]} Email:{i[1]} Phone:{i[2]}")
        monthly_customer_var.set(list1)
    else:
        monthly_customer_var.set("No Result")


monthly_customer_btn = ttk.Button(customer_frame, text="Active Customers Past Month", command=get_last_month_customers)
monthly_customer_btn.grid(columnspan=3, pady=(10, 0))

# Monthly Customer List box
monthly_customer_list = []
monthly_customer_var = tk.Variable(value=monthly_customer_list)
monthly_customer_box = tk.Listbox(customer_frame, height=12, width=60, listvariable=monthly_customer_var)
monthly_customer_box.grid(columnspan=3, column=0, rowspan=3)

# Get Customer ID
get_customer_id_lab = tk.Label(customer_frame, text="Get Customer ID", font=15, bg="lightblue")
get_customer_id_lab.grid(row=10, columnspan=3, column=0)

customer_info_var = tk.StringVar()
customer_info_ent = tk.Entry(customer_frame, textvariable=customer_info_var, width=50)
customer_info_ent.grid(row=11, column=0, columnspan=2)


def find_customer():
    """Accesses result from database. Checks for unknown data results"""
    id = db1.lookup_customer(customer_info_var.get())
    if id:
        customer_id_var.set(f"Customer ID: {id[0][0]}")
    else:
        customer_id_var.set("Invalid Info")


customer_info_btn = ttk.Button(customer_frame, command=find_customer, text="Find ID")
customer_info_btn.grid(column=2, row=11, sticky='w')

customer_id_var = tk.StringVar()
customer_id_lab = tk.Label(customer_frame, textvariable=customer_id_var, width=50, bg="lightblue", relief="groove")
customer_id_lab.grid(columnspan=3, column=0, row=12)

# ---------------Products Column-----------------
product_label = tk.Label(customer_frame, text="Product Info", font=30, bg="lightblue")
product_label.grid(column=3, columnspan=3, row=0)


def get_all_products():
    list1 = []
    result = db1.list_all_stock()
    print(result)
    for i in result:
        list1.append(f"ISBN:{i[0]}     Title: {i[1]}     Stock: {i[2]}")
    all_products_var.set(list1)


all_prod_btn = ttk.Button(customer_frame, command=get_all_products, text="All Products")
all_prod_btn.grid(column=3, row=1, columnspan=3, pady=(10, 0))

# All Products List Box
all_products_list = []
all_products_var = tk.Variable(value=all_products_list)
all_products_box = tk.Listbox(customer_frame, listvariable=all_products_var, height=12, width=50)
all_products_box.grid(columnspan=3, row=2, column=3, rowspan=3)

# Adding a new customer
new_cus_label = tk.Label(customer_frame, text="Add New Customer", font=30, bg="lightblue")
new_cus_label.grid(column=3, columnspan=3, row=5)

l_name_lab = tk.Label(customer_frame, text="Last Name:", bg='pink')
l_name_lab.grid(column=3, row=7, pady=(20, 0))
l_name_var = tk.StringVar()
l_name_ent = tk.Entry(customer_frame, textvariable=l_name_var)
l_name_ent.grid(column=4, row=7, pady=(20, 0))

email_lab = tk.Label(customer_frame, text="Email:", bg='pink')
email_lab.grid(column=3, row=8, pady=(20, 0))
email_var = tk.StringVar()
email_ent = tk.Entry(customer_frame, textvariable=email_var)
email_ent.grid(column=4, row=8, pady=(20, 0))

phone_lab = tk.Label(customer_frame, text="Phone:", bg='pink')
phone_lab.grid(column=3, row=9, pady=(20, 0))
phone_var = tk.StringVar()
phone_ent = tk.Entry(customer_frame, textvariable=phone_var)
phone_ent.grid(column=4, row=9, pady=(20, 0))

del_add_lab = tk.Label(customer_frame, text="Delivery Address:", bg='pink')
del_add_lab.grid(column=3, row=10, pady=(20, 0))
del_add_var = tk.StringVar()
del_add_ent = tk.Entry(customer_frame, textvariable=del_add_var)
del_add_ent.grid(column=4, row=10, pady=(20, 0))

pos_code_lab = tk.Label(customer_frame, text="Postal Code:", bg='pink')
pos_code_lab.grid(column=3, row=11, pady=(20, 0))
pos_code_var = tk.StringVar()
pos_code_ent = tk.Entry(customer_frame, textvariable=pos_code_var)
pos_code_ent.grid(column=4, row=11, pady=(20, 0))


def new_customer():
    db1.add_customer(l_name=l_name_var.get(), email=email_var.get(), phone=phone_var.get(), delivery_address=del_add_var.get(), postal_code=pos_code_var.get())
    l_name_var.set("")
    email_var.set("")
    phone_var.set("")
    del_add_var.set("")
    pos_code_var.set("")


add_customer_btn = ttk.Button(customer_frame, command=new_customer, text="Add New Customer")
add_customer_btn.grid(column=3, row=6, columnspan=3, pady=(10, 0))

# All Products List Box
all_products_list = []
all_products_var = tk.Variable(value=all_products_list)
all_products_box = tk.Listbox(customer_frame, listvariable=all_products_var, height=12, width=50)
all_products_box.grid(columnspan=3, row=2, column=3, rowspan=3)


# Zero Stock Products
zero_stock_lab = tk.Label(customer_frame, text="Zero Stock Items", font=30, bg="lightblue")
zero_stock_lab.grid(column=0, row=5, columnspan=3)


def get_zero_stock():
    """Accesses results from database and appends each result to a list. Checks for no results"""
    list1 = []
    result = db1.list_zero_stock()
    print(result)
    if result:
        for i in result:
            list1.append(f"ISBN:{i[0]}     Title: {i[1]}")
        zero_stock_var.set(list1)
    else:
        zero_stock_var.set("No Results")


# Zero Products Button
zero_stock_btn = ttk.Button(customer_frame, text="Zero Stock Items", command=get_zero_stock)
zero_stock_btn.grid(row=6, columnspan=3, column=0, pady=(10, 0))

# Zero Products List Box
zero_stock_var = tk.StringVar()
zero_stock_box = tk.Listbox(customer_frame, height=12, width=60, listvariable=zero_stock_var)
zero_stock_box.grid(columnspan=3, column=0, row=7, rowspan=3)

# --------Start Order Column------------
order_lab = tk.Label(customer_frame, text="Start Order", font=30, bg="lightblue")
order_lab.grid(column=7, row=0, sticky='w')

order_new_lab = tk.Label(customer_frame, text="Customer ID:", bg='pink')
order_new_lab.grid(column=6, row=1, pady=(20, 0))
order_new_var = tk.StringVar()
order_new_ent = tk.Entry(customer_frame, textvariable=order_new_var)
order_new_ent.grid(column=7, row=1, pady=(20, 0))


def start_order():
    """Inserts new record into the database. Finds what the new order_id is"""
    order_new_ent["state"] = "readonly"
    new_order = db1.start_new_order(customer_id=int(order_new_var.get()))
    order_id_var.set(new_order[0][0])
    order_frame_btn['state'] = "disabled"


order_frame_btn = ttk.Button(customer_frame, text="Start Order", command=start_order)
order_frame_btn.grid(row=1, pady=(20, 0), padx=(10, 0), column=8)

order_id_var = tk.IntVar()
order_id_lab = tk.Label(customer_frame, text="Order ID:")
order_id_lab.grid(column=6, row=2)
order_id_2 = tk.Label(customer_frame, textvariable=order_id_var)
order_id_2.grid(column=7, row=2)

# Order Elements
isbn_lab = tk.Label(customer_frame, text="ISBN: ", bg='lightgreen')
isbn_lab.grid(column=6, row=3)
isbn_var = tk.StringVar()
isbn_ent = tk.Entry(customer_frame, relief="groove", textvariable=isbn_var)
isbn_ent.grid(column=7, row=3)

book_count_lab = tk.Label(customer_frame, text="Amount")
book_count_lab.grid(column=6, row=4)
book_count_var = tk.IntVar()
book_count_ent = tk.Entry(customer_frame, textvariable=book_count_var, state="readonly")
book_count_ent.grid(column=7, row=4)


def add_amount():
    """Increase quantity of book wanted."""
    book_count_var.set(value=book_count_var.get() + 1)


add_count_btn = ttk.Button(customer_frame, text='+', command=add_amount)
add_count_btn.grid(column=7, row=5)


def sub_amount():
    """Decrease quantity of book wanted. Cannot be negative"""
    if book_count_var.get() > 0:
        book_count_var.set(value=book_count_var.get() - 1)


sub_count_btn = ttk.Button(customer_frame, text='-', command=sub_amount)
sub_count_btn.grid(column=6, row=5)


def add_book():
    """Try to update inventory (check if enough stock, catches value error if not). If enough add to invoice"""
    amount = -1 * book_count_var.get()
    try:
        db1.update_inventory(isbn=isbn_var.get(), change_amount=amount)
    except ValueError as ve:
        showinfo("Alert", "Not enough books in stock")
        return
    db1.add_to_order(order_id=order_id_var.get(), isbn=isbn_var.get(),
                     count=book_count_var.get())
    isbn_var.set("")
    book_count_var.set(0)


add_btn = ttk.Button(customer_frame, text="Add Book", command=add_book)
add_btn.grid(column=6, columnspan=2, row=6)


def gen_invoice():
    """Finishes order, updates, stock, active customers and zero stock automatically, displays invoice entry from database"""
    o_id = order_id_var.get()

    db1.generate_invoice(o_id)
    tup1 = db1.display_invoice(o_id)[0]
    print(tup1)
    showinfo(f"Invoice for OrderID:{o_id}",
             f"InvoiceID:{tup1[0]}\nOrderID:{tup1[1]}\nGrand Total:{tup1[2]}\nNumber Of Items:{tup1[3]}\nSale Date:{tup1[4]}\nCustomerID:{tup1[5]}\nLast Name:{tup1[6]}\nEmail:{tup1[7]}\nPhone:{tup1[8]}\nDeliveryAddress:{tup1[9]}\nPostalCode:{tup1[10]}")
    order_new_var.set('')
    order_frame_btn['state'] = "normal"
    order_new_ent['state'] = "normal"
    list1 = []
    result = db1.list_all_stock()
    for i in result:
        list1.append(f"ISBN:{i[0]}     Title: {i[1]}     Stock: {i[2]}")
    all_products_var.set(list1)
    list1 = []
    result = db1.get_active_customers()
    for i in result:
        list1.append(f"LName:{i[0]} Email:{i[1]} Phone:{i[2]}")
    monthly_customer_var.set(list1)
    list1 = []
    result = db1.list_zero_stock()
    if result:
        for i in result:
            list1.append(f"ISBN:{i[0]}     Title: {i[1]}")
        zero_stock_var.set(list1)
    else:
        zero_stock_var.set("No Results")


sub_order = ttk.Button(customer_frame, text="Submit Order", command=gen_invoice)
sub_order.grid(column=6, row=7, columnspan=2)

root.mainloop()
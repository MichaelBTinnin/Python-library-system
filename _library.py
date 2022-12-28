import sqlite3
from tkinter import *
from BooksDatabase import BooksDatabase
from CustomerDatabase import CustomerDatabase
from tkinter import messagebox
#from dateutil.parser import parse
from datetime import datetime


# Book search by isbn or title
def find_books1():
    conn = None
    try:
        conn = sqlite3.connect('__books.db')
        cur = conn.cursor()
        query = """SELECT * FROM __books """
        cur.execute(query)
        result = cur.fetchall()
        found = False
        books_list.delete(0, END)
        for i in result:
            if find_book.get() in i[0] or find_book.get() in i[1]:
                books_list.insert(END, i)
                found = True

        if not found:
            lines = ["Not", "Found"]
            messagebox.showerror("Message", "\n".join(lines))

    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()


# General book search by author last name, genre, or publisher
def find_books2():
    conn = None
    try:
        conn = sqlite3.connect('__books.db')
        cur = conn.cursor()
        query = """SELECT * FROM __books """
        cur.execute(query)
        result = cur.fetchall()
        found = False
        books_list.delete(0, END)
        for i in result:
            if find_book2.get() == i[3] or find_book2.get() == i[4] or find_book2.get() == i[5]:
                books_list.insert(END, i)
                found = True

        if not found:
            lines = ["Not", "Found"]
            messagebox.showerror("Message", "\n".join(lines))

    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        if conn:
            conn.close()


def check_out():
    if password.get() == 'abc':
        if customer_name.get() == '' or card_number.get() == '' or isbn.get() == '' or name.get() == '' or first_name.get() == '' or last_name.get() == '' or publisher.get() == '' or genre.get() == '' or description.get() == '' or checked_in.get() == '':
            lines = ["Select", "A", "Book", "", "Enter", "Card", "Number", "", "Enter", "Customer's", "Name"]
            messagebox.showerror("Message", "\n".join(lines))
            return
        else:
            if checked_in.get() == 'checked_in':
                dbCustomers.insert(card_number.get(), customer_name.get(), name.get(), isbn.get(),)
                checked_out_list.delete(0, END)
                checked_out_list.insert(END, (
                    isbn.get(), customer_name.get(), name.get(), "checked_out"))
                clear_customer_text()
                clear_text()
                populate_customer_list()
            else:
                lines = ["Book", "Already", "Checked", "Out"]
                messagebox.showerror("Message", "\n".join(lines))
                clear_customer_text()
                clear_text()

    else:
        lines = ["Librarian", "Password", "Required"]
        messagebox.showerror("Message", "\n".join(lines))


def check_in():

    #check_out_time = ('2020-1-20')#testing line
    conn = None
    if password.get() == "abc":
        try:
            conn = sqlite3.connect('___customers.db')
            cur = conn.cursor()
            query = """SELECT * FROM ___customers """
            cur.execute(query)
            result = cur.fetchall()
            found = False
            checked_out_list.delete(0, END)
            for i in result:

                if unique_id.get() in i[0]:
                    check_in_time = str(datetime.today().strftime('%Y-%m-%d'))
                    dbCustomers.update(check_in_time, unique_id.get())
                    check_in_time = parse(check_in_time)
                    check_out_time = parse(i[5])
                    comparison = int((check_in_time - check_out_time).days)
                    if comparison > 7 and checked_in.get() == "checked_out":
                        lines = ["Pay", "Late", "Fee"]
                        messagebox.showerror("Message", "\n".join(lines))
                        #print("Days since check out", comparison)#tesing code
                    if comparison <= 7 and checked_in.get() == "checked_out":
                        lines = ["Book", "Returned", "On Time"]
                        messagebox.showinfo("Message", "\n".join(lines))
                        #print("Days since check out", comparison)#testing code
                    dbCustomers._update(unique_id.get())
                    checked_out_list.insert(END, i)
                    found = True
                    break

            if not found:
                lines = ["Not", "Found"]
                messagebox.showerror("Message", "\n".join(lines))

            update_customer()

        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            if conn:
                conn.close()
    else:
        lines = ["Librarian", "Password", "Required"]
        messagebox.showerror("Message", "\n".join(lines))


def add_book():
    if password.get() == 'abc':
        if isbn.get() == '' or name.get() == '' or first_name.get() == '' or last_name.get() == '' or publisher.get() == '' or genre.get() == '' or description.get() == '' or checked_in.get() == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
            return
        dbBooks.insert(isbn.get(), name.get(), first_name.get(), last_name.get(), genre.get(), publisher.get(),
                       description.get(), checked_in.get())
        books_list.delete(0, END)
        books_list.insert(END, (
            isbn.get(), name.get(), first_name.get(), last_name.get(), publisher.get(), genre.get(), description.get(),
            checked_in.get()))
        clear_text()
        populate_list()
    else:
        lines = ["Librarian", "Password", "Required"]
        messagebox.showinfo("Message", "\n".join(lines))


def remove_book():
    if password.get() == 'abc':
        dbBooks.remove(selected_item[0])
        clear_text()
        populate_list()
    else:
        lines = ["Librarian", "Password", "Required"]
        messagebox.showinfo("Message", "\n".join(lines))


def update_book():
    if password.get() == 'abc':
        dbBooks.update(isbn.get(), name.get(), first_name.get(), last_name.get(), publisher.get(),
                       genre.get(), description.get(),
                       checked_in.get())
        clear_text()
        populate_list()
    else:
        lines = ["Librarian", "Password", "Required"]
        messagebox.showinfo("Message", "\n".join(lines))


def update_customer():
    if password.get() == 'abc':
        dbCustomers._update(unique_id.get())
        populate_customer_list()
    else:
        lines = ["Librarian", "Password", "Required"]
        messagebox.showinfo("Message", "\n".join(lines))


def populate_customer_list():
    checked_out_list.delete(0, END)
    for row in dbCustomers.fetch():
        checked_out_list.insert(END, row)


def clear_text():
    isbn_entry.delete(0, END)
    name_entry.delete(0, END)
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    genre_entry.delete(0, END)
    publisher_entry.delete(0, END)
    description_entry.delete(0, END)
    checked_in_entry.delete(0, END)


def clear_customer_text():
    card_number_entry.delete(0, END)
    unique_id_entry.delete(0, END)
    customer_name_entry.delete(0, END)


def populate_list():
    books_list.delete(0, END)
    for row in dbBooks.fetch():
        books_list.insert(END, row)


def select_item(event):
    try:
        global selected_item
        index = books_list.curselection()[0]
        selected_item = books_list.get(index)

        isbn_entry.delete(0, END)
        isbn_entry.insert(END, selected_item[0])
        name_entry.delete(0, END)
        name_entry.insert(END, selected_item[1])
        first_name_entry.delete(0, END)
        first_name_entry.insert(END, selected_item[2])
        last_name_entry.delete(0, END)
        last_name_entry.insert(END, selected_item[3])
        genre_entry.delete(0, END)
        genre_entry.insert(END, selected_item[4])
        publisher_entry.delete(0, END)
        publisher_entry.insert(END, selected_item[5])
        description_entry.delete(0, END)
        description_entry.insert(END, selected_item[6])
        checked_in_entry.delete(0, END)
        checked_in_entry.insert(END, selected_item[7])

    except IndexError:
        pass


def select_customer(event):
    try:
        global selected_customer
        index = checked_out_list.curselection()[0]
        selected_customer = checked_out_list.get(index)

        unique_id_entry.delete(0, END)
        unique_id_entry.insert(END, selected_customer[0])

    except IndexError:
        pass


dbBooks = BooksDatabase('__books.db')
dbCustomers = CustomerDatabase('___customers.db')
# Create window object
app = Tk()

# Find Book by isbn or title
find_book = StringVar()
book_label = Label(app, text='Find Book By isbn or title', font=('bold', 14), pady=20)
book_label.grid(row=0, column=0, sticky=W)
book_entry = Entry(app, textvariable=find_book)
book_entry.grid(row=0, column=1)
# General Book Search by authors last name, genre, or publisher
find_book2 = StringVar()
book2_label = Label(app, text='General Search', font=('bold', 14))
book2_label.grid(row=0, column=2, sticky=W)
book2_entry = Entry(app, textvariable=find_book2)
book2_entry.grid(row=0, column=3)

# Buttons for book searches
findBooks1_btn = Button(app, text='Find by isbn..', width=12, command=find_books1)
findBooks1_btn.grid(row=1, column=0, pady=20)
findBooks2_btn = Button(app, text='General Search', width=12, command=find_books2)
findBooks2_btn.grid(row=1, column=1, pady=20)
#Display books button
displayBooks_btn = Button(app, text='Display All Books', width=12, command=populate_list)
displayBooks_btn.grid(row=1, column=2, pady=20)

# Customer name
customer_name = StringVar()
customer_name_label = Label(app, text='Customer Name', font=('bold', 14), pady=20)
customer_name_label.grid(row=6, column=4, sticky=W)
customer_name_entry = Entry(app, textvariable=customer_name)
customer_name_entry.grid(row=6, column=5)

# Customer card number
card_number = StringVar()
card_number_label = Label(app, text='Card Number', font=('bold', 14), pady=20)
card_number_label.grid(row=11, column=0, sticky=W)
card_number_entry = Entry(app, textvariable=card_number)
card_number_entry.grid(row=11, column=1)

# Customer's book unique_id
unique_id = StringVar()
unique_id_label = Label(app, text='Transaction ID', font=('bold', 14), pady=20)
unique_id_label.grid(row=11, column=2, sticky=W)
unique_id_entry = Entry(app, textvariable=unique_id)
unique_id_entry.grid(row=11, column=3)

# Check out Check in buttons
check_out_btn = Button(app, text='Check Out', width=12, command=check_out)
check_out_btn.grid(row=11, column=4, pady=20)
check_in_btn = Button(app, text='Check In', width=12, command=check_in)
check_in_btn.grid(row=11, column=5, pady=20)

# Librarian password
password = StringVar()
password_label = Label(app, text='Librarian Password', font=('bold', 14), pady=20)
password_label.grid(row=12, column=0, sticky=W)
password_entry = Entry(app, textvariable=password)
password_entry.grid(row=12, column=1)

# Add remove edit books buttons
addBooks_btn = Button(app, text='Add Book', width=12, command=add_book)
addBooks_btn.grid(row=12, column=2, pady=20)
removeBooks_btn = Button(app, text='Remove Book', width=12, command=remove_book)
removeBooks_btn.grid(row=12, column=3, pady=20)
editBooks_btn = Button(app, text='Edit Book', width=12, command=update_book)
editBooks_btn.grid(row=12, column=4, pady=20)

# Book name for Librarian
name = StringVar()
name_label = Label(app, text='Book Title', font=('bold', 14), pady=20)
name_label.grid(row=13, column=0, sticky=W)
name_entry = Entry(app, textvariable=name)
name_entry.grid(row=13, column=1)

# Author first name
first_name = StringVar()
first_name_label = Label(app, text="Author's First Name", font=('bold', 14), pady=20)
first_name_label.grid(row=13, column=2, sticky=W)
first_name_entry = Entry(app, textvariable=first_name)
first_name_entry.grid(row=13, column=3)

# Author last name
last_name = StringVar()
last_name_label = Label(app, text="Author's Last Name", font=('bold', 14), pady=20)
last_name_label.grid(row=13, column=4, sticky=W)
last_name_entry = Entry(app, textvariable=last_name)
last_name_entry.grid(row=13, column=5)

# isbn of book
isbn = StringVar()
isbn_label = Label(app, text="ISBN", font=('bold', 14), pady=20)
isbn_label.grid(row=14, column=0, sticky=W)
isbn_entry = Entry(app, textvariable=isbn)
isbn_entry.grid(row=14, column=1)

# publisher
publisher = StringVar()
publisher_label = Label(app, text="Publisher", font=('bold', 14), pady=20)
publisher_label.grid(row=14, column=2, sticky=W)
publisher_entry = Entry(app, textvariable=publisher)
publisher_entry.grid(row=14, column=3)

# genre
genre = StringVar()
genre_label = Label(app, text="Genre", font=('bold', 14), pady=20)
genre_label.grid(row=14, column=4, sticky=W)
genre_entry = Entry(app, textvariable=genre)
genre_entry.grid(row=14, column=5)

# short description
description = StringVar()
description_label = Label(app, text="Description", font=('bold', 14), pady=20)
description_label.grid(row=15, column=0, sticky=W)
description_entry = Entry(app, textvariable=description)
description_entry.grid(row=15, column=1)

# checked_in status
checked_in = StringVar()
checked_in_label = Label(app, text="checked_in / checked_out", font=('bold', 14), pady=20)
checked_in_label.grid(row=15, column=2, sticky=W)
checked_in_entry = Entry(app, textvariable=checked_in)
checked_in_entry.grid(row=15, column=3)

# Books list
books_list = Listbox(app, height=8, width=120, border=0)
books_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# Set scrollbar to listbox
books_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=books_list.yview)
# Bind select
books_list.bind('<<ListboxSelect>>', select_item)

checked_out_list = Listbox(app, height=8, width=120, border=0)
checked_out_list.grid(row=16, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar2 = Scrollbar(app)
scrollbar2.grid(row=16, column=3)
# Set scrollbar to listbox
checked_out_list.configure(yscrollcommand=scrollbar2.set)
scrollbar2.configure(command=checked_out_list.yview)
# Bind select
checked_out_list.bind('<<ListboxSelect>>', select_customer)

# dbBooks.remove(11113)
app.title('Library Manager')
app.geometry('1200x700')

# Start program
app.mainloop()

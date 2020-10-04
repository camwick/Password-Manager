'''
Developer: Cameron Wickersham 

This program is pretty much the same as the other password manager I made
in C++ but I wanted to make a version using a GUI.
This python program utilizes tkinter and sqlite3 to make the program look nicer.

Tkinter is a module that specializes in GUIs that comes default with python.

Sqlite3 is a module that lets you build SQL databases within a lighter
load -- meaning you get enough functions to work with a SQL database but 
without all the 'beefy-ness' of a true SQL module.

I utilized Tkinter to build the main gui and display all the information 
within the program. Sqlite3 was used for data manipuation (duh).

The first program I wrote in C++ saved all the information in a file
that acted as a makeshift database. I wanted to challenge myself to learn
a little SQL and thus Sqlite3 was imported.
'''

from tkinter import *
import sqlite3
from fpdf import FPDF

# defined functions
def enter_data():
	#opening database location to add new entries
	conn = sqlite3.connect('pass.db')
	c = conn.cursor()

	# insert data entries into the database table
	c.execute("INSERT INTO database VALUES (:website, :username, :password)",
			{
				'website': website_etr.get(),
				'username': username_etr.get(),
				'password': password_etr.get(),			
			})
	conn.commit()
	conn.close()

	#clear textboxes
	website_etr.delete(0, END)
	username_etr.delete(0, END)
	password_etr.delete(0, END)

def view_data():
	# opening database location to add new entries
	conn = sqlite3.connect('pass.db')
	c = conn.cursor()

	# select database contents
	c.execute("SELECT *, oid FROM database")
		
	# list box to hold all of database
	my_listbox = Listbox(root, width=22, height=14, font='8')
	my_listbox.grid(row=0, rowspan=15, column=3, ipady=70)

	# for loop to put each tuple in the text box 
	records = c.fetchall()
	for row in records:
		my_listbox.insert(END, "Website: " + str(row[0]))
		my_listbox.insert(END, "Username: " + str(row[1]))
		my_listbox.insert(END, "Password: " + str(row[2]))
		my_listbox.insert(END, "ID#: " + str(row[3]))
		my_listbox.insert(END, '')

	conn.commit()
	conn.close()

	delete_box.delete(0, END)

	# added a little text to explain how to manipulate the list box
	directions = Label(root, font='8', text="You can scroll using the mouse \nwheel or click in the box \nand use the arrow keys")
	directions.grid(row=0, rowspan=2, column=5, columnspan=2)

	# adding capability to search for specific info by website name
	web_search = Label(root, text="Website: ", font='16')
	web_search.grid(row=3, column=5)

	global web_search_etr
	web_search_etr = Entry(root, width=30)
	web_search_etr.grid(row=3, column=6, padx=20)

	web_search_btn = Button(root, text="Search", font='16', bg='#BC64E3', command=search)
	web_search_btn.grid(row=4, column=5, columnspan=2, pady=10, padx=10, ipadx=100)

def delete_data():
	#opening database location to add new entries
	conn = sqlite3.connect('pass.db')
	c = conn.cursor()
	
	# delete an entry
	c.execute("DELETE from database WHERE oid = " + delete_box.get())

	conn.commit()
	conn.close()

	delete_box.delete(0, END)

def edit_data():
	# using new window for data editing
	global editor
	editor = Tk()
	editor.title("Change An Entry")
	editor.iconbitmap('lock.ico')
	editor.geometry('325x150')

	# opening database location to add new entries
	conn = sqlite3.connect('pass.db')
	c = conn.cursor()

	# select database contents
	entry_id = delete_box.get()
	c.execute("SELECT * FROM database WHERE oid = " + entry_id)
	records= c.fetchall()

	# creating labels and putting them on the screen
	website_lb_editor = Label(editor, text="Website:", font='16')
	website_lb_editor.grid(row=0, column=0)
	username_lb_editor = Label(editor, text="Username:", font='16')
	username_lb_editor.grid(row=1, column=0)
	password_lb_editor = Label(editor, text="Password:", font='16')
	password_lb_editor.grid(row=2, column=0)

	# creating global variables for editor names
	global website_etr_editor
	global username_etr_editor
	global password_etr_editor

	# creating entry fields and putting them on the screen
	website_etr_editor = Entry(editor, width=30)
	website_etr_editor.grid(row=0, column=1, padx=20)
	username_etr_editor = Entry(editor, width=30)
	username_etr_editor.grid(row=1, column=1, padx=20)
	password_etr_editor = Entry(editor, width=30)
	password_etr_editor.grid(row=2, column=1, padx=20)

	# puts the known entry in the entry fields
	for record in records:
		website_etr_editor.insert(0, record[0])
		username_etr_editor.insert(0, record[1])
		password_etr_editor.insert(0, record[2])

	conn.commit()
	conn.close()

	# save button
	save_btn = Button(editor, text='Save', font='16', bg='#CBFF76', command=save_data)
	save_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=90)

def save_data():

	conn = sqlite3.connect('pass.db')
	c = conn.cursor()
	
	# changing the database editor entry boxes
	record_id = delete_box.get()
	c.execute("""UPDATE database SET
			website = :website,
			username = :username,
			password = :password

			WHERE oid = :oid""",
			{
			'website': website_etr_editor.get(),
			'username': username_etr_editor.get(),
			'password': password_etr_editor.get(),
			'oid': record_id
			})

	conn.commit()
	conn.close()

	# closes the editor window after button is pressed
	editor.destroy()

def search():
	# open database 
	conn = sqlite3.connect('pass.db')
	c = conn.cursor()

	# creating the list box
	search_results = Listbox(root, height=6, font='8')
	search_results.grid(row=5, rowspan=4, column=5, columnspan=2, ipady=5)

	# selecting the correct tuple using the website entry box 
	website_search = web_search_etr.get()
	c.execute("SELECT *,oid FROM database WHERE website = ?", (website_search,))
	records = c.fetchall()

	# putting the 
	for row in records:
		search_results.insert(END, "Website: " + str(row[0]))
		search_results.insert(END, "Username: " + str(row[1]))
		search_results.insert(END, "Password: " + str(row[2]))
		search_results.insert(END, "ID#: " + str(row[3]))
		search_results.insert(END, '')

	# save changes to database and close connection
	conn.commit()
	conn.close()

	web_search_etr.delete(0, END)

def create_pdf():
	# my father wanted a to be able to export the database to a pdf, so why not

	# open database
	conn = sqlite3.connect('pass.db')
	c = conn.cursor()

	# select database contents
	c.execute("SELECT * FROM database")

	# pdf variable
	pdf = FPDF()

	# add a pdf page
	pdf.add_page()

	# setting pdf style
	pdf.set_font("Arial", size = 18)

	pdf.cell(0, 10, txt="Cam Manager Database", ln=1, align='C')

	pdf.set_font("Arial", size = 16)

	# adding the database info to the pdf
	records = c.fetchall()
	for record in records:
		pdf.cell(0, 8, txt="Website:  " + str(record[0]), ln=1, align='L')
		pdf.cell(0, 8, txt="Username: " + str(record[1]), ln=1, align='L')
		pdf.cell(0, 8, txt="Password: " + str(record[2]), ln=1, align='L')
		pdf.cell(0, 1, txt="---------------------------", ln=1, align='L')

	# save pdf and closing database
	pdf.output("pass.pdf")
	conn.commit()
	conn.close()
	
def how():
	# this function displays a window that tells the user how to use the program
	how_window = Tk()
	how_window.title("Information")
	how_window.iconbitmap('question.ico')
	how_window.geometry('950x750')

	# labels acting as the lines 
	instructions = Label(how_window, font='8', text="Submitting new entries:")
	instructions1 = Label(how_window, font='8', text="-Type the website, username, and password into their entry boxes")
	instructions2 = Label(how_window, font='8', text="-Click Enter Data button to submit the entry to the database")
	instructionstwo = Label(how_window, font='8', text="-All characters are allowed and spaces may be used")
	instructions3 = Label(how_window, font='8', text="Show Records Button:")
	instructions4 = Label(how_window, font='8', text="-Once clicked, a text box will appear on the right side that displays all database entries")
	instructions5 = Label(how_window, font='8', text="-Use the mouse wheel or arrow keys to scroll the text box")
	instructions6 = Label(how_window, font='8', text="-To search for a specific entry point, type the website name and click Search")
	instructions7 = Label(how_window, font='8', text="-Search button causes a new text box to appear with the website's saved info")
	instructions8 = Label(how_window, font='8', text="-If no info appears then the website doesn't exist or a typo occured")
	instructions9 = Label(how_window, font='8', text="-WEBSITE SEARCH IS CASE & CHARACTER SENSITIVE")
	instructions10 = Label(how_window, font='8', text="Delete Entry/Update Entry:")
	instructions11 = Label(how_window, font='8', text="-Both Delete Entry and Update Entry buttons use the Select ID entry field")
	instructions12 = Label(how_window, font='8', text="-Type the ID# of the entry you wish to delete or update")
	instructions13 = Label(how_window, font='8', text="-ID# can be found using Show Records")
	instructions14 = Label(how_window, font='8', text="-Delete Entry will delete the specified website info from the database")
	instructions15 = Label(how_window, font='8', text="-Update Entry will open a new window where the user may change the saved information and save it")
	instructions16 = Label(how_window, font='8', text="-Using the ID# as the selector forces the user to do a two step process of \nlooking up the ID# so that an entry isn't accidently deleted or changed")
	blank = Label(how_window, text=' ')
	blank1 = Label(how_window, text=' ')
	blank2 = Label(how_window, text=' ')
	info_create = Label(how_window, font='8', text="Creating a PDF of the Database:")
	info_create1 = Label(how_window, font='8', text="-Click the Create PDF button to create a pdf file of the current saved database")
	info_create2 = Label(how_window, font='8', text="-Once created, the pdf file will appear in the folder that houses the program")

	# putting stuff in the window
	instructions.grid(row=0, column=0)
	instructions1.grid(row=1, column=0)
	instructionstwo.grid(row=2, column=0)
	instructions2.grid(row=3, column=0)
	blank.grid(row=4, column=0)
	instructions3.grid(row=5, column=0)
	instructions4.grid(row=6, column=0)
	instructions5.grid(row=7, column=0)
	instructions6.grid(row=8, column=0)
	instructions7.grid(row=9, column=0)
	instructions8.grid(row=10, column=0)
	instructions9.grid(row=11, column=0)
	blank1.grid(row=12, column=0)
	info_create.grid(row=13, column=0)
	info_create1.grid(row=14, column=0)
	info_create2.grid(row=15, column=0)
	blank2.grid(row=16, column=0)
	instructions10.grid(row=17, column=0)
	instructions11.grid(row=18, column=0)
	instructions12.grid(row=19, column=0)
	instructions13.grid(row=20, column=0)
	instructions14.grid(row=21, column=0)
	instructions15.grid(row=22, column=0)
	instructions16.grid(row=23, column=0)

#=============================== main window of the program ===============================
root = Tk()
root.title("Cam Manager")
root.iconbitmap('lock.ico')
root.geometry('1000x520')

'''
This was only ran once to create the database file.
I later made this into it's own program so that when I shared this program with 
friends and family I could supply the pass.db file within the installation application.
Left it in for reference.

creating/opening the database
conn = sqlite3.connect('pass.db')
c = conn.cursor()
c.execute("""CREATE TABLE database (
		website text,
		username text,
		password text
		)""")
conn.commit()
conn.close()
'''

# creating labels and putting them on the screen
website_lb = Label(root, text="Website:", font='16')
website_lb.grid(row=0, column=0)
username_lb = Label(root, text="Username:", font='16')
username_lb.grid(row=1, column=0)
password_lb = Label(root, text="Password:", font='16')
password_lb.grid(row=2, column=0)

# creating entry fields and putting them on the screen
website_etr = Entry(root, width=30)
website_etr.grid(row=0, column=1, padx=20)
username_etr = Entry(root, width=30)
username_etr.grid(row=1, column=1, padx=20)
password_etr = Entry(root, width=30)
password_etr.grid(row=2, column=1, padx=20)

# enter data button
enter = Button(root, text='Enter Data', font='16', bg='#5ac18e', command=enter_data)
enter.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=84)

# view data button
view = Button(root, text="Show Records", font='16', bg='#5188ED', command=view_data)
view.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=70)

# delete button (shared with update button as a selection button)
delete_box = Entry(root, width=30)
delete_box.grid(row=5, column=1)

delete_box_lb = Label(root, text="Select ID:", font='16')
delete_box_lb.grid(row=5, column=0)

delete = Button(root, text="Delete Entry", font='16', bg='#FE3F10', command=delete_data)
delete.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=80)

# update button
update_btn = Button(root, text="Update Entry", font='16', bg='#ffd700', command=edit_data)
update_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=80)

# create pdf button
create_pdf_btn = Button(root, text="Create PDF", font='16', bg='#a0ff69', command=create_pdf)
create_pdf_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=80)

# How to button
howto = Button(root, text="Program Info", font='16', bg='#5EEAF3', command=how)
howto.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=80)

root.mainloop()
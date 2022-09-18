import json
import string
import tkinter as tk
from random import choice, randint, shuffle
from tkinter import messagebox
from pathlib import Path
from tkinter import ttk

FONT = ('default', 13)
FILE = 'test.json'

#---------------------------------------------PASSWORD GENERATOR----------------------------------------------------
def generator_command():
    lowercases = string.ascii_lowercase
    uppercases = string.ascii_uppercase
    numbers = string.digits
    specialchars = '~`!@#$%^&*()_-+={[}]|\:;"\'<,>.?/'
    final_password = []
    for _ in range(randint(5, 6)): final_password.append(choice(lowercases))
    for _ in range(randint(3, 5)): final_password.append(choice(uppercases))
    for _ in range(randint(2, 4)): final_password.append(choice(numbers))
    for _ in range(randint(2, 5)): final_password.append(choice(specialchars))


    shuffle(final_password)
    final_password = ''.join(final_password)


    password_entry.delete(0, tk.END)
    password_entry.insert(0, final_password)


#----------------------------------------------------SAVE-----------------------------------------------------------
def _touch_file():
    Path(FILE).touch(exist_ok=True)

def _clean_entries():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def _save_in_file(website, username, password):
    login_data = {'user': username, 'pw': password}
    with open(FILE, 'r+') as file:
        try:
            credentials = json.load(file)
            credentials[website] = login_data
            file.seek(0)
            file.truncate()
            json.dump(credentials, file)
        except:
            json.dump({website: login_data}, file)

def _warning_messagebox(website, username, password):
    if not website or not username or not password: 
        messagebox.showwarning("Blank fields", "Please, fill all the informations")
        return True

def _confirm_credentials_messagebox(website, username, password):
    message = f"These are the details entered for {website}: \nEmail/Username: {username} \nPassword: {password} \nIs it ok to save?"
    return messagebox.askokcancel('Confirm', message)

def add_command():
    website, username, password = website_entry.get(), username_entry.get(), password_entry.get()
    if _warning_messagebox(website, username, password): return
    if not _confirm_credentials_messagebox(website, username, password): return
    _clean_entries()
    _touch_file()
    _save_in_file(website, username, password)
    messagebox.showinfo('Success', 'Credentials saved successfully')
    update_combobox()

#---------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------SEARCH-----------------------------------------------------------------
def search_command():
    website = websites_combobox.get()
    with open(FILE, 'r') as file:
        credentials_data = json.load(file)
        username = credentials_data[website]['user']
        password = credentials_data[website]['pw']
        message = f'Email/Username: {username} \nPassword: {password}'
        messagebox.showinfo('Info', message)


#---------------------------------------------------------------------------------------------------------------------------------

def update_combobox():
    websites_combobox.config(values=credentials_list())

def credentials_list():
    with open(FILE, 'r') as file:
        credentials_data = json.load(file)
        return list(credentials_data.keys())



root = tk.Tk()
root.geometry('650x600')
root.resizable(0, 0)

root.grid_columnconfigure(0, pad=50)
root.grid_columnconfigure(2, pad=20)

img = tk.PhotoImage(file='logo.png')

canvas = tk.Canvas(root, width=200, height=189)
canvas.create_image(0, 0, anchor=tk.NW, image=img)
canvas.grid(row=0, column=0, columnspan=3)

#------------------------------------------LABELS----------------------------------------------
website_label = tk.Label(root, text='Website: ', font=FONT).grid(row=1, column=0)
username_label = tk.Label(root, text='Email/Username: ', font=FONT).grid(row=2, column=0)
password_label = tk.Label(root, text='Password: ', font=FONT).grid(row=3, column=0)

#------------------------------------------------------------------------------------------------

#------------------------------------------ENTRIES----------------------------------------------
website_entry = tk.Entry(root, font=FONT)
website_entry.grid(row=1, column=1, columnspan=2, sticky='nwe', pady=5)

username_entry = tk.Entry(root, font=FONT)
username_entry.grid(row=2, column=1, columnspan=2, sticky='nwe', pady=5)

password_entry = tk.Entry(root, font=FONT, width=22)
password_entry.grid(row=3, column=1, sticky='nwe', pady=5)
#------------------------------------------------------------------------------------------------

#-------------------------------------------BUTTONS----------------------------------------------
generate_password_button = tk.Button(root, text='Generate Password', command=generator_command)
generate_password_button.grid(row=3, column=2, sticky='e', pady=5)

add_button = tk.Button(root, text='Add', command=add_command)
add_button.grid(row=4, column=1, columnspan=2, sticky='nsew', pady=5)
#------------------------------------------------------------------------------------------------

websites_combobox = ttk.Combobox(root, values=credentials_list(), state='readonly')
websites_combobox.current(0)
websites_combobox.grid(row=5, column=1, sticky='w')

search_button = tk.Button(root, text='Search', command=search_command)
search_button.grid(row=5, column=2)


root.mainloop()

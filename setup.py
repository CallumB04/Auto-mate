## Imports
from tkinter import *
import json

window = Tk() ## initialises the tkinter window

def setup():
    global entry_token, entry_status, list_status ## globals the values for use in submit procedure

    ## Bot token
    label_token = Label(window, text="Bot Token:", fg="black", font=("Helvetica", 14))
    label_token.place(x=25, y=50)
    entry_token = Entry(window, bd=2, width=50)
    entry_token.place(x=130, y=55)

    ## Bot status text
    label_status = Label(window, text="Bot Status:", fg="black", font=("Helvetica", 14))
    label_status.place(x=25, y=85)
    entry_status = Entry(window, bd=2, width=50)
    entry_status.place(x=130, y=90)

    ## Bot status type (Necessary to choose one)
    list_data = ("Online", "Idle", "DND")
    list_status = Listbox(window, height=5, selectmode="single")
    for option in list_data:
        list_status.insert(END, option)
    list_status.place(x = 312, y = 120)

    ## Button for submitting inputs
    b = Button(window, text="Submit", command=submit)
    b.place(x=30, y=180)

    ## Tkinter window configuration
    window.title("Auto-mate Config!")
    window.geometry("500x300")
    window.mainloop()

def submit():

    ## Retreives values for the user input and stores them inside of a json file to then be used on bot initialisation
    ## Use of try and except block since submitting without a chose status mode raises an error (allows app to carry on until one is chosen)
    try:
        token = entry_token.get()
        status = entry_status.get()
        mode = list_status.get(list_status.curselection())
    
        with open("./data/botinfo.json", "r") as f:
            info = json.load(f)

            info["token"] = token
            info["status_text"] = status
            info["status_mode"] = mode
        
        with open("./data/botinfo.json", "w") as f:
            json.dump(info, f)

        window.destroy() ## destroys tkinter window and runs the bot.run() function in main.py

    except:
        pass
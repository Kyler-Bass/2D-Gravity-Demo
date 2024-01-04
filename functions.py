import pygame
import tkinter as tk
from tkinter import ttk

def exit_event_check():
    """Check if user clicked the (x) exit button, and what to do when they clicked it"""
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True

def test_input(window, tv1, tv2, tv3, tv4):
    grav = tv1.get()
    obj_mass = tv2.get()
    obj_ct = tv3.get()
    obj_color = tv4.get()

    try:
        if grav == "":
            grav = 0.01
        else:
            grav = float(grav)
        if obj_mass == "":
            obj_mass = 1
        else:
            obj_mass = float(obj_mass)
        if obj_ct == "":
            obj_ct = 0
        else:
            obj_ct = int(obj_ct)
        if '(' in obj_color:
            color = tuple(int(i) for i in obj_color[1:-1].split(','))
            for num in color:
                if num > 255: 
                    raise ValueError
        elif obj_color == "":
            color = "white"

        # close window and set variables 
        window.destroy()
        tv1.set(grav)
        tv2.set(obj_mass)
        tv3.set(obj_ct)
        tv4.set(color)
    except:
        # put an error message on screen and reset inputs 
        tv1.set("")
        tv2.set("")
        tv3.set("")
        tv4.set("")
        error_msg = ttk.Label(window, text="Error with input, try again", background="red")
        error_msg.grid(row=4, column=0)
        
def input_form():
    """Opens a tkinter window to get user input"""
    # window setup
    window = tk.Tk()
    window.geometry("375x110")
    window.title("Parameters Form")
    window.configure(bg="light blue")

    # input setup
    tv1 = tk.StringVar()
    prompt1 = ttk.Label(window, text="Gravity Constant (Below 0.1): ", background="light blue")
    prompt1.grid(row=0, column=0, sticky="W")
    entry1 = ttk.Entry(window, width=20, textvariable=tv1)
    entry1.grid(row=0, column=1)

    tv2 = tk.StringVar()
    prompt2 = ttk.Label(window, text="Mass of Objects (Any Positive Number): ", background="light blue")
    prompt2.grid(row=1, column=0, sticky="W")
    entry2 = ttk.Entry(window, width=20, textvariable=tv2)
    entry2.grid(row=1, column=1)

    tv3 = tk.StringVar()
    prompt3 = ttk.Label(window, text="Number of Starting Objects (Positive Integer): ", background="light blue")
    prompt3.grid(row=2, column=0, sticky="W")
    entry3 = ttk.Entry(window, width=20, textvariable=tv3)
    entry3.grid(row=2, column=1)

    tv4 = tk.StringVar()
    prompt4 = ttk.Label(window, text="Object Color (Word or (0-255,0-255,0-255)): ", background="light blue")
    prompt4.grid(row=3, column=0, sticky="W")
    entry4 = ttk.Entry(window, width=20, textvariable=tv4)
    entry4.grid(row=3, column=1)


    submit = ttk.Button(window, command= lambda: test_input(window, tv1, tv2, tv3, tv4), text="Submit")
    submit.grid(row=4, column=1)
    
    window.mainloop()

    return [tv1.get(),tv2.get(),tv3.get(),tv4.get()]
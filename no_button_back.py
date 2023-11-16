import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import json

# Global variables
checkbuttons = []
checkbutton_states = {}

def load_existing_tasks():
    tasks = load_all_tasks()
    for task in tasks:
        valitud_kuupäev = task['date']
        ülesande_tekst = task['text']
        task_id = task['id']

        # Recreate Checkbuttons for existing tasks
        check_var = tk.BooleanVar(value=checkbutton_states.get(task_id, False))
        märkeruut = tk.Checkbutton(ülesannete_kuvamine, variable=check_var,
                                   command=lambda var=check_var, id=task_id, date=valitud_kuupäev, text=ülesande_tekst:
                                   märki_ülesanne_täidetuks(var, id, date, text))
        ülesannete_kuvamine.window_create(tk.END, window=märkeruut)

        # Update Checkbuttons' states
        checkbuttons.append((märkeruut, check_var))

def ülesanne_lisamine():
    valitud_kuupäev = kalender.get_date()
    ülesande_tekst = sisestatud_tekst.get()

    # Generate a unique task_id
    task_id = int(datetime.timestamp(datetime.now()) * 1000)

    # Checkbox creation
    check_var = tk.BooleanVar()
    märkeruut = tk.Checkbutton(ülesannete_kuvamine, variable=check_var,
                               command=lambda var=check_var, id=task_id, date=valitud_kuupäev, text=ülesande_tekst:
                               märki_ülesanne_täidetuks(var, id, date, text))
    ülesannete_kuvamine.window_create(tk.END, window=märkeruut)

    # Store a reference to the Checkbutton and its associated variable
    checkbuttons.append((märkeruut, check_var))

    # Update Checkbuttons' states
    check_var.set(checkbutton_states.get(task_id, False))

    # Task addition to the text field
    ülesanne_koos_märkeruuduga = f"{valitud_kuupäev}: {ülesande_tekst}\n"
    ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)

    # Save the task to the file
    save_task({"id": task_id, "date": valitud_kuupäev, "text": ülesande_tekst})

    # Store Checkbutton state
    checkbutton_states[task_id] = check_var.get()

    # Clear the input field
    sisestatud_tekst.delete(0, tk.END)

def märki_ülesanne_täidetuks(check_var, task_id, valitud_kuupäev, ülesande_tekst):
    # Update Checkbuttons' states
    checkbutton_states[task_id] = check_var.get()

    # Cross out the corresponding task when the checkbox is checked
    ülesanne_indeks = ülesannete_kuvamine.index(tk.CURRENT)
    ülesannete_kuvamine.tag_add("tehtud", f"{ülesanne_indeks} linestart", f"{ülesanne_indeks} lineend")
    ülesannete_kuvamine.tag_configure("tehtud", overstrike=True)

    # Remove the completed task from the file
    delete_completed_tasks(task_id)

def uuenda_ülesannete_kuvamist(sündmus):
    # Clear the text field when selecting a new day
    ülesannete_kuvamine.delete(1.0, tk.END)
    valitud_kuupäev = kalender.get_date()

    # Load tasks from the file
    tasks = load_tasks(valitud_kuupäev)
    for task in tasks:
        check_var = tk.BooleanVar(value=checkbutton_states.get(task['id'], False))
        märkeruut = tk.Checkbutton(ülesannete_kuvamine, variable=check_var,
                                   command=lambda t=task, var=check_var:
                                   märki_ülesanne_täidetuks(var, t['id'], t['date'], t['text']))
        ülesannete_kuvamine.window_create(tk.END, window=märkeruut)
        ülesanne_koos_märkeruuduga = f"{task['date']}: {task['text']}\n"
        ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)

def save_task(task):
    # Save the task to the file
    with open("tasks.json", "a") as file:
        json.dump(task, file)
        file.write('\n')

def load_tasks(date):
    tasks = []
    try:
        # Load tasks from the file
        with open("tasks.json", "r") as file:
            for line in file:
                task = json.loads(line.strip())
                if task['date'] == date:
                    tasks.append(task)
    except FileNotFoundError:
        pass

    return tasks

def delete_completed_tasks(task_id):
    # Remove the completed task from the file
    tasks = load_all_tasks()
    updated_tasks = [task for task in tasks if task['id'] != task_id]

    with open("tasks.json", "w") as file:
        for task in updated_tasks:
            json.dump(task, file)
            file.write('\n')

def load_all_tasks():
    # Load all tasks from the file
    tasks = []
    try:
        with open("tasks.json", "r") as file:
            for line in file:
                task = json.loads(line.strip())
                tasks.append(task)
    except FileNotFoundError:
        pass

    return tasks

# Main window initialization
täna = datetime.today()
juur = tk.Tk()
juur.title("Kalender ülesannetega")

# Calendar creation
kalender = Calendar(juur, selectmode='day', year=täna.year, month=täna.month, day=täna.day)
kalender.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Text field for entering tasks
sisestatud_tekst = tk.Entry(juur, width=30)
sisestatud_tekst.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Button for adding a task
lisa_nupp = tk.Button(juur, text="Lisa ülesanne", command=ülesanne_lisamine)
lisa_nupp.grid(row=1, column=2, pady=5)

# Text field for displaying tasks
ülesannete_kuvamine = tk.Text(juur, height=10, width=30)
ülesannete_kuvamine.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

# Event when selecting a day in the calendar
kalender.bind("<<CalendarSelected>>", uuenda_ülesannete_kuvamist)

# Load existing tasks and recreate Checkbuttons when the application starts
load_existing_tasks()

# Start the Tkinter main loop
juur.mainloop()


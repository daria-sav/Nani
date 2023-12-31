import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

###
import json

# Define the checkbuttons list at the global level
checkbuttons = []
checkbutton_states = {}

def load_existing_tasks():
    tasks = load_all_tasks()
    for task in tasks:
        valitud_kuupäev = task['date']
        ülesande_tekst = task['text']
        task_id = task['id']

        # Recreate Checkbuttons for existing tasks
        märkeruut = tk.Checkbutton(ülesannete_kuvamine, command=lambda id=task_id, date=valitud_kuupäev, text=ülesande_tekst: märki_ülesanne_täidetuks(id, date, text))
        ülesannete_kuvamine.window_create(tk.END, window=märkeruut)

        # Update Checkbuttons' states
        if task_id in checkbutton_states:
            märkeruut.select()

        checkbuttons.append(märkeruut)
        
def ülesanne_lisamine():
    valitud_kuupäev = kalender.get_date()
    ülesande_tekst = sisestatud_tekst.get()
    
        
    # genereeri unikaalne task_id
    task_id = int(datetime.timestamp(datetime.now()) * 1000)

    # märkeruudu lisamine
    check_var = tk.BooleanVar()
    märkeruut = tk.Checkbutton(ülesannete_kuvamine, variable=check_var, command=lambda var=check_var, id=task_id, date=valitud_kuupäev, text=ülesande_tekst: märki_ülesanne_täidetuks(var, id, date, text))
    ülesannete_kuvamine.window_create(tk.END, window=märkeruut)
    
    # store a reference to the Checkbutton and its associated variable
    checkbuttons.append((märkeruut, check_var))
    
    #№№ Update Checkbuttons' states
    if task_id in checkbutton_states:
        märkeruut.select()

    # ülesanne lisamine tekstivälja
    ülesanne_koos_märkeruuduga = f"{valitud_kuupäev}: {ülesande_tekst}\n"
    ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)
    
    ### Сохранение задачи в файл
    save_task({"id": task_id, "date": valitud_kuupäev, "text": ülesande_tekst})

    # Store Checkbutton state
    checkbutton_states[task_id]  = check_var.get()

    # sisestusvälja puhastamine
    sisestatud_tekst.delete(0, tk.END)

def märki_ülesanne_täidetuks(task_id, valitud_kuupäev, ülesande_tekst, check_var):
    #№№ Update Checkbuttons' states
    checkbutton_states[task_id] = check_var.get()
    
    # see kriipsutab vastava ülesande üle, kui märkeruut on märgitud
    ülesande_indeks = ülesannete_kuvamine.index(tk.CURRENT)
    ülesannete_kuvamine.tag_add("tehtud", f"{ülesande_indeks} linestart", f"{ülesande_indeks} lineend")
    ülesannete_kuvamine.tag_configure("tehtud", overstrike=True)

    ### Удаление выполненной задачи из файла
    delete_completed_tasks(valitud_kuupäev, ülesande_tekst)

def uuenda_ülesannete_kuvamist(sündmus):
    #praegu puhastame ülesannete kuvamine välja uue päevavalimisel
    ülesannete_kuvamine.delete(1.0, tk.END)
    valitud_kuupäev = kalender.get_date()
    # siit pärast saame laadida valitud päeva ülesanded failist
    # ja kuvada need tekstiväljal
    
    ### Загрузка задач из файла
    tasks = load_tasks(valitud_kuupäev)
    
    for task in tasks:
        ülesanne_koos_märkeruuduga = f"{task['date']}: {task['text']}\n"
        ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)

def save_task(task):
    ### Сохранение задачи в файл
    with open("tasks.json", "a") as file:
        json.dump(task, file)
        file.write('\n')

def load_tasks(date):
    tasks = []
    try:
        ### Загрузка задач из файла
        with open("tasks.json", "r") as file:
            for line in file:
                task = json.loads(line.strip())
                if task['date'] == date:
                    tasks.append(task)
    except FileNotFoundError:
        pass

    return tasks

def delete_completed_tasks(task_id):
    ### Удаление выполненной задачи из файла
    tasks = load_all_tasks()
    updated_tasks = [task for task in tasks if task['id'] != task_id]

    with open("tasks.json", "w") as file:
        for task in updated_tasks:
            json.dump(task, file)
            file.write('\n')

def load_all_tasks():
    ### Загрузка всех задач из файла
    tasks = []
    try:
        with open("tasks.json", "r") as file:
            for line in file:
                task = json.loads(line.strip())
                tasks.append(task)
    except FileNotFoundError:
        pass

    return tasks

juur = tk.Tk()
juur.title("Kalender ülesannetega")

# Kalendri loomine
kalender = Calendar(juur, selectmode='day', year=2023, month=11, day=9)
kalender.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

sisestatud_tekst = tk.Entry(juur, width=30)
sisestatud_tekst.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Sisestusvälja loomine ülesande jaoks
lisa_nupp = tk.Button(juur, text="Lisa ülesanne", command=ülesanne_lisamine)
lisa_nupp.grid(row=1, column=2, pady=5)

#Nupp ülesande lisamiseks
ülesannete_kuvamine = tk.Text(juur, height=10, width=30)
ülesannete_kuvamine.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

#Nupp ülesande lisamiseks
kalender.bind("<<CalendarSelected>>", uuenda_ülesannete_kuvamist)

# Start the Tkinter main loop
juur.mainloop()

# Load existing tasks and recreate Checkbuttons when the application starts
load_existing_tasks()


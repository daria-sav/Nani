import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import json
import uuid


def ülesanne_lisamine():
    valitud_kuupäev = kalender.get_date()
    ülesande_tekst = sisestatud_tekst.get()
    task_id = str(uuid.uuid4())

    # märkeruudu lisamine

    märkeruut = tk.Checkbutton(ülesannete_kuvamine, command=lambda t_id=task_id, date=valitud_kuupäev, text=ülesande_tekst: märki_ülesanne_täidetuks(t_id, date, text))

    ülesannete_kuvamine.window_create(tk.END, window=märkeruut)

    # ülesanne lisamine tekstivälja
    ülesanne_koos_märkeruuduga = f"{valitud_kuupäev}: {ülesande_tekst}\n"
    ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)
    
    ### Сохранение задачи в файл
    ülesanne = {"id": task_id, "date": valitud_kuupäev, "text": ülesande_tekst}
    ülesanne_salvestamine(ülesanne)

    # sisestusvälja puhastamine
    sisestatud_tekst.delete(0, tk.END)

def märkeruutu_loomine(task_id, valitud_kuupäev, ülesande_tekst):
    return tk.Checkbutton(ülesannete_kuvamine, command=lambda: märki_ülesanne_täidetuks(task_id, valitud_kuupäev, ülesande_tekst))

def märki_ülesanne_täidetuks(task_id, valitud_kuupäev, ülesande_tekst):

    # see kriipsutab vastava ülesande üle, kui märkeruut on märgitud
    ülesande_indeks = ülesannete_kuvamine.index(tk.CURRENT)
    ülesannete_kuvamine.tag_add("tehtud", f"{ülesande_indeks} linestart", f"{ülesande_indeks} lineend")
    ülesannete_kuvamine.tag_configure("tehtud", overstrike=True)

    lõpetatud_ülesannete_kustutamine(task_id)


def uuenda_ülesannete_kuvamist(sündmus):
    #praegu puhastame ülesannete kuvamine välja uue päevavalimisel
    ülesannete_kuvamine.delete(1.0, tk.END)
    valitud_kuupäev = kalender.get_date()
    # siit pärast saame laadida valitud päeva ülesanded failist
    # ja kuvada need tekstiväljal
    
    ### Загрузка задач из файла
    ülesanded = ülesannete_laadimine(valitud_kuupäev)
    
    for ülesanne in ülesanded:
        märkeruut = märkeruutu_loomine(ülesanne.get('id'), ülesanne['date'], ülesanne['text'])
        ülesannete_kuvamine.window_create(tk.END, window=märkeruut)
        ülesanne_koos_märkeruuduga = f"{ülesanne['date']}: {ülesanne['text']}\n"
        ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)

        if ülesanne.get("completed", False):
            ülesanne_indeks = ülesannete_kuvamine.index(tk.END)
            ülesannete_kuvamine.tag_add("tehtud", f"{ülesanne_indeks} linestart", f"{ülesanne_indeks} lineend")
            ülesannete_kuvamine.tag_configure("tehtud", overstrike=True)



def ülesanne_salvestamine(ülesanne):
    ### Сохранение задачи в файл
    with open("tasks.json", "a") as file:
        json.dump(ülesanne, file)
        file.write('\n')

def ülesannete_laadimine(date):
    ülesanded = []
    try:
        ### Загрузка задач из файла
        with open("tasks.json", "r") as fail:
            for rida in fail:
                ülesanne = json.loads(rida.strip())
                if ülesanne['date'] == date:
                    ülesanded.append(ülesanne)
    except FileNotFoundError:
        pass

    return ülesanded

def lõpetatud_ülesannete_kustutamine(task_id):
    ### Удаление выполненной задачи из файла
    ülesanded = kõikide_ülesannete_laadimine()
    uuendatud_ülesanded = [ülesanne for ülesanne in ülesanded if ülesanne.get('id') != task_id]


    with open("tasks.json", "w") as fail:
        for ülesanne in uuendatud_ülesanded:
            json.dump(ülesanne, fail)
            fail.write('\n')

def kõikide_ülesannete_laadimine():
    ### Загрузка всех задач из файла
    ülesanded = []
    try:
        with open("tasks.json", "r") as fail:
            for rida in fail:
                ülesanne = json.loads(rida.strip())
                ülesanded.append(ülesanne)
    except FileNotFoundError:
        pass

    return ülesanded

täna = datetime.today()
juur = tk.Tk()
juur.title("Kalender ülesannetega")

# Kalendri loomine
kalender = Calendar(juur, selectmode='day', year=täna.year, month=täna.month, day=täna.day)
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
juur.mainloop()
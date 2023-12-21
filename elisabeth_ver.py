import tkinter as tk
from tkcalendar import Calendar
from tkinter import filedialog
from datetime import datetime
from tkinter import scrolledtext
from PIL import Image, ImageTk
import json
import uuid

def ülesanne_lisamine():
    valitud_kuupäev = kalender.get_date()
    ülesande_tekst = sisestatud_tekst.get()
    task_id = str(uuid.uuid4())

    # Märkeruudu loomine
    märkeruut = tk.Checkbutton(ülesannete_kuvamine, command=lambda: märki_ülesanne_täidetuks(task_id, valitud_kuupäev, ülesande_tekst))
    ülesannete_kuvamine.window_create(tk.END, window=märkeruut)

    # Lisamine uudise tekstiväljale
    ülesanne_koos_märkeruuduga = f"{valitud_kuupäev}: {ülesande_tekst}\n"
    ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)
    
    # Salvestamine ülesandefaili
    ülesanne = {"id": task_id, "date": valitud_kuupäev, "text": ülesande_tekst}
    ülesanne_salvestamine(ülesanne)

    # Sisestusvälja tühjendamine
    sisestatud_tekst.delete(0, tk.END) 

def copy_text():
    selected_text = ülesannete_kuvamine.get(tk.SEL_FIRST, tk.SEL_LAST)
    if selected_text:
        juur.clipboard_clear()
        juur.clipboard_append(selected_text)

def paste_text():
    try:
        pasted_text = juur.clipboard_get()
        sisestatud_tekst.insert(tk.END, pasted_text)
    except tk.TclError:
        pass

# Hotkeys
def on_key_press(event):
    if märkmik == juur.focus_get() and event.keysym == 'Return':
        salvesta_märkmik()
    elif event.keysym.lower() == 'c' and event.state == 0x4:  # Ctrl+C
        copy_text()
    elif event.keysym.lower() == 'v' and event.state == 0x4:  # Ctrl+V
        paste_text()
    elif event.keysym == 'Return':
        ülesanne_lisamine()

def märkmik_on_enter(event):
    märkmik.insert(tk.END, '\n')
    salvesta_märkmik() 

def märkeruutu_loomine(task_id, valitud_kuupäev, ülesande_tekst):
    return tk.Checkbutton(ülesannete_kuvamine, command=lambda: märki_ülesanne_täidetuks(task_id, valitud_kuupäev, ülesande_tekst))

def märki_ülesanne_täidetuks(task_id, valitud_kuupäev, ülesande_tekst):
    # Ülesande märkimine tehtuks, kui märkeruut on märgitud
    ülesande_indeks = ülesannete_kuvamine.index(tk.CURRENT)
    ülesannete_kuvamine.tag_add("tehtud", f"{ülesande_indeks} linestart", f"{ülesande_indeks} lineend")
    ülesannete_kuvamine.tag_configure("tehtud", overstrike=True)

    # Lõpetatud ülesande eemaldamine failist
    lõpetatud_ülesannete_kustutamine(task_id)

def uuenda_ülesannete_kuvamist(sündmus):
    # Tekstivälja tühjendamine uue kuupäeva valimisel kalendrist
    ülesannete_kuvamine.delete(1.0, tk.END)
    valitud_kuupäev = kalender.get_date()
    
    # Ülesannete laadimine failist ja nende kuvamine tekstiväljal
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
    # Salvesta ülesanne faili
    with open("tasks.json", "a") as file:
        json.dump(ülesanne, file)
        file.write('\n')

def ülesannete_laadimine(date):
    # Lae ülesanded failist
    ülesanded = []
    try:
        with open("tasks.json", "r") as fail:
            for rida in fail:
                ülesanne = json.loads(rida.strip())
                if ülesanne['date'] == date:
                    ülesanded.append(ülesanne)
    except FileNotFoundError:
        pass

    return ülesanded

def lõpetatud_ülesannete_kustutamine(task_id):
    # Eemalda lõpetatud ülesanne failist
    ülesanded = kõikide_ülesannete_laadimine()
    uuendatud_ülesanded = [ülesanne for ülesanne in ülesanded if ülesanne.get('id') != task_id]

    with open("tasks.json", "w") as fail:
        for ülesanne in uuendatud_ülesanded:
            json.dump(ülesanne, fail)
            fail.write('\n')

def kõikide_ülesannete_laadimine():
    # Lae kõik ülesanded failist
    ülesanded = []
    try:
        with open("tasks.json", "r") as fail:
            for rida in fail:
                ülesanne = json.loads(rida.strip())
                ülesanded.append(ülesanne)
    except FileNotFoundError:
        pass

    return ülesanded

def salvesta_märkmik():
    # Salvesta märkmik faili
    märkmik_text = märkmik.get("1.0", tk.END)
    with open("märkmik.txt", "w", encoding="utf-8") as file:
        file.write(märkmik_text)

def laadi_märkmik():
    # Lae märkmik failist
    try:
        with open("märkmik.txt", "r", encoding="utf-8") as file:
            märkmik_text = file.read()
            märkmik.delete(1.0, tk.END)
            märkmik.insert(tk.END, märkmik_text)
    except FileNotFoundError:
        pass

def toggle_media():
    if media_button.winfo_ismapped():
        media_button.grid_forget()
        show_selected_media()
    else:
        hide_selected_media()
        media_button.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

def show_selected_media():
    media_canvas.place(relx=0, rely=0, anchor=tk.NW)

def hide_selected_media():
    media_canvas.place_forget()

# Funktsioon pildi valimiseks
def vali_media_fail():
    # Ava failivaliku dialoog meediale
    file_path = filedialog.askopenfilename()

    # Näita valitud pilti või GIFi lõuendil
    if file_path:
        # Lae pilt
        original_image = Image.open(file_path)

        # Saada suurused
        width, height = original_image.size

        # Saada suurused, mis on saadaval pildi jaoks
        max_width = ülesannete_kuvamine.winfo_width()  # Uudise laius
        max_height = media_canvas.winfo_height()  # Kalendri uudise kõrgus

        # Arvuta uued pildi suurused
        new_width = max_width
        new_height = int(height * (max_width / width))

        # Kui uus kõrgus on suurem kui maksimaalne kõrgus, arvuta uuesti suurused
        if new_height > max_height:
            new_height = max_height
            new_width = int(width * (max_height / height))

        # Muuda pildi suurust
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

        # Puhasta lõuend enne uue pildi kuvamist
        media_canvas.delete("all")

        # Teisenda pilt PhotoImage-iks lõuendile kuvamiseks
        img_tk = ImageTk.PhotoImage(resized_image)

        # Joonista pilt lõuendile
        media_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        media_canvas.image = img_tk

# Põhiaken
täna = datetime.today()
juur = tk.Tk()
juur.title("Kalender ülesannetega")

# Kalender
kalender = Calendar(juur, selectmode='day', year=täna.year, month=täna.month, day=täna.day)
kalender.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

# Sisestusväli ülesande jaoks
sisestatud_tekst = tk.Entry(juur, width=30)
sisestatud_tekst.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

# Nupp ülesande lisamiseks
lisa_nupp = tk.Button(juur, text="Lisa ülesanne", command=ülesanne_lisamine)
lisa_nupp.grid(row=1, column=2, pady=5, sticky="nsew")

# Tekstiväli ülesannete kuvamiseks
ülesannete_kuvamine = tk.Text(juur, height=10, width=30)
ülesannete_kuvamine.grid(row=2, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

# Sündmus uue kuupäeva valimisel kalendrist
kalender.bind("<<CalendarSelected>>", uuenda_ülesannete_kuvamist)

# Bind hotkeys
juur.bind('<Return>', on_key_press)
juur.bind_all('<Control-c>', lambda e: on_key_press(e))
juur.bind_all('<Control-v>', lambda e: on_key_press(e))

märkmik = scrolledtext.ScrolledText(juur, wrap=tk.WORD, width=30, height=10)
märkmik.grid(row=0, column=3, padx=10, pady=10, rowspan=2, sticky="nsew")
märkmik.bind('<Return>', märkmik_on_enter)

laadi_märkmik()

media_canvas = tk.Canvas(juur, width=150, height=150)
media_canvas.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

media_nupp = tk.Button(juur, text="Vali media fail", command=vali_media_fail)
media_nupp.grid(row=3, column=3, pady=5, sticky="nsew")

juur.mainloop()
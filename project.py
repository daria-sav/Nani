import tkinter as tk
from tkcalendar import Calendar

def ülesanne_lisamine():
    valitud_kuupäev = kalender.get_date()
    ülesande_tekst = sisestatud_tekst.get()

    # märkeruudu lisamine
    märkeruut = tk.Checkbutton(ülesannete_kuvamine, command=lambda: märki_ülesanne_täidetuks(märkeruut))
    ülesannete_kuvamine.window_create(tk.END, window=märkeruut)

    # ülesanne lisamine tekstivälja
    ülesanne_koos_märkeruuduga = f"{valitud_kuupäev}: {ülesande_tekst}\n"
    ülesannete_kuvamine.insert(tk.END, ülesanne_koos_märkeruuduga)
    # sisestusvälja puhastamine
    sisestatud_tekst.delete(0, tk.END)

def märki_ülesanne_täidetuks(märkeruut):
    # see kriipsutab vastava ülesande üle, kui märkeruut on märgitud
    ülesande_indeks = ülesannete_kuvamine.index(tk.CURRENT)
    ülesannete_kuvamine.tag_add("tehtud", f"{ülesande_indeks} linestart", f"{ülesande_indeks} lineend")
    ülesannete_kuvamine.tag_configure("tehtud", overstrike=True)

def uuenda_ülesannete_kuvamist(sündmus):
    #praegu puhastame ülesannete kuvamine välja uue päevavalimisel
    ülesannete_kuvamine.delete(1.0, tk.END)
    valitud_kuupäev = kalender.get_date()
    # siit pärast saame laadida valitud päeva ülesanded failist
    # ja kuvada need tekstiväljal

juur = tk.Tk()
juur.title("Kalender ülesannetega")

# Kalendri loomine
kalender = Calendar(juur, selectmode='day', year=2023, month=11, day=9)
kalender.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Sisestusvälja loomine ülesande jaoks
ülesande_sisestus = tk.Entry(juur, width=30)
ülesande_sisestus.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

#Nupp ülesande lisamiseks
lisa_nupp = tk.Button(juur, text="Lisa ülesanne", command=ülesanne_lisamine)
lisa_nupp.grid(row=1, column=2, pady=5)

# Tekstiväli ülesannete kuvamiseks valitud päeval
ülesannete_kuvamine = tk.Text(juur, height=10, width=30)
ülesannete_kuvamine.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

kalender.bind("<<CalendarSelected>>", uuenda_ülesannete_kuvamist)
juur.mainloop()
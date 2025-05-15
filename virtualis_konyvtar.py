import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def config():
    ablak = Tk()
    ablak.title("Virtuális köyvtár")
    ablak_magassag = 550
    ablak_szelesseg = 900
    kepernyo_magassag = ablak.winfo_screenheight()
    kepernyo_szelesseg = ablak.winfo_screenwidth()
    x = (kepernyo_szelesseg/2)- (ablak_szelesseg/2)
    y = (kepernyo_magassag/2) - (ablak_magassag/2)
    ablak.geometry(f"{ablak_szelesseg}x{ablak_magassag}+{int(x)}+{int(y)}")
    ablak.iconbitmap("e_book.ico")
    stilus = ttk.Style()
    stilus.theme_use("vista")
    stilus.map("Treeview", background=[("selected", "blue")])
    return ablak

def get_conn():
    try:
        conn = sqlite3.connect("Virtualis_konyvtar.db")
        return conn        
    except sqlite3.Error as e:
        print(f"Adatbázis hiba: {e}")

def init_db():
    conn =  get_conn()
    curs = conn.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS konyvtar
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                iro TEXT, 
                cim TEXT,
                mufaj TEXT, 
                kiadas_eve INTEGER, 
                olvasva TEXT DEFAULT '')""")
    conn.commit()
    curs.close()
    conn.close()

ablak = config()
init_db()

conn = get_conn()
curs = conn.cursor()

def menusor():
    program_menu = Menu(ablak)
    ablak.config(menu=program_menu)
    def uj_konyv():
        uj_ablak = Toplevel(ablak)
        uj_ablak.title("Új könyv hozzáadása")
        uj_ablak_magassag = 300
        uj_ablak_szelesseg = 400
        kepernyo_magassag = uj_ablak.winfo_screenheight()
        kepernyo_szelesseg = uj_ablak.winfo_screenwidth()
        a = (kepernyo_szelesseg / 2) - (uj_ablak_szelesseg / 2)
        b = (kepernyo_magassag / 2) - (uj_ablak_magassag / 2)
        uj_ablak.geometry(f"{uj_ablak_szelesseg}x{uj_ablak_magassag}+{int(a)}+{int(b)}")
        uj_ablak.iconbitmap("e_book.ico")

        values = ["Író", "Cím", "Műfaj", "Kiadás éve"]
        for value in enumerate(values):
            cimke = Label(uj_ablak, text=value[1], font="algerian 15")
            cimke.grid(row=value[0], column=0, pady=10, padx=10, columnspan=2)
            bevitel = Entry(uj_ablak)
            bevitel.grid(row=value[0], column=2, pady=10, padx=10, columnspan=2, ipadx=40)

        iro_bevitel = Entry(uj_ablak)
        iro_bevitel.grid(row=0, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        cim_bevitel = Entry(uj_ablak)
        cim_bevitel.grid(row=1, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        mufaj_bevitel = Entry(uj_ablak)
        mufaj_bevitel.grid(row=2, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        kiadas_eve_bevitel = Entry(uj_ablak)
        kiadas_eve_bevitel.grid(row=3, column=2, pady=10, padx=10, columnspan=2, ipadx=40)

        def mezo_torles():
            iro_bevitel.delete(0,END)
            cim_bevitel.delete(0, END)
            mufaj_bevitel.delete(0, END)
            kiadas_eve_bevitel.delete(0, END)

        # új ablak gombok függvényei
        def ok():
            iro, cim, mufaj, kiadas_eve = iro_bevitel.get(), cim_bevitel.get(), mufaj_bevitel.get(), kiadas_eve_bevitel.get()
            if not iro or not cim or not mufaj or not kiadas_eve:
                felugro_ablak = messagebox.showwarning("Figyelem!", "Minden mező kitöltése kötelező!")
                Label(uj_ablak, text=felugro_ablak).grid(row=1, column=1, sticky=N+E+W+S)
                uj_konyv()
                mezo_torles()
                return
            try:
                ev = int(kiadas_eve)
            except Exception as e:
                felugro_ablak = messagebox.showerror("Hiba!", "Az évszám csak szám lehet!")
                Label(uj_ablak, text=felugro_ablak).grid(row=1, column=1, sticky=N + E + W + S)
                uj_konyv()
                mezo_torles()
                return
            curs.execute("""INSERT INTO konyvtar (iro, cim, mufaj, kiadas_eve) VALUES (?, ?, ?, ?)""", (iro, cim, mufaj, kiadas_eve))
            conn.commit()
            mezo_torles()
            frissites()

        def megsem():
            frissites()
            uj_ablak.destroy()

        bevitel_gomb = Button(uj_ablak, text="ok", font="algerian 15", command=ok)
        bevitel_gomb.grid(row=4, column=1, columnspan=2, padx=20, pady=30)
        megsem_gomb = Button(uj_ablak, text="Mégsem", font="algerian 15", command=megsem)
        megsem_gomb.grid(row=4, column=2, columnspan=2, padx=20)

    def torles():
        kijelolt_elemek = treeview_tablazat.selection()
        if not kijelolt_elemek:
            messagebox.showwarning("Figyelem!", "Nincs kijelölve egy könyv sem!")
            return

        felugro_ablak = messagebox.askyesno("Könyv törlése", "Biztosan törölni akarod a könyvet?")
        if felugro_ablak == 1:
            for kijelolt in kijelolt_elemek:
                curs.execute("DELETE FROM konyvtar WHERE id=?", (int(kijelolt),))
                conn.commit()
                treeview_tablazat.delete(kijelolt)

    fajl_menu = Menu(program_menu, tearoff=False)
    program_menu.add_cascade(label="Fájl", menu=fajl_menu)
    fajl_menu.add_command(label="Új", command=uj_konyv)
    fajl_menu.add_command(label="Törlés", command=torles)
    fajl_menu.add_separator()
    fajl_menu.add_command(label="Kilépés", command=ablak.quit)

def indulas():
    global indulo_kep, indulo_kep_cimke
    indulo_kep = PhotoImage(file="virtualiskonyvtar.png")
    indulo_kep_cimke = Label(ablak,image=indulo_kep)
    indulo_kep_cimke.pack()
    ablak.after(1000, trw_tablazat)

def trw_tablazat():
    global kereses_bevitel
    global legordulo_menu
    indulo_kep_cimke.destroy()
    menusor()
    kereses_keret = Frame(ablak)
    kereses_keret.pack(ipady=10)

    kereses_cimke = Label(kereses_keret, text="Keresés: ", font="algerian 15")
    kereses_cimke.grid(row=0, column=0, padx=10)
    kereses_bevitel = Entry(kereses_keret)
    kereses_bevitel.grid(row=0, column=1, padx=10)

    fejlecek = {
    "Válaszd ki az oszlopot":" ",
    "Író": "iro",
    "Cím": "cim",
    "Műfaj": "mufaj",
    "Kiadás éve": "kiadas_eve",
    "Olvasva": "olvasva"
}
    legordulo_menu = ttk.Combobox(kereses_keret, values=list(fejlecek.keys()), state="readonly")
    legordulo_menu.current(0)
    legordulo_menu.bind("<<ComboboxSelected>>")
    legordulo_menu.grid(row=0, column=2, padx=10)

    def kereses():
        oszlop = fejlecek[legordulo_menu.get()]  # oszlopnév lekérése
        ertek = kereses_bevitel.get().strip().lower()
        if not ertek or legordulo_menu.get() == list(fejlecek.keys())[0]:
            messagebox.showwarning("Figyelem!", "Minden mező kitöltése kötelező!")
        else:
            treeview_tablazat.delete(*treeview_tablazat.get_children())
            curs.execute(f"SELECT * FROM konyvtar WHERE LOWER({oszlop}) LIKE ?", (f"%{ertek}%",))
            adatok = curs.fetchall()

            treeview_tablazat.tag_configure("paratlansor", background="white")
            treeview_tablazat.tag_configure("parossor", background="lightblue")
            n = 0
            for adat in adatok:
                if n % 2 == 0:
                    treeview_tablazat.insert("", "end", iid=adat[0],values=(adat[1], adat[2], adat[3], adat[4], adat[5]), tags=("parossor",))
                else:
                    treeview_tablazat.insert("", "end", iid=adat[0],values=(adat[1], adat[2], adat[3], adat[4], adat[5]),tags=("paratlansor",))
                n += 1
        kereses_bevitel.delete(0,END)
        legordulo_menu.current(0)

    kereses_gomb = Button(kereses_keret, text="Keresés", font="algerian 15", command=kereses)
    kereses_gomb.grid(row=0, column=3, padx=10)

    alaphelyzet_gomb = Button(kereses_keret, text="Alaphelyzetbe állítás", font="algerian 15", command=frissites)
    alaphelyzet_gomb.grid(row=0, column=4, padx=10)

    treeview_keret = Frame(ablak)
    treeview_keret.pack()

    gorgetosav = Scrollbar(treeview_keret)
    gorgetosav.pack(side=RIGHT, fill=Y)

    global treeview_tablazat
    treeview_tablazat = ttk.Treeview(treeview_keret, columns=("c1", "c2", "c3", "c4", "c5"), show="headings", yscrollcommand=gorgetosav)
    values = ["# 1", "# 2", "# 3", "# 4", "# 5"]
    texts = ["Író", "Cím", "Műfaj", "Kiadás éve", "Olvasva"]
    for i in range(len(values)):
        treeview_tablazat.column(values[i], anchor=CENTER, stretch=NO, width=250)
        treeview_tablazat.heading(values[i], text=texts[i])
    treeview_tablazat.pack(ipady=120)

    def olvasva(event):
        oszlop = treeview_tablazat.identify_column(event.x)  # például: '#5'
        sor = treeview_tablazat.identify_row(event.y)
        olvasott = '✔'
        nem_olvasott = ' '
        if not oszlop and sor:
            return
        aktualis_allapot = treeview_tablazat.set(sor, "c5")
        if oszlop == "#5" and sor:
            if aktualis_allapot != olvasott:
                treeview_tablazat.set(sor, "c5", olvasott)
                curs.execute("UPDATE konyvtar SET olvasva = ? WHERE id = ?", (olvasott, sor))
                conn.commit()
            else:
                treeview_tablazat.set(sor, "c5", nem_olvasott)
                curs.execute("UPDATE konyvtar SET olvasva = ? WHERE id = ?", (nem_olvasott, sor))
                conn.commit()

    # oszloprendezés funkció
    def rendezes(treeview_tablazat, oszlop, visszafele):
        adatok = [(treeview_tablazat.set(k, oszlop), k) for k in treeview_tablazat.get_children("")]
        adatok.sort(reverse=visszafele)
        for index, (val, k) in enumerate(adatok):
            treeview_tablazat.move(k, '', index)
        treeview_tablazat.heading(oszlop, command=lambda: rendezes(treeview_tablazat, oszlop, not visszafele))

    values = [("Író", "c1", False),
            ("Cím", "c2", False),
            ("Műfaj", "c3", False),
            ("Kiadás éve", "c4", False),
            ("Olvasva", "c5", False)]
    
    for value in values:
        treeview_tablazat.heading(value[1], text=value[0], command=lambda: rendezes(treeview_tablazat, value[1], value[2])) 

    frissites()

    gorgetosav.configure(command=treeview_tablazat.yview())

    treeview_tablazat.bind("<Button-1>", olvasva)
    treeview_tablazat.bind("<Double-Button-1>", feluliras)

def frissites():
    kereses_bevitel.delete(0,END)
    legordulo_menu.current(0)
    curs.execute("SELECT * FROM konyvtar")
    adatok = curs.fetchall()
    treeview_tablazat.delete(*treeview_tablazat.get_children())
    treeview_tablazat.tag_configure("paratlansor", background="white")
    treeview_tablazat.tag_configure("parossor", background="lightblue")
    for n, adat in enumerate(adatok):
        if n %2 == 0:
            treeview_tablazat.insert("", "end", iid=adat[0], values=(adat[1], adat[2], adat[3], adat[4]), tags=("parossor",))
        else:
            treeview_tablazat.insert("", "end", iid=adat[0], values=(adat[1], adat[2], adat[3], adat[4]), tags=("paratlansor",))

def feluliras(event):
    feluliras_ablak = Toplevel()
    feluliras_ablak.title("Módosítás")
    feluliras_ablak_magassag = 300
    feluliras_ablak_szelesseg = 400
    kepernyo_magassag = feluliras_ablak.winfo_screenheight()
    kepernyo_szelesseg = feluliras_ablak.winfo_screenwidth()
    a = (kepernyo_szelesseg / 2) - (feluliras_ablak_szelesseg / 2)
    b = (kepernyo_magassag / 2) - (feluliras_ablak_magassag / 2)
    feluliras_ablak.geometry(f"{feluliras_ablak_szelesseg}x{feluliras_ablak_magassag}+{int(a)}+{int(b)}")
    feluliras_ablak.iconbitmap("e_book.ico")

    kijelolt_sor = treeview_tablazat.selection()[0]
    sor_elemek = treeview_tablazat.item(kijelolt_sor, "values")

    values = ["Író", "Cím", "Műfaj", "Kiadás éve"]
    for value in enumerate(values):
        cimke = Label(feluliras_ablak, text=value[1], font="algerian 15")
        cimke.grid(row=value[0], column=0, pady=10, padx=10, columnspan=2)

    bevitels = []
    for idx, value in enumerate(values):
        bevitel = Entry(feluliras_ablak)
        bevitel.insert(0, sor_elemek[idx])
        bevitel.grid(row=idx, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        bevitels.append(bevitel)
    def felulir():
        iro, cim, mufaj, kiadas_eve = bevitels[0].get(), bevitels[1].get(), bevitels[2].get(), bevitels[3].get()
        if cim and iro and mufaj and kiadas_eve:
            try:
                ev = int(kiadas_eve)
                curs.execute("UPDATE konyvtar SET iro=?, cim=?, mufaj=?, kiadas_eve=? WHERE id=?",
                            (iro, cim, mufaj, kiadas_eve, kijelolt_sor))
                conn.commit()
                frissites()
                messagebox.showinfo("", "A felülírás sikerült")
            except Exception as e:
                messagebox.showerror("", "A felülírás sikertelen!")

    felulir_gomb = Button(feluliras_ablak, text="Felülírás", font="algerian 15", command=felulir)
    felulir_gomb.grid(row=5, column=1, pady=10, padx=10)

    megsem_gomb = Button(feluliras_ablak, text="Mégsem", font="algerian 15", command=feluliras_ablak.destroy)
    megsem_gomb.grid(row=5, column=3, pady=10, sticky=E)

if __name__ == "__main__":
    indulas()
    ablak.mainloop()
    conn.close()
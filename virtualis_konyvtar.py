import time
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import messagebox

ablak = Tk()
ablak.title("Virtuális köyvtár")
# a program szélességének és magasságának meghatározása
ablak_magassag = 550
ablak_szelesseg = 900
# a képernyő geometriájának meghatározása
kepernyo_magassag = ablak.winfo_screenheight()
kepernyo_szelesseg = ablak.winfo_screenwidth()
# az program bal felső sarkának meghatározása
x = (kepernyo_szelesseg/2)- (ablak_szelesseg/2)
y = (kepernyo_magassag/2) - (ablak_magassag/2)
# a program geometriájának meghatározása
ablak.geometry(f"{ablak_szelesseg}x{ablak_magassag}+{int(x)}+{int(y)}")
ablak.iconbitmap("e_book.ico")

#témák és stílusok hozzáadása
stilus = ttk.Style()
stilus.theme_use("vista")
stilus.map("Treeview", background=[("selected", "blue")])

# SQLite adatbázis létrehozása
conn = sqlite3.connect("Virtualis_konyvtar.db")
curs = conn.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS konyvtar (id INTEGER PRIMARY KEY AUTOINCREMENT, iro TEXT, cim TEXT, mufaj TEXT, kiadas_eve INTEGER, olvasva TEXT DEFAULT '')")

def menusor():
    #menüsor létrehozása
    program_menu = Menu(ablak)
    ablak.config(menu=program_menu)
    # ÚJ menü parancs létrehozása
    def uj_konyv():
        uj_ablak = Toplevel(ablak)
        uj_ablak.title("Új könyv hozzáadása")
        # az új könyv ablak szélességének és magasságának meghatározása
        uj_ablak_magassag = 300
        uj_ablak_szelesseg = 400
        # a képernyő geometriájának meghatározása
        kepernyo_magassag = uj_ablak.winfo_screenheight()
        kepernyo_szelesseg = uj_ablak.winfo_screenwidth()
        # az új könyv ablak bal felső sarkának meghatározása
        a = (kepernyo_szelesseg / 2) - (uj_ablak_szelesseg / 2)
        b = (kepernyo_magassag / 2) - (uj_ablak_magassag / 2)
        # az új könyv ablak geometriájának meghatározása
        uj_ablak.geometry(f"{uj_ablak_szelesseg}x{uj_ablak_magassag}+{int(a)}+{int(b)}")
        uj_ablak.iconbitmap("e_book.ico")

        # új könyv ablak beviteli mezők létrehozása
        iro_bevitel_cimke = Label(uj_ablak, text="Író: ", font="algerian 15")
        iro_bevitel_cimke.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
        cim_bevitel_cimke = Label(uj_ablak, text="Cím: ", font="algerian 15")
        cim_bevitel_cimke.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
        mufaj_bevitel_cimke = Label(uj_ablak, text="Műfaj: ", font="algerian 15")
        mufaj_bevitel_cimke.grid(row=2, column=0, pady=10, padx=10,  columnspan=2)
        kiadas_eve_bevitel_cimke = Label(uj_ablak, text="Kiadás éve: ", font="algerian 15")
        kiadas_eve_bevitel_cimke.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

        # új könyv ablak beviteli mezők létrehozása
        iro_bevitel = Entry(uj_ablak)
        iro_bevitel.grid(row=0, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        cim_bevitel = Entry(uj_ablak)
        cim_bevitel.grid(row=1, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        mufaj_bevitel = Entry(uj_ablak)
        mufaj_bevitel.grid(row=2, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
        kiadas_eve_bevitel = Entry(uj_ablak)
        kiadas_eve_bevitel.grid(row=3, column=2, pady=10, padx=10, columnspan=2, ipadx=40)


        #beviteli mezők törlése
        def mezo_torles():
            iro_bevitel.delete(0,END)
            cim_bevitel.delete(0, END)
            mufaj_bevitel.delete(0, END)
            kiadas_eve_bevitel.delete(0, END)

        # új ablak gombok függvényei
        def ok():
            # beviteli mezők kitöltöttségének ellenőrzése
            if not iro_bevitel.get() or not cim_bevitel.get() or not mufaj_bevitel.get() or not kiadas_eve_bevitel.get():
                felugro_ablak = messagebox.showwarning("Figyelem!", "Minden mező kitöltése kötelező!")
                Label(uj_ablak, text=felugro_ablak).grid(row=1, column=1, sticky=N+E+W+S)
                uj_konyv()
                mezo_torles()
            # a kiadás éve csak szám lehet, ezt itt ellenőrzzük
            try:
                ev = int(kiadas_eve_bevitel.get())
            except:
                felugro_ablak = messagebox.showerror("Hiba!", "Az évszám csak szám lehet!")
                Label(uj_ablak, text=felugro_ablak).grid(row=1, column=1, sticky=N + E + W + S)
                uj_konyv()
                mezo_torles()
            curs.execute("INSERT INTO konyvtar (iro, cim, mufaj, kiadas_eve) VALUES (?, ?, ?, ?)", (iro_bevitel.get(), cim_bevitel.get(), mufaj_bevitel.get(), kiadas_eve_bevitel.get()))
            conn.commit()
            mezo_torles()
            frissites()

        def megsem():
            frissites()
            uj_ablak.destroy()

        # új könyv ablak gombok létrehozása
        bevitel_gomb = Button(uj_ablak, text="ok", font="algerian 15", command=ok)
        bevitel_gomb.grid(row=4, column=1, columnspan=2, padx=20, pady=30)
        megsem_gomb = Button(uj_ablak, text="Mégsem", font="algerian 15", command=megsem)
        megsem_gomb.grid(row=4, column=2, columnspan=2, padx=20)

    def torles():
        # a kijelölt elem meghatározása
        kijelolt_elemek = treeview_tablazat.selection()
        if not kijelolt_elemek:
            messagebox.showwarning("Figyelem!", "Nincs kijelölve egy könyv sem!")
            return

        # felugró ablak a törlés megerősítésére
        felugro_ablak = messagebox.askyesno("Könyv törlése", "Biztosan törölni akarod a könyvet?")
        #ha igen a válasz
        if felugro_ablak == 1:
            for kijelolt in kijelolt_elemek:
                curs.execute("DELETE FROM konyvtar WHERE id=?", (int(kijelolt),))
                conn.commit()
                treeview_tablazat.delete(kijelolt)


    # fájl menü létrehozása
    fajl_menu = Menu(program_menu, tearoff=False)
    program_menu.add_cascade(label="Fájl", menu=fajl_menu)
    fajl_menu.add_command(label="Új", command=uj_konyv)
    fajl_menu.add_command(label="Törlés", command=torles)
    fajl_menu.add_separator()
    fajl_menu.add_command(label="Kilépés", command=ablak.quit)


def indulas():
    global indulo_kep, indulo_kep_cimke
    # betöltő kép létrehozása
    indulo_kep = PhotoImage(file="virtualiskonyvtar.png")
    indulo_kep_cimke = Label(ablak,image=indulo_kep)
    indulo_kep_cimke.pack()
    # késleltetési idő beállítása
    ablak.after(1000, trw_tablazat)


def trw_tablazat():
    global kereses_bevitel
    global legordulo_menu
    indulo_kep_cimke.destroy()
    menusor()
    # kereses keret létrehozása
    kereses_keret = Frame(ablak)
    kereses_keret.pack(ipady=10)

    #keresés címke llétrehozása
    kereses_cimke = Label(kereses_keret, text="Keresés: ", font="algerian 15")
    kereses_cimke.grid(row=0, column=0, padx=10)
    #keresés beviteli mező létrehozása
    kereses_bevitel = Entry(kereses_keret)
    kereses_bevitel.grid(row=0, column=1, padx=10)

    # keresés legördülő menü létrehozása
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

    #keresés gombhoz tartozó funkció létrehozása
    def kereses():
        oszlop = fejlecek[legordulo_menu.get()]  # oszlopnév lekérése
        ertek = kereses_bevitel.get()
        # a beviteli mező és a legördülő menü helyes kitöltésének ellenőrzése
        if not kereses_bevitel.get() or legordulo_menu.get() == list(fejlecek.keys())[0]:
            messagebox.showwarning("Figyelem!", "Minden mező kitöltése kötelező!")
        else:
            # treeview táblázat törlése és feltöltése a keresési eredménnyel
            treeview_tablazat.delete(*treeview_tablazat.get_children())
            curs.execute(f"SELECT * FROM konyvtar WHERE {oszlop} LIKE ?", (f"%{ertek}%",))
            adatok = curs.fetchall()

            # sorcímkék létrehozása a vizuális tagoláshoz
            treeview_tablazat.tag_configure("paratlansor", background="white")
            treeview_tablazat.tag_configure("parossor", background="lightblue")
            # "n" változó létrehozása, amivel a sorok színezését határozzuk meg
            n = 0
            # a treeview táblázat feltöltése a a keresési találatokkal
            for adat in adatok:
                # ha "n" válzotó oszthat kettővel, a "parossor"-ban megadott színű legyen a sor
                if n % 2 == 0:
                    treeview_tablazat.insert("", "end", iid=adat[0],values=(adat[1], adat[2], adat[3], adat[4], adat[5]), tags=("parossor",))
                else:
                    treeview_tablazat.insert("", "end", iid=adat[0],values=(adat[1], adat[2], adat[3], adat[4], adat[5]),tags=("paratlansor",))
                n += 1
        kereses_bevitel.delete(0,END)
        legordulo_menu.current(0)

    # keresés gomb létrehozása
    kereses_gomb = Button(kereses_keret, text="Keresés", font="algerian 15", command=kereses)
    kereses_gomb.grid(row=0, column=3, padx=10)

    # a treeview táblázat alaphelyzetbe állítása
    alaphelyzet_gomb = Button(kereses_keret, text="Alaphelyzetbe állítás", font="algerian 15", command=frissites)
    alaphelyzet_gomb.grid(row=0, column=4, padx=10)

    # treeview keret létrehozása
    treeview_keret = Frame(ablak)
    treeview_keret.pack()

    #görgetősáv létrehozása
    gorgetosav = Scrollbar(treeview_keret)
    gorgetosav.pack(side=RIGHT, fill=Y)
    #treeview táblázat formázása

    # treeview táblázat létrehozása
    global treeview_tablazat
    treeview_tablazat = ttk.Treeview(treeview_keret, columns=("c1", "c2", "c3", "c4", "c5"), show="headings", yscrollcommand=gorgetosav)
    treeview_tablazat.column("# 1", anchor=CENTER, stretch=NO, width=200)
    treeview_tablazat.heading("# 1", text="Író")
    treeview_tablazat.column("# 2", anchor=CENTER, stretch=NO, width=200)
    treeview_tablazat.heading("# 2", text="Cím")
    treeview_tablazat.column("# 3", anchor=CENTER, stretch=NO, width=250)
    treeview_tablazat.heading("# 3", text="Műfaj")
    treeview_tablazat.column("# 4", anchor=CENTER, stretch=NO, width=100)
    treeview_tablazat.heading("# 4", text="Kiadás éve")
    treeview_tablazat.column("# 5", anchor=CENTER, stretch=NO, width=100)
    treeview_tablazat.heading("# 5", text="Olvasva")
    treeview_tablazat.pack(ipady=120)

    # olvasva checkbox függvény létrehozása
    def olvasva(event):
        #kijelölt sor és oszlop meghatáározása
        oszlop = treeview_tablazat.identify_column(event.x)  # például: '#5'
        sor = treeview_tablazat.identify_row(event.y)
        # az olvasott és nem olvasott értékek változókhoz rendelése
        olvasott = '✔'
        nem_olvasott = ' '
        #kijelölés ellenőrzése, ha nincs nem folytatódik a prgramsor
        if not oszlop and sor:
            return
        aktualis_allapot = treeview_tablazat.set(sor, "c5")
        # a sor és az olvasott (#5) oszlop kijelöltségének llenőrzése
        if oszlop == "#5" and sor:
            # a kijeölt sor ellenőrzése olvasott vagy sem
            if aktualis_allapot != olvasott:
                # a treeview táblázat olvasott oszlopának átírása "olvasott"-ra (pipa)
                treeview_tablazat.set(sor, "c5", olvasott)
                # az SQL táblázat olvasott oszlopának átírása "olvasott"-ra (pipa)
                curs.execute("UPDATE konyvtar SET olvasva = ? WHERE id = ?", (olvasott, sor))
                conn.commit()
            else:
                # a treeview táblázat olvasott oszlopának átírása "nem olvasott"-ra (nincs pipa)
                treeview_tablazat.set(sor, "c5", nem_olvasott)
                # az SQL táblázat frissítése "nem olvasott"-ra (nincs pipa)
                curs.execute("UPDATE konyvtar SET olvasva = ? WHERE id = ?", (nem_olvasott, sor))
                conn.commit()

    # oszloprendezés funkció
    def rendezes(treeview_tablazat, oszlop, visszafele):
        # oszlopadatok lekérdezése
        adatok = [(treeview_tablazat.set(k, oszlop), k) for k in treeview_tablazat.get_children("")]
        # A lista rendezése történik meg: ha visszafele=True, csökkenő sorrendben, egyébként növekvően
        adatok.sort(reverse=visszafele)
        # Az új sorrend alapján mozgatjuk a sorokat a Treeview-ban
        for index, (val, k) in enumerate(adatok):
            treeview_tablazat.move(k, '', index)
        # Beállítjuk újra a fejléc kattintás eseményt, hogy a következő kattintás megfordítsa a rendezést
        treeview_tablazat.heading(oszlop, command=lambda: rendezes(treeview_tablazat, oszlop, not visszafele))

    # Fejlécek elnevezése és kattintás esemény hozzárendelése
    treeview_tablazat.heading("c1", text="Író", command=lambda:rendezes(treeview_tablazat, "c1", False))
    treeview_tablazat.heading("c2", text="Cím", command=lambda: rendezes(treeview_tablazat, "c2", False))
    treeview_tablazat.heading("c3", text="Műfaj", command=lambda: rendezes(treeview_tablazat, "c3", False))
    treeview_tablazat.heading("c4", text="Kiadás éve", command=lambda: rendezes(treeview_tablazat, "c4", False))
    treeview_tablazat.heading("c5", text="Olvasva", command=lambda: rendezes(treeview_tablazat, "c5", False))

    frissites()

    #görgetősáv konfigurálása
    gorgetosav.configure(command=treeview_tablazat.yview())

    # egérkattintás beállítása
    treeview_tablazat.bind("<Button-1>", olvasva)
    treeview_tablazat.bind("<Double-Button-1>", feluliras)

#a treeview táblázat automatikus frissítése
def frissites():
    #a keresési beviteli mező és a legördülő menü alaphelyzetbe állítása, ha nem abban van
    if kereses_bevitel and legordulo_menu:
        kereses_bevitel.delete(0,END)
        legordulo_menu.current(0)
    # az SQL adatbázis tartalmának lekérése
    curs.execute("SELECT * FROM konyvtar")
    adatok = curs.fetchall()
    # a treeview táblázat törlése
    treeview_tablazat.delete(*treeview_tablazat.get_children())
    #sorcímkék létrehozása a vizuális tagoláshoz
    treeview_tablazat.tag_configure("paratlansor", background="white")
    treeview_tablazat.tag_configure("parossor", background="lightblue")
    # "n" változó létrehozása, amivel a sorok színezését határozzuk meg
    n = 0
    # a treeview táblázat feltöltése a legfrissebb adatokkal
    for adat in adatok:
        # ha "n" válzotó oszthat kettővel, a "parossor"-ban megadott színű legyen a sor
        if n %2 == 0:
            treeview_tablazat.insert("", "end", iid=adat[0], values=(adat[1], adat[2], adat[3], adat[4], adat[5]), tags=("parossor",))
        else:
            treeview_tablazat.insert("", "end", iid=adat[0], values=(adat[1], adat[2], adat[3], adat[4], adat[5]), tags=("paratlansor",))
        n +=1

# táblázat sorainak felülírása
def feluliras(evet):
    feluliras_ablak = Toplevel()
    feluliras_ablak.title("Módosítás")
    feluliras_ablak_magassag = 300
    feluliras_ablak_szelesseg = 400
    # a képernyő geometriájának meghatározása
    kepernyo_magassag = feluliras_ablak.winfo_screenheight()
    kepernyo_szelesseg = feluliras_ablak.winfo_screenwidth()
    # az új könyv ablak bal felső sarkának meghatározása
    a = (kepernyo_szelesseg / 2) - (feluliras_ablak_szelesseg / 2)
    b = (kepernyo_magassag / 2) - (feluliras_ablak_magassag / 2)
    # az új könyv ablak geometriájának meghatározása
    feluliras_ablak.geometry(f"{feluliras_ablak_szelesseg}x{feluliras_ablak_magassag}+{int(a)}+{int(b)}")
    feluliras_ablak.iconbitmap("e_book.ico")

    # a kijelölt sor és a sor elemeinek meghatározása
    kijelolt_sor = treeview_tablazat.selection()[0]
    sor_elemek = treeview_tablazat.item(kijelolt_sor, "values")

    # felülírás ablak címkék létrehozása
    iro_bevitel_cimke = Label(feluliras_ablak, text="Író: ", font="algerian 15")
    iro_bevitel_cimke.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
    cim_bevitel_cimke = Label(feluliras_ablak, text="Cím: ", font="algerian 15")
    cim_bevitel_cimke.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
    mufaj_bevitel_cimke = Label(feluliras_ablak, text="Műfaj: ", font="algerian 15")
    mufaj_bevitel_cimke.grid(row=2, column=0, pady=10, padx=10, columnspan=2)
    kiadas_eve_bevitel_cimke = Label(feluliras_ablak, text="Kiadás éve: ", font="algerian 15")
    kiadas_eve_bevitel_cimke.grid(row=3, column=0, pady=10, padx=10, columnspan=2)

    #beviteli mezők létrehozása az alapártelmezett szövegekkel
    iro_bevitel = StringVar(value=sor_elemek[0])
    Entry(feluliras_ablak, textvariable=iro_bevitel).grid(row=0, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
    cim_bevitel = StringVar(value=sor_elemek[1])
    Entry(feluliras_ablak, textvariable=cim_bevitel).grid(row=1, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
    mufaj_bevitel = StringVar(value=sor_elemek[2])
    Entry(feluliras_ablak, textvariable=mufaj_bevitel).grid(row=2, column=2, pady=10, padx=10, columnspan=2, ipadx=40)
    kiadas_eve_bevitel = StringVar(value=sor_elemek[3])
    Entry(feluliras_ablak, textvariable=kiadas_eve_bevitel).grid(row=3, column=2, pady=10, padx=10, columnspan=2, ipadx=40)

    #felülírás gomb funkciója
    def felulir():
        if iro_bevitel.get() and cim_bevitel.get() and mufaj_bevitel.get() and kiadas_eve_bevitel.get():
            # az kiadás éve ellenőrzése: csak szám lehet
            try:
                ev = int(kiadas_eve_bevitel.get())
                #a változtatások mentése az SQL táblázatba
                curs.execute("UPDATE konyvtar SET iro=?, cim=?, mufaj=?, kiadas_eve=? WHERE id=?", (iro_bevitel.get(), cim_bevitel.get(), mufaj_bevitel.get(), kiadas_eve_bevitel.get(), kijelolt_sor))
                conn.commit()
                frissites()
                messagebox.showinfo("", "A felülírás sikerült")
            except:
                messagebox.showerror("", "A felülírás sikertelen!")

    # felülírás gombok léétrehozása
    felulir_gomb = Button(feluliras_ablak, text="Felülírás", font="algerian 15", command=felulir)
    felulir_gomb.grid(row=5, column=1, pady=10, padx=10)

    megsem_gomb = Button(feluliras_ablak, text="Mégsem", font="algerian 15", command=feluliras_ablak.destroy)
    megsem_gomb.grid(row=5, column=3, pady=10, sticky=E)

indulas()
ablak.mainloop()
conn.commit()
conn.close()
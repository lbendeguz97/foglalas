import datetime
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
class Szoba ():
    def __init__(self, ar: int, szobaszam: int) -> None:
        self.ar=ar
        self.szobaszam=szobaszam
class Egyagyasszoba(Szoba):
    def __init__(self, ar, szobaszam, dohanyzo=False) -> None:
        super().__init__(ar, szobaszam)
        self.dohanyzo=dohanyzo
        self.szobatipus="Egy ágyas szoba (1 fő)"
    def __str__(self):
        return "Egyagyas szoba, száma: {0} ára: {1}, emeleteságyas: {2}".format(self.szobaszam, self.ar, self.dohanyzo)
class Ketagyasszoba(Szoba):
    def __init__(self, ar, szobaszam, franciaagy=False) -> None:
        super().__init__(ar, szobaszam)
        self.franciaagy=franciaagy
        self.szobatipus="Két ágyas szoba (2 fő)"
    def __str__(self):
        return "Kétágyas szoba, száma: {0} ára: {1}, franciaágyas: {2}".format(self.szobaszam, self.ar, self.franciaagy)
class Szalloda():
    def __init__(self, nev="", szobak= []):
        self.szobak=szobak
        self.nev=nev
    def szobakrealas(self,  ar: int, szobaszam: int, args={}, ketagyas=False):
        for o in self.szobak:
            if o.szobaszam==szobaszam:
                print("Szobaszám már létezik")
                return
        if ketagyas:
            if "franciaagy" in args:
                self.szobak.append(Ketagyasszoba(ar, szobaszam, args["franciaagy"]))
            else:
                self.szobak.append(Ketagyasszoba(ar, szobaszam))
        else:
            if "dohanyzo" in args:
                self.szobak.append(Egyagyasszoba(ar, szobaszam, args["dohanyzo"]))
            else:
                self.szobak.append(Egyagyasszoba(ar, szobaszam))
    def szobak_listazasa(self):
        for i in self.szobak:
            print(i)

class Foglalas():
    def __init__(self, datum: datetime.date, szoba: Szoba, nev: str):
        self.datum=datum
        self.szoba=szoba
        self.nev=nev
def fogl_objektum_krealas(datum, valasztott_szoba_szama, foglalo_neve):
    global foglalasok
    szoba=migransszallo.szobak[valasztott_szoba_szama]
    foglalasok.append(Foglalas(datum, szoba, foglalo_neve ))
    jelenlegi_foglalas=foglalasok[-1]
    str_date=jelenlegi_foglalas.datum.strftime("%Y/%d/%m")
    foglalas_string.append("Dátum: "+str_date+", Név: "+foglalo_neve+", Szobaszám: "+str(valasztott_szoba_szama))
    try:
        menu = bottomframe.nametowidget(ddm2.menuname)
        menu.delete(0, "end")
        for item in foglalas_string:
            menu.add_command(label=item, command=lambda value=item: lem_string.set(value))
        ent1.delete(0, END)
        #valasztott_szoba.set(0)
        refresh_upperframe(0)
        print(foglalas_string)
    except:
        pass
        
#Paraméterek beállítása
migransszallo=Szalloda("Migránszálló")
migransszallo.szobakrealas(ar=1000, szobaszam=0)
migransszallo.szobakrealas(2000, 1,  {"franciaagy": True}, True)
migransszallo.szobakrealas(2000, 2,  {"dohanyzo": True}, False)
migransszallo.szobak_listazasa()
foglalasok=[]
foglalhato_szobak=[]
foglalas_string=[]
for i in migransszallo.szobak:
    foglalhato_szobak.append(i.szobaszam)

#GUI
root=Tk()
topframe=Frame()
bottomframe=Frame()
root.title("Migránsszálló ötcsillagos hotel")
#GUI variables
valasztott_szoba=IntVar(root)
valasztott_szoba.set(foglalhato_szobak[0])
nev=StringVar(root)
szobatipus=StringVar(root)
szoba_spec=StringVar(root)
szoba_ar=StringVar(root)
lem_nev=StringVar(root)
lem_szobatipus=StringVar(root)
lem_szoba_spec=StringVar(root)
lem_string=StringVar(root)
#Foglalások létrehozása
fogl_objektum_krealas(datetime.date.today(), 0, "Sanyi")
fogl_objektum_krealas(datetime.date.today(), 1, "Peti")
fogl_objektum_krealas(datetime.date.today(), 2, "Gábor")
fogl_objektum_krealas(datetime.date.today(), 0, "Ferenc")
fogl_objektum_krealas(datetime.date.today(), 1, "Jancsi")
lem_string.set(foglalas_string[0])

#Make appointment
def foglalas():
    global foglalas_string
    datum=cal.get_date()
    valasztott_szoba_szama=int(valasztott_szoba.get())
    foglalo_neve=ent1.get()
    if valid_booking_check(datum, valasztott_szoba_szama, foglalo_neve):
        fogl_objektum_krealas(datum, valasztott_szoba_szama, foglalo_neve)
        messagebox.showinfo("Info", "Sikeres foglalás")
#Rerfresh function for upper frame
def refresh_upperframe(value):
    num=valasztott_szoba.get()
    room=migransszallo.szobak[num-1]
    attr=""
    try:
        if room.dohanyzo==True:
            attr="Dohányzó"
    except:
        if room.franciaagy==True:
            attr="Francia ágyas"
    szoba_spec.set(attr)
    szobatipus.set(room.szobatipus)
    szoba_ar.set(str(room.ar) +" Ft/nap")
def valid_booking_check(datum, szobaszam, nev):
    today=datetime.date.today()
    if datum<=today:
        messagebox.showerror("Hiba", "Legkorábban a holnapi naptól foglalhat")
        return False
    for i in foglalasok:
        if i.datum==datum and i.szoba.szobaszam==szobaszam:
            messagebox.showerror("Hiba", "A megadott napon a megadott szoba már foglalt")
            return False
    if nev=="":
        messagebox.showerror("Hiba", "A név mező nem lehet üres")
        return False
    return True
def lemondas():
    global foglalasok
    lemondas=lem_string.get()
    num=foglalas_string.index(lemondas)
    foglalasok.pop(num)
    foglalas_string.remove(lemondas)
    menu = bottomframe.nametowidget(ddm2.menuname)
    menu.delete(0, "end")
    for item in foglalas_string:
        menu.add_command(label=item, command=lambda value=item: lem_string.set(value))
    lem_string.set(foglalas_string[0])
    messagebox.showinfo("Info", "Sikeres lemondás")
#GUI
#FRAME1
#ROW0
txt1= Label(topframe, text="Foglalás")
txt1.grid(column=0, row=0)
#ROW1
cal=DateEntry(topframe,selectmode='day')
cal.grid(row=1,column=0,padx=15)

txt1= Label(topframe, text="Válasszon szobát")
txt1.grid(column=1, row=1)
ddm1 = OptionMenu(topframe, valasztott_szoba, *foglalhato_szobak, command=refresh_upperframe)
ddm1.grid(column=2, row=1)
but1=Button(topframe, text="Foglalás", command=foglalas)
but1.grid(column=3, row=1, padx=15)
#ROW2
txt2= Label(topframe, text="Adja meg nevét:")
txt2.grid(column=0, row=2, sticky="w")
ent1=Entry(topframe, textvariable=nev, width=30)
ent1.grid(row=2, column=1, columnspan=3)
#ROW3
txt3= Label(topframe, text="Személyek száma:")
txt3.grid(column=0, row=3, sticky="w")
txt4= Label(topframe, textvariable=szobatipus)
txt4.grid(column=1, row=3, sticky="e")
#ROW4
txt4= Label(topframe, text="Megjegyzés:")
txt4.grid(column=0, row=4, sticky="w")
txt5= Label(topframe, textvariable=szoba_spec)
txt5.grid(column=1, row=4, sticky="e")
#ROW5
txt_ar= Label(topframe, text="Ár:")
txt_ar.grid(column=0, row=5, sticky="w")
txt_ar_int= Label(topframe, textvariable=szoba_ar)
txt_ar_int.grid(column=1, row=5, sticky="e")
#FRAME2
#ROW1
txt6= Label(bottomframe, text="Foglalások")
txt6.grid(column=0, row=0, sticky="w")
ddm2 = OptionMenu(bottomframe, lem_string, *foglalas_string)
ddm2.grid(column=0, row=1, columnspan=3, sticky="w")
#ROW2
but2=Button(bottomframe, text="Foglalás lemondása", command=lemondas)
but2.grid(column=0, row=2, sticky="w")
#MAIN GUI
topframe.pack( side = TOP )
bottomframe.pack( side = BOTTOM )
refresh_upperframe(0)
root.mainloop()


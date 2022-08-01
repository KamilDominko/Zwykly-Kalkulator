import tkinter as tk
from tkinter import ttk


class NumButton(ttk.Button):
    def __init__(self, master, numer, kalkulator):
        super().__init__(master, text=str(numer), command=lambda: kalkulator.click_num_btn(numer))


class OperButton(ttk.Button):
    def __init__(self, master, symbol, kalkulator):
        super().__init__(master, text=str(symbol), command=lambda: kalkulator.click_oper_btn(symbol))


class Operacja:
    def __init__(self):
        self.oper = None

    def set(self, symbol):
        if symbol != "=":
            self.oper = symbol

    def clear(self):
        self.oper = None

    def oblicz(self, zmn1, zmn2):
        x = None
        if self.oper == "+":
            x = zmn1 + zmn2
        elif self.oper == "-":
            x = zmn1 - zmn2
        elif self.oper == "*":
            x = zmn1 * zmn2
        elif self.oper == "/":
            x = zmn1 // zmn2
        return int(x)

    def drop(self):
        return self.oper


class Zmienna:
    def __init__(self):
        self.zmn = None

    def set(self, zmienna):
        self.zmn = int(zmienna)

    def clear(self):
        self.zmn = None

    def add(self, var):
        x = str(self.zmn) + str(var)
        self.set(x)

    def change_sign(self):
        self.zmn *= -1

    def drop(self):
        return self.zmn


class Kalkulator:
    def __init__(self):
        self.zmn1 = Zmienna()
        self.zmn2 = Zmienna()
        self.oper = Operacja()
        self.suma = None
        self.root = tk.Tk()
        self.root_frame = None
        self.display_text = None

        self.option_var = tk.IntVar(self.root)
        self.languages = [1, 0.8, 0.6]

    def ustawienia_programu(self):
        self.root.title("Zwykły Kalkulator")  # ustawia tytuł programu
        self.root.resizable(False, False)  # możliwosć zmiany rozmiarów okna myszką
        self.root.attributes('-alpha', 1)  # przezroczystość okna 0.0 - przezroczyste
        self.root.attributes('-topmost', 1)  # okno na wierzchu innych okien
        self.root.iconbitmap("./icon.ico")  # ustawia ikone programu
        self.root.eval('tk::PlaceWindow . center')  # sutawia okno na środek ekranu

    def click_num_btn(self, x):
        if self.oper.drop() is None:
            if self.zmn1.drop() is None:
                self.zmn1.set(x)
                self.suma = None
            elif self.zmn1.drop() is not None:
                self.zmn1.add(x)
            self.display_text.set(self.zmn1.drop())
        elif self.oper.drop() is not None:
            if self.zmn2.drop() is None:
                self.zmn2.set(x)
            elif self.zmn2.drop() is not None:
                self.zmn2.add(x)
            self.display_text.set(self.zmn2.drop())

    def wykonaj_obliczenia(self):
        self.suma = self.oper.oblicz(self.zmn1.drop(), self.zmn2.drop())
        self.zmn1.clear()
        self.zmn2.clear()
        self.oper.clear()
        self.display_text.set(self.suma)

    def click_oper_btn(self, symbol):
        specialneZnaki = ("=", ",", "%", "+/-", "C")
        if symbol not in specialneZnaki:
            # if symbol != "=":  # Czy NIE JEST to znak równości
            if self.zmn1.drop() is None:  # ZMN1 = None
                if self.suma is None:
                    pass
                elif self.suma is not None:
                    self.zmn1.set(self.suma)
                    self.oper.set(symbol)
            elif self.zmn1.drop() is not None:  # ZMN1 != None
                if self.zmn2.drop() is None:
                    self.oper.set(symbol)
                elif self.zmn2.drop() is not None:
                    self.wykonaj_obliczenia()
                    self.zmn1.set(self.suma)
                    self.oper.set(symbol)
        elif symbol == "=":  # Czy JEST to znak równości
            if self.zmn1.drop() is not None and self.zmn2.drop() is not None:
                self.wykonaj_obliczenia()
        elif symbol == "C":  # Czyszczenie zmiennych
            if self.zmn1.drop() is not None:
                if self.zmn2.drop() is None:
                    self.zmn1.clear()
                    self.display_text.set("")
                elif self.zmn2.drop() is not None:
                    self.zmn2.clear()
                    self.display_text.set("")
            elif self.zmn1.drop() is None:
                self.suma = None
                self.display_text.set("")
        elif symbol == "+/-":  # Zmiana znaku na przeciwny
            if self.zmn1.drop() is not None:
                if self.zmn2.drop() is None:
                    self.zmn1.change_sign()
                    self.display_text.set(self.zmn1.drop())
                elif self.zmn2.drop() is not None:
                    self.zmn2.change_sign()
                    self.display_text.set(self.zmn2.drop())

    def stworz_pasek_statusu(self):
        pasekMenu = tk.Menu(self.root, tearoff=0, bg="black", fg="black")
        kaskadaMenu = tk.Menu(pasekMenu, tearoff=0)
        pasekMenu.add_cascade(label="Ustawienia", menu=kaskadaMenu)
        self.stworz_opcje_przezroczystosci(kaskadaMenu)  # Dodaje opcje przezroczystośći do kaskadowego menu aplikacji
        # self.stworz_opcje_motywu(kaskadaMenu)
        kaskadaMenu.add_command(label="Wyjście", command=self.root.quit)
        self.root.config(menu=pasekMenu, bg="black")

    def stworz_opcje_motywu(self, kaskadaMenu):  # Porzucone
        kaskadaMotywu = tk.Menu(kaskadaMenu, tearoff=0)
        kaskadaMenu.add_cascade(label="Motyw", menu=kaskadaMotywu)
        kaskadaMotywu.add_command(label="Jasny", command=lambda: self.ustaw_motyw("jasny"))
        kaskadaMotywu.add_command(label="Ciemny", command=lambda: self.ustaw_motyw("ciemny"))

    def ustaw_motyw(self, motyw="jasny"):  # Porzucone
        if motyw.lower() == "jasny":
            print("jasny")
            self.root.configure(background="white")
            self.root_frame.configure(bg="white")
        elif motyw.lower() == "ciemny":
            print("ciemny")
            self.display.configure(bg="#181818", fg="white")
            self.keyboard_frame.configure(bg="#181818")

    def stworz_opcje_przezroczystosci(self, kaskadaMenu):
        kaskadaPrzezroczystosci = tk.Menu(kaskadaMenu, tearoff=0)
        kaskadaMenu.add_cascade(label="Przezroczystość", menu=kaskadaPrzezroczystosci)
        kaskadaPrzezroczystosci.add_command(label="1", command=lambda: self.ustaw_przezroczystosc(1))
        kaskadaPrzezroczystosci.add_command(label="0,9", command=lambda: self.ustaw_przezroczystosc(0.9))
        kaskadaPrzezroczystosci.add_command(label="0,8", command=lambda: self.ustaw_przezroczystosc(0.8))
        kaskadaPrzezroczystosci.add_command(label="0,7", command=lambda: self.ustaw_przezroczystosc(0.7))
        kaskadaPrzezroczystosci.add_command(label="0,6", command=lambda: self.ustaw_przezroczystosc(0.6))

    def ustaw_przezroczystosc(self, var):
        self.root.attributes('-alpha', var)

    def stworz_wyswietlacz(self):
        display_frame = tk.Frame(self.root_frame)
        display_frame.grid(column=0, row=0, sticky="NEWS")
        self.display = tk.Label(display_frame, anchor="e", textvariable=self.display_text, font=("Arial", 20))
        self.display.pack(ipady=20, fill="both")

    def stworz_klawisze_cyfr(self, keyboard_frame, pad, ipad):
        NumButton(keyboard_frame, 1, self).grid(column=0, row=3, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 2, self).grid(column=1, row=3, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 3, self).grid(column=2, row=3, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 4, self).grid(column=0, row=2, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 5, self).grid(column=1, row=2, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 6, self).grid(column=2, row=2, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 7, self).grid(column=0, row=1, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 8, self).grid(column=1, row=1, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 9, self).grid(column=2, row=1, padx=pad, pady=pad, ipady=ipad)
        NumButton(keyboard_frame, 0, self).grid(column=0, row=4, padx=pad, pady=pad, ipady=ipad, columnspan=2,
                                                sticky="NSWE")

    def stworz_klawisze_operacji(self, keyboard_frame, pad, ipad):
        OperButton(keyboard_frame, "+", self).grid(column=3, row=3, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "-", self).grid(column=3, row=2, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "*", self).grid(column=3, row=1, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "/", self).grid(column=3, row=0, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "=", self).grid(column=3, row=4, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, ",", self).grid(column=2, row=4, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "%", self).grid(column=2, row=0, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "+/-", self).grid(column=1, row=0, padx=pad, pady=pad, ipady=ipad)
        OperButton(keyboard_frame, "C", self).grid(column=0, row=0, padx=pad, pady=pad, ipady=ipad)

    def stworz_klawiature(self):
        pad, ipad = 2, 15
        self.keyboard_frame = tk.Frame(self.root_frame, bd=8)
        self.keyboard_frame.grid(column=0, row=1, sticky="e")
        self.keyboard_frame.columnconfigure(0, weight=1)
        self.keyboard_frame.rowconfigure(0, weight=1)
        self.keyboard_frame.grid_propagate(True)
        self.stworz_klawisze_cyfr(self.keyboard_frame, pad, ipad)
        self.stworz_klawisze_operacji(self.keyboard_frame, pad, ipad)

    def stworz_glowne_okno(self):
        self.display_text = tk.StringVar()
        self.root_frame = tk.Frame(self.root)
        self.root_frame.pack()
        self.ustawienia_programu()
        self.stworz_pasek_statusu()
        self.stworz_wyswietlacz()
        self.stworz_klawiature()

    def uruchom(self):
        self.stworz_glowne_okno()
        self.root.mainloop()


if __name__ == "__main__":
    Kalkulator().uruchom()

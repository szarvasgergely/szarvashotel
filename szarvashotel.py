import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random


class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def ar_megad(self):
        pass


class EgyagyasSzoba(Szoba):
    def ar_megad(self):
        return self.ar

    def __init__(self, szobaszam):
        super().__init__(szobaszam, 10000)


class KetagyasSzoba(Szoba):
    def ar_megad(self):
        return self.ar

    def __init__(self, szobaszam):
        super().__init__(szobaszam, 17500)


class Foglalas:
    def __init__(self, szobaszam, datum, foglalasi_szam, ar):
        self.szobaszam = szobaszam
        self.datum = datum
        self.foglalasi_szam = foglalasi_szam
        self.ar = ar


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
        self.szobak_hozzaadasa()

    def szobak_hozzaadasa(self):
        self.szobak.append(EgyagyasSzoba("01"))
        self.szobak.append(KetagyasSzoba("02"))
        self.szobak.append(EgyagyasSzoba("03"))

    def foglalas(self, szobaszam, datum):
        datum_obj = datetime.strptime(datum, '%Y-%m-%d')
        if datum_obj < datetime.now():
            return "A foglalási dátum nem lehet a múltban."
        if any(f.szobaszam == szobaszam and f.datum == datum for f in self.foglalasok):
            return "Ez a szoba már foglalt ezen a napon."
        szoba = next((s for s in self.szobak if s.szobaszam == szobaszam), None)
        if not szoba:
            return "Nem létező szobaszám."
        foglalasi_szam = str(random.randint(10000000, 99999999))
        self.foglalasok.append(Foglalas(szobaszam, datum, foglalasi_szam, szoba.ar_megad()))
        return f"Foglalás sikeres. Foglalási szám: {foglalasi_szam}, Ár: {szoba.ar_megad()} Ft"

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(
            f"Dátum: {f.datum}, Szobaszám: {f.szobaszam}, Foglalási szám: {f.foglalasi_szam}, Ár: {f.ar} Ft" for f in
            self.foglalasok)

    def foglalas_torlese(self, foglalasi_szam):
        torlendo_foglalas = next((f for f in self.foglalasok if f.foglalasi_szam == foglalasi_szam), None)
        if torlendo_foglalas:
            self.foglalasok.remove(torlendo_foglalas)
            return f"Foglalás törölve: {foglalasi_szam}"
        return "Nincs ilyen foglalási szám."


def felhasznaloi_interfesz():
    szalloda = Szalloda("Szarvas Hotel")
    print(f"Üdvözöljük a {szalloda.nev}ben!")

    # Kezdeti foglalások hozzáadása
    szalloda.foglalas("01", (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
    szalloda.foglalas("02", (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'))
    szalloda.foglalas("03", (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'))
    szalloda.foglalas("01", (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'))
    szalloda.foglalas("02", (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'))

    while True:
        print("\n1. Foglalás\n2. Foglalások listázása\n3. Foglalás törlése\n4. Kilépés")
        valasztas = input("Válasszon egy opciót: ")
        if valasztas == "1":
            szobaszam = input("Adja meg a szobaszámot (01, 02, 03): ")
            datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD): ")
            print(szalloda.foglalas(szobaszam, datum))
        elif valasztas == "2":
            print(szalloda.foglalasok_listazasa())
        elif valasztas == "3":
            foglalasi_szam = input("Adja meg a törlendő foglalási számot: ")
            print(szalloda.foglalas_torlese(foglalasi_szam))
        elif valasztas == "4":
            print("Kilépés a programból.")
            break
        else:
            print("Érvénytelen opció.")


felhasznaloi_interfesz()
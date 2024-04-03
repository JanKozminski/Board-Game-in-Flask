import random

from karta import Karta


class Gracz:
    def __init__(self, identyfikator, kolor):
        self.identyfikator = identyfikator
        self.kolor = kolor
        self.zestaw_kart = self.generuj_karty()
        self.aktualny_wynik = 0

    def generuj_karty(self):
        wartosci = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
        random.shuffle(wartosci)
        return [Karta(self.kolor, wartosc) for wartosc in wartosci[:10]]

    def __repr__(self):
        return f"Gracz({self.identyfikator}, {self.kolor})"
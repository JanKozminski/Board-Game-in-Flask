import uuid

from karta import Karta


class Gra:
    def __init__(self, liczba_graczy=2):
        self.siatka = [[None for _ in range(6)] for _ in range(6)]
        self.gra_aktywna = True
        self.aktywny_gracz = 0
        self.gracze = []
        self.liczba_graczy = liczba_graczy

    def umiesc_karte(self, x, y, nowa_karta):
        print(f"Próba umieszczenia karty na pozycji ({x}, {y})")

        obecna_karta = self.siatka[x][y]

        if isinstance(obecna_karta, dict):
            obecna_karta = Karta.from_dict(obecna_karta)

        print(f"Obecna karta na pozycji: {obecna_karta}")
        print(f"Nowa karta do umieszczenia: {nowa_karta}")

        if obecna_karta is None or nowa_karta.porownaj(obecna_karta):
            self.siatka[x][y] = nowa_karta.to_dict()
            print("Karta umieszczona poprawnie.")
            if self.sprawdz_wygrana():
                return True, "Gracz wygrał!"
            return True, "Karta poprawnie umieszczona"
        print("Nie można umieścić karty o mniejszym nominale.")
        return False, "Nie można umieścić karty o mniejszym lub równym nominale"

    def to_dict(self):
        siatka_serialized = [[karta.to_dict() if isinstance(karta, Karta) else karta for karta in row] for row in
                             self.siatka]
        return {
            'siatka': siatka_serialized,
            'gra_aktywna': self.gra_aktywna,
            'aktywny_gracz': self.aktywny_gracz,
            'gracze': [gracz.to_dict() for gracz in self.gracze],
            'liczba_graczy': self.liczba_graczy
        }

    @classmethod
    def from_dict(cls, data):

        gra = cls()
        gra.siatka = [[Karta.from_dict(karta) if karta else None for karta in row] for row in data['siatka']]
        gra.gra_aktywna = data['gra_aktywna']
        gra.aktywny_gracz = data['aktywny_gracz']
        gra.gracze = data['gracze']
        gra.liczba_graczy = data.get('liczba_graczy', 2)
        return gra

    def karta_from_dict(self, karta_dict):
        if isinstance(karta_dict, Karta):
            return karta_dict
        elif karta_dict:
            return Karta(karta_dict['kolor'], karta_dict['wartosc'], uuid.UUID(karta_dict['id']))
        return None

    def sprawdz_wygrana(self):
        print(f"Aktualna liczba graczy: {self.liczba_graczy}")
        wymagana_dlugosc_ciagu = 4 if self.liczba_graczy == 2 else 3

        for i in range(6):
            if self.czy_linia_wygrana([self.siatka[i][j] for j in range(6)], wymagana_dlugosc_ciagu) or \
                    self.czy_linia_wygrana([self.siatka[j][i] for j in range(6)], wymagana_dlugosc_ciagu):
                self.gra_aktywna = False
                return True

        for i in range(6 - wymagana_dlugosc_ciagu + 1):
            if self.czy_linia_wygrana([self.siatka[j][j + i] for j in range(6 - i)], wymagana_dlugosc_ciagu) or \
                    self.czy_linia_wygrana([self.siatka[j + i][j] for j in range(6 - i)], wymagana_dlugosc_ciagu) or \
                    self.czy_linia_wygrana([self.siatka[j][5 - j - i] for j in range(6 - i)], wymagana_dlugosc_ciagu) or \
                    self.czy_linia_wygrana([self.siatka[j + i][5 - j] for j in range(6 - i)], wymagana_dlugosc_ciagu):
                self.gra_aktywna = False
                return True

        return False

    def czy_linia_wygrana(self, linia, wymagana_dlugosc_ciagu):
        if len(linia) < wymagana_dlugosc_ciagu:
            return False

        for i in range(len(linia) - wymagana_dlugosc_ciagu + 1):
            if all(linia[j] and (Karta.from_dict(linia[j]) if isinstance(linia[j], dict) else linia[j]).kolor == (
                    Karta.from_dict(linia[i]) if isinstance(linia[i], dict) else linia[i]).kolor for j in
                   range(i, i + wymagana_dlugosc_ciagu)):
                return True

        return False

    def dodaj_gracza(self, gracz):
        self.gracze.append(gracz)

    def zmien_gracza(self):
        self.aktywny_gracz = (self.aktywny_gracz + 1) % len(self.gracze)

    def __repr__(self):
        return f"Gra(aktywny_gracz={self.aktywny_gracz}, gracze w rozgrywce = {self.gracze})"

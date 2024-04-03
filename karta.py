import uuid


class Karta:
    def __init__(self, kolor, wartosc, id=None):
        self.kolor = kolor
        self.wartosc = wartosc
        self.id = id or uuid.uuid4()

    def porownaj(self, inna_karta):
        return self.wartosc > inna_karta.wartosc

    def to_dict(self):
        return {'kolor': self.kolor, 'wartosc': self.wartosc, 'id': str(self.id)}

    @classmethod
    def from_dict(cls, data):
        return cls(data['kolor'], data['wartosc'], uuid.UUID(data['id']))

    def __repr__(self):
        return f"Karta({self.kolor}, {self.wartosc})"

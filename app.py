from flask import Flask, render_template, request, redirect, url_for, session, flash

from gra import Gra
from gracz import Gracz
from karta import Karta

app = Flask(__name__)

app.secret_key = 'TwojTajnyKlucz'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plansza')
def plansza():
    gracze_dane = session.get('gracze', [])
    gracze = [Gracz(dane['identyfikator'], dane['kolor']) for dane in gracze_dane]

    for gracz, dane in zip(gracze, gracze_dane):
        gracz.zestaw_kart = [Karta.from_dict(karta_data) for karta_data in dane['zestaw_kart']]

        gra_data = session.get('gra')
        gra = Gra.from_dict(gra_data) if gra_data else Gra()

    return render_template('plansza.html', gracze=gracze, gra=gra, gra_aktywna=gra.gra_aktywna)


@app.route('/ustaw_graczy', methods=['POST'])
def ustaw_graczy():
    liczba_graczy = request.form.get('liczba_graczy', type=int)
    session['aktywny_gracz'] = 0
    session['liczba_graczy'] = liczba_graczy

    kolory = ['red', 'blue', 'green', 'yellow']

    gracze = [Gracz(i, kolory[i % len(kolory)]) for i in range(liczba_graczy)]

    for gracz in gracze:
        gracz.zestaw_kart = gracz.generuj_karty()

    session['gracze'] = [{'identyfikator': gracz.identyfikator, 'kolor': gracz.kolor,
                          'zestaw_kart': [karta.to_dict() for karta in gracz.zestaw_kart]} for gracz in gracze]

    nowa_gra = Gra(liczba_graczy=liczba_graczy)
    session['gra'] = nowa_gra.to_dict()

    return redirect(url_for('plansza'))


@app.route('/umiesc_karte', methods=['POST'])
def umiesc_karte():
    karta_id = request.form.get('karta_id')
    x = request.form.get('x', type=int)
    y = request.form.get('y', type=int)

    gracze_dane = session.get('gracze', [])
    aktywny_gracz_id = session.get('aktywny_gracz')
    gracze = [Gracz(dane['identyfikator'], dane['kolor']) for dane in gracze_dane]

    for gracz, dane in zip(gracze, gracze_dane):
        gracz.zestaw_kart = [Karta.from_dict(karta_data) for karta_data in dane['zestaw_kart']]

    aktywny_gracz = gracze[aktywny_gracz_id]

    gra_data = session.get('gra')
    gra = Gra.from_dict(gra_data) if gra_data else Gra()

    if not gra.gra_aktywna:
        flash("Gra zakończona, nie można umieścić więcej kart.")
        return redirect(url_for('plansza'))

    karta_do_umieszczenia = next((karta for karta in aktywny_gracz.zestaw_kart if str(karta.id) == karta_id), None)

    if karta_do_umieszczenia is None:
        flash("Nie wybrano karty!")
        return redirect(url_for('plansza'))

    umieszczenie_udane, wiadomosc = gra.umiesc_karte(x, y, karta_do_umieszczenia)
    print(f"Wynik umieszczenia karty: {umieszczenie_udane}, wiadomość: {wiadomosc}")
    if umieszczenie_udane:
        aktywny_gracz.zestaw_kart.remove(karta_do_umieszczenia)
        gracze_dane[aktywny_gracz_id]['zestaw_kart'] = [karta.to_dict() for karta in aktywny_gracz.zestaw_kart]
        session['gracze'] = gracze_dane
        session['gra'] = gra.to_dict()

        if gra.sprawdz_wygrana():
            flash(f"Gracz {aktywny_gracz.identyfikator} (kolor: {karta_do_umieszczenia.kolor}) wygrał!")

        session['aktywny_gracz'] = (aktywny_gracz_id + 1) % len(gracze)
    else:
        flash(wiadomosc)

    return redirect(url_for('plansza'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12133, debug=True)

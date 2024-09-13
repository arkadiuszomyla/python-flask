from flask import Flask, render_template, url_for, request, flash #dodajemy import flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomethingWhatNo1CanGuess!'  #ustawiamy SECRET_KEY na potrzeby użycia ciasteczek, nie udostępniać np. na githubie :)

class Currency:
    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag

    def __repr__(self):  #funkcja __repl__ odpowiada za budowanie tekstowej wartości zapisywanej w klasie
        return '<Currency {}'.format(self.code)


class CantorOffer:
    def __init__(self):
        self.currencies = []
        self.danied_code = [] # dodajemy listę kodów zakazanych

    def load_offer(self):
        self.currencies.append(Currency('USD', 'Dollar', 'flaga_ameryka.jpg'))
        self.currencies.append(Currency('EUR', 'Euro', 'flaga_euro.jpg'))
        self.currencies.append(Currency('JPY', 'Yen', 'flaga_japan.jpg'))
        self.danied_code.append('USD')

    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return Currency('unknown', 'unknown', 'flaga_pirat.jpg')


@app.route('/')
def index():
    return 'Strona główna'


@app.route('/exchange', methods=['GET','POST'])
def exchange():

    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange_dziedziczenie.html', offer=offer) #przekazujemy oferty jako parametr do wykorzystania
    else:
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        if currency in offer.danied_code:          #dodajemy komunikat flash, trzymany on jest jako plik cookie, trzeba zmodyfikować również odpowiednio Templates, nie można wykorzystać plików cookie jeśli nie mamy zdefiniowanego secret key
            flash('The currency {} connot be accepted'.format(currency))
        elif offer.get_by_code(currency) == 'unknown':
            flash('The currency {} connot be accepted'.format(currency))
        else:
            flash('Request to exchange {} was accepted'.format(currency))

        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_result_dziedziczenie.html', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))  #przekazujemy oferty jako parametr do wykorzystania


if __name__ == '__main__':
    app.run(debug=True)
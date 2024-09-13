from flask import Flask, render_template, url_for, request

app = Flask(__name__)


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

    def load_offer(self):
        self.currencies.append(Currency('USD', 'Dollar', 'flaga_ameryka.jpg'))
        self.currencies.append(Currency('EUR', 'Euro', 'flaga_euro.jpg'))
        self.currencies.append(Currency('JPY', 'Yen', 'flaga_japan.jpg'))

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
        return render_template('exchange_options_for.html', offer=offer) #przekazujemy oferty jako parametr do wykorzystania
    else:
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_options_result_for.html', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))  #przekazujemy oferty jako parametr do wykorzystania


if __name__ == '__main__':
    app.run(debug=True)
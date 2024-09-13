from flask import Flask, render_template, url_for, request, flash, g #odajemy 'g' - pozwala na przetrzymywanie zmiennych globalnych na skale pojedynczego requestu
import sqlite3 #dodajemy import

app_info = {
    'db_file': 'C:/Users/arkadiuszo/PycharmProjects/python-flask/data/cantor.db'
}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomethingWhatNo1CanGuess!'

def get_db():

    if not hasattr(g, 'sqlite3_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row # zwracane będą dane w postaci słowników, domyślnie zwracane są tuplety
        g.sqlite_db = conn
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):

    if hasattr(g, 'sqlite3_db'):
        g.sqlite3_db.close()


class Currency:
    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag

    def __repr__(self):
        return '<Currency {}'.format(self.code)


class CantorOffer:
    def __init__(self):
        self.currencies = []
        self.danied_code = []

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
    return render_template("index.html")


@app.route('/exchange', methods=['GET','POST'])
def exchange():

    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange.html', offer=offer)
    else:
        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        if currency in offer.danied_code:
            flash('The currency {} connot be accepted'.format(currency))
        elif offer.get_by_code(currency) == 'unknown':
            flash('The currency {} connot be accepted'.format(currency))
        else:
            db = get_db() #dodajemy zapis do bazy
            sql_command = 'insert into transactions (currency, amount, user) values (?, ?, ?)'
            db.execute(sql_command, [currency, amount, 'admin'])
            db.commit()

            flash('Request to exchange {} was accepted'.format(currency))

        return render_template('exchange_result.html', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))


if __name__ == '__main__':
    app.run(debug=True)
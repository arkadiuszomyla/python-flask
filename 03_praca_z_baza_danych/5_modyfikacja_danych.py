from flask import Flask, render_template, url_for, request, flash, g, redirect
import sqlite3
from datetime import date

app_info = {
    'db_file': 'C:/Users/arkadiuszo/PycharmProjects/python-flask/data/cantor.db'
}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomethingWhatNo1CanGuess!'


def get_db():
    if not hasattr(g, 'sqlite3_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row
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
    return render_template("index.html", active_menu='home')


@app.route('/exchange', methods=['GET','POST'])
def exchange():
    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange.html', active_menu='exchange', offer=offer)
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
            db = get_db()
            sql_command = 'insert into transactions (currency, amount, user) values (?, ?, ?)'
            db.execute(sql_command, [currency, amount, 'admin'])
            db.commit()

            flash('Request to exchange {} was accepted'.format(currency))

        return render_template('exchange_result.html', active_menu='exchange', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency))


@app.route('/history')
def history():
    db = get_db()
    sql_command = 'select id, currency, amount, trans_date from transactions;'
    cur = db.cursor()
    cur.execute(sql_command)
    transactions = cur.fetchall()

    return render_template('history_with_delete_and_modify.html', acive_menu='history', transactions=transactions) #dodajemy też parametr acive_menu, w menu.html pogrubioną czcionke mają strony, które są aktualnie aktywne


@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    db = get_db()
    sql_statement = 'delete from transactions where id = ?;'
    db.execute(sql_statement, [transaction_id])
    db.commit()

    return redirect(url_for('history'))


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    offer = CantorOffer()
    offer.load_offer()
    db = get_db()

    if request.method == 'GET':
        sql_statement = 'select id, currency, amount from transactions where id=?;'
        cur = db.execute(sql_statement, [transaction_id])
        transaction = cur.fetchone()

        if transaction == None:
            flash('No such transaction!')
            return redirect(url_for('history'))
        else:
            return render_template('edit_transaction.html', transaction=transaction, offer=offer, active_menu='history')

        return render_template('exchange.html', active_menu='exchange', offer=offer)
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
            sql_command = '''update transactions set currency=?, amount=?, user=?, trans_date=? where id=?'''
            db.execute(sql_command, [currency, amount, 'admin', date.today(), transaction_id])
            db.commit()

            flash('Transaction was updated')

        return redirect(url_for('history'))


if __name__ == '__main__':
    app.run(debug=True)
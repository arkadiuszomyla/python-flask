from flask import Flask, render_template, url_for, request, flash, g, redirect, session #importujemy sesje
import sqlite3
from datetime import date

import random
import string
import hashlib
import binascii

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


class UserPass:
    def __init__(self, user='', password=''):
        self.user = user
        self.password = password

    def hash_password(self):
        '''Hash a password for storing'''
        # the values generated using os.urandom(60)
        os_urandom_static = b'\xf5\xb1\x9f\xe5s\xff\xfc~\xa0\xac\xd6"P\xb4\xa1C\xb8\x19\xa8\xc3T\xab\xac `h.\xe9!\xa7;j\x9e\xff\xbe\x902\xcf\x93}\xe8\x1d\xa8\x03\xe4v0\xb0\x86G\xda\xcc\xda@2\xe6\xe5\x0c4\xcf'
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        '''Verify a stored password against one provided by user'''
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def get_random_user_password(self):
        random_user = ''.join(random.choice(string.ascii_lowercase)for i in range(3))
        self.user = random_user
        password_characters = string.ascii_letters
        random_password = ''.join(random.choice(password_characters)for i in range(3))
        self.password = random_password

    # dodajemy login_user
    def login_user(self):
        db = get_db()
        sql_statement = 'select id, name, email, password, is_active, is_admin from users where name=?'
        cur = db.execute(sql_statement, [self.user])
        user_record = cur.fetchone()

        if user_record != None and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None


@app.route('/init_app')
def init_app():
    db = get_db()
    sql_statement = 'select count(*) as cnt from users where is_active and is_admin;'
    cur = db.execute(sql_statement)
    active_admins = cur.fetchone()

    if active_admins != None and active_admins['cnt'] > 0:
        flash('Aplication is already set-up. Nothing to do')
        return redirect(url_for('index'))

    user_pass = UserPass()
    user_pass.get_random_user_password()
    db.execute('''insert into users(name, email, password, is_active, is_admin) values (?, ?, ?, True, True);''',
               [user_pass.user, 'noone@nowhere.no', user_pass.hash_password()])
    db.commit()
    flash('User {} with password {} has been created'.format(user_pass.user, user_pass.password))
    return redirect(url_for('index'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', active_menu='login')
    else:
        user_name = '' if 'user_name' not in request.form else request.form['user_name']
        user_pass = '' if 'user_pass' not in request.form else request.form['user_pass']

        login = UserPass(user_name, user_pass)
        login_record = login.login_user()

        if login_record != None:
            session['user'] = user_name
            flash('Logon succesfull, welcome {}'.format(user_name))
            return redirect(url_for('index'))
        else:
            flash('Logon failed, try again')
            return render_template('login.html')


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

    return render_template('history.html', acive_menu='history', transactions=transactions)


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
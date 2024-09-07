from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!!!!!!</h1>'


@app.route('/exchange')
def exchange():

    # tutaj formularz budujemy w html-u, po wypełnieniu formularza przejdź na stronę /exchange_process
    body = '''   
        <form id="exchange_form" action="/exchange_process" method="POST">
            <label for="currency">Currency</label>
            <input type="text" id="currency" name="currency" value="EUR"><br>
            <label for="amount">Amount</label>
            <input type="text" id="amount" name="amount" value="100"><br>
            <input type="submit" value="Send">
        </form>
    '''
    return body


@app.route('/exchange_process', methods=['POST']) #trzeba wskazać jakie metody są dozwolone dla danej 'ruty'
def exchange_process():

    currency = 'EUR'
    if 'currency' in request.form:
        currency = request.form['currency']

    amount = 100
    if 'amount' in request.form:
        amount = request.form['amount']

    body = f'You want to exchange {amount} {currency}?'
    return body


if __name__ == '__main__':
    app.run(debug=True)


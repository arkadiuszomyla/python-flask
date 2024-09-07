from flask import Flask, request, url_for, redirect #importujemy redirect

app = Flask(__name__)

#DLA ELEMENTÓW STATYCZNYCH TRZEBA ZAŁOŻYĆ FOLDER 'STATIC' lub inny

@app.route('/')
def index():

    #budujemy menu, here ma być jako link,w url_for odwołujemy się do nazwy metody, która ma być wywołana
    #aby wywołać w url_for funkcję z parametrami trzeba dodatkowo przekazać wartości
    #w img src dodajemy wyświetlanie obrazka
    menu = f'''
        Go <a href="{url_for('exchange')}">here</a> to exchange money<br>
        To exchange 50 CHF go <a href="{url_for('cantor', currency='CHF', amount=50)}">here</a><br><br>
        <img src="{url_for('static', filename='dollars.jpg')}"><br><br>
        <img src="{url_for('static', filename='currencies/euro.jpg')}"><br><br>
        '''

    return f'<h1>Hello World!!!!!!</h1><br>{menu}'


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():

    if request.method == 'GET':  #formularz chcemy wyświetlić tylko jeśli GET
        # tutaj formularz budujemy w html-u, tutaj formularz odwołuje się już sam do siebie
        body = f'''   
            <form id="exchange_form" action="{url_for('exchange')}" method="POST">
                <label for="currency">Currency</label>
                <input type="text" id="currency" name="currency" value="EUR"><br>
                <label for="amount">Amount</label>
                <input type="text" id="amount" name="amount" value="100"><br>
                <input type="submit" value="Send">
            </form>
            '''
        return body
    else:  #jeżeli nie GET, wiemy, że POST
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        body = f'You want to exchange {amount} {currency}?'
        #return body
        #return redirect(url_for('index')) #przerzucamy użytkownika na stronę główną
        return redirect(url_for('cantor', currency=currency, amount=amount))


@app.route('/cantor/<currency>/<int:amount>')  #chcemy w adresie strony podawać swoje zmienne, można kontrolować typy np.: <int:amount>, <string:currency>
def cantor(currency, amount):   #nazwy i ilość zmiennych w funkcji muszą być takie same jak w route
    message = f'<h1>You selected {currency} and amount {amount}</h1>'
    return message


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, url_for, request
#Jeżeli chce wywoływać szablony muszę założyć dodatkowy katalog o nazwie Templates, w takim katalogu można tworzyć pliki odpowiedzialne za zawartość strony
#W takich templetach można korzystać z kodu używając {{}}

#Jeżeli chce w plikach Templates umieścić bardziej złożony kawałek kodu (np if) trzeba go umieścić między znacznikami {% %}

app = Flask(__name__)


@app.route('/')
def index():

    return 'This is index'


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():

    if request.method == 'GET':
        return render_template('exchange_options.html')
    else:
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']

        amount = 100
        if 'amount' in request.form:
            amount = request.form['amount']

        return render_template('exchange_options_result.html', currency=currency, amount=amount)  #przekazujemy parametry do szablonu


if __name__ == '__main__':
    app.run(debug=True)
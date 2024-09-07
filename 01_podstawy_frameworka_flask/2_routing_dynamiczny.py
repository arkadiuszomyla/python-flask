#python -m venv venv - stworzenie środowiska wirtualnego
#z terminala: .\venv\Scripts\activate - aktywacja środowiska
#jeżeli aplikacja ma się nazywac inaczej niż 1_wstep_app.py trzeba ustawić zmienną środowiskową set FLASK_APP=nowa_nazwa.py
#zmienna środowiskowa set FLASK_DEBUG=1 włącza tryb debuowania, jeżeli strona wykryje zmiany w kodzie to aplikacja sama się zresetuje - u mnie zadziałało dopiero dodaanie do app.run: debug=True i uruchamianie aplikacji przez python 1_wstep_app.py
#NA POTRZEBY NOTATEK ZMIENIAM NAZWĘ z app.py

from flask import Flask

app = Flask(__name__) #konstruktor klasy flask wymaga przekazania nazwy modułu, w którym jest tworzona aplikacja


@app.route('/')
def index():
    return '<h1>Hello World!!!!!!</h1>'


@app.route('/cantor/<currency>/<int:amount>')  #chcemy w adresie strony podawać swoje zmienne, można kontrolować typy np.: <int:amount>, <string:currency>
def cantor(currency, amount):   #nazwy i ilość zmiennych w funkcji muszą być takie same jak w route
    message = f'<h1>You selected {currency} and amount {amount}</h1>'
    return message


@app.route('/about')
def about():
    return '<h1>about page</h1>'


@app.route('/error')
def error():
    a = 10
    b = 0
    return '<h1>error page' \
           ' {}</h1>'.format(a/b)


if __name__ == '__main__':   #pozwala uruchomić skrypt przez 'python 1_wstep_app.py' w terminalu
    app.run(debug=True)


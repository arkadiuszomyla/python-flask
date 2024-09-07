from flask import Flask, request #dodajemy request

app = Flask(__name__)


@app.route('/')
def index():

    color = 'black'
    style = 'normal'
    print(request.query_string) #w adresie strony możemy wpisać np. http://127.0.0.1:5000/?color=blue&style=italic

    if 'color' in request.args:
        print(request.args['color'])  #możemy się odwołać do konkretnego przekazanego parametru
        color = request.args['color']

    if 'style' in request.args:
        style = request.args['style']

    for p in request.args:  #można wyświetlić sobie to co wpisują użytkownicy np. w pętli
        print(p, request.args[p])

    return f'<h1 style="color:{color}; font-style:{style};">Hello World!!!!!!</h1>'


if __name__ == '__main__':
    app.run(debug=True)


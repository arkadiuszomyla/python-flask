# https://getbootstrap.com/docs/5.3/components/navbar/#how-it-works
# https://getbootstrap.com/docs/5.3/getting-started/introduction/#quick-start

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_bootstrap_bez_flask_bootstrap.html')


if __name__ == '__main__':
    app.run(debug=True)
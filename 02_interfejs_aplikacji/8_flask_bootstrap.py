# pip install flask-bootstrap
# https://pythonhosted.org/Flask-Bootstrap/basic-usage.html
# https://getbootstrap.com/docs/5.3/components/navbar/#how-it-works
# https://getbootstrap.com/docs/5.3/getting-started/introduction/#quick-start

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index_flask_bootstrap.html')


if __name__ == '__main__':
    app.run(debug=True)
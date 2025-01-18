from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-expense')
def add_expense():
    return render_template('add_expense.html')


if __name__ == '__main__':
    app.run(debug=True)

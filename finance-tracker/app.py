from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


expenses = []

@app.route('/')
def index():
    return render_template('index.html', expences=expenses)


@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
        if request.method == 'POST':
             amount = request.form['amount']
             category = request.form['category']
             description = request.form['description']
             date = request.form['date']

             expense = {
                  'amount': amount,
                  'category': category,
                  'description': description,
                  'date':date
             }
             expenses.append(expense)
             return redirect(url_for('index'))
        return render_template('add_expense.html')


if __name__ == '__main__':
    app.run(debug=True)

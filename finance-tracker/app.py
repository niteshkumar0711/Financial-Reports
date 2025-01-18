from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


expenses = []
total_budget = 10000

@app.route('/')
def index():
    total_expenses = sum([float(expense["amount"]) for expense in expenses])
    remaining_balance = total_budget - total_expenses
    return render_template('index.html', expenses=expenses, total_budget=total_budget, remaining_balance= remaining_balance)


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

@app.route('/set-budget', methods=['GET', 'POST'])
def set_budget():
     global total_budget

     if request.method == 'POST':
          new_budget = request.form.get('budget')
          if new_budget and new_budget.isdigit():
               total_budget = float(new_budget)
               return redirect('/')
     return render_template('set_budget.html')

if __name__ == '__main__':
    app.run(debug=True)

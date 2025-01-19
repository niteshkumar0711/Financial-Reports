from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lxcifer0711'


# expenses = []
total_budget = 10000


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')

@app.route("/")
def index():
    expenses = session.get('expenses',[])
    total_expenses = sum([float(expense["amount"]) for expense in expenses])
    remaining_balance = total_budget - total_expenses
    today = get_today_date()
    recent_expenses = [expense for expense in expenses if expense['date'] == today]

    return render_template(
        "index.html",
        expenses=recent_expenses,
        total_budget=total_budget,
        remaining_balance=remaining_balance,
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    expenses = session.get('expenses',[])
#     today = datetime.today().strftime('%Y-%m-%d')

    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description")

        today = datetime.today().strftime('%Y-%m-%d')



        if name and amount and category and date:
            expenses.append(
                {
                    "name": name,
                    "amount": float(amount),
                    "category": category.capitalize(),
                    "date": date,
                    "description": description
                    or "No description provided",
                }
            )
            session['expenses'] = expenses
            return redirect("/")
        else:
            return render_template("add_expense.html", error="All fields are required!")

    return render_template("add_expense.html")



@app.route("/set-budget", methods=["GET", "POST"])
def set_budget():
    global total_budget

    if request.method == "POST":
        new_budget = request.form.get("budget")
        if new_budget and new_budget.isdigit():
            total_budget = float(new_budget)
            return redirect("/")
    return render_template("set_budget.html")

@app.route('/view-expenses')
def view_expenses():
    expenses = session.get('expenses', [])
    return render_template('view_expenses.html', expenses=expenses)


if __name__ == "__main__":
    app.run(debug=True)

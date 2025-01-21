from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lxcifer0711'


# expenses = []
total_budget = 10000

@app.before_request
def set_default_budget():
    if 'total_budget' not in session:
        session['total_budget'] = 10000


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')

@app.route("/")
def index():
    expenses = session.get('expenses',[])
    total_budget = session.get('total_budget',0)
    total_expenses = sum([float(expense["amount"]) for expense in expenses])
    remaining_balance = total_budget - total_expenses
    over_budget_warning = False

    if total_expenses > total_budget:
        over_budget_warning = True

    today = get_today_date()
    recent_expenses = [expense for expense in expenses if expense['date'] == today]

    return render_template(
        "index.html",
        expenses=recent_expenses,
        total_budget=total_budget,
        remaining_balance=remaining_balance,
        over_budget_warning=over_budget_warning
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
    if request.method == "POST":
        new_budget = request.form.get("budget")
        if new_budget and new_budget.isdigit():
            total_budget = float(new_budget)
            session['total_budget'] = float(new_budget)
            return redirect("/")
    return render_template("set_budget.html")


@app.route("/reset-budget", methods=["POST"])
def reset_budget():
    expenses = session.get('expenses',[])
    session['total_budget'] = 10000
    session['expenses'] = expenses
    return redirect("/")


@app.route('/view-expenses')
def view_expenses():
    expenses = session.get('expenses', [])

    category_filter = request.args.get("category_filter")
    date_filter = request.args.get("date_filter")

    if category_filter:
        expenses = [expense for expense in expenses if expense['category'].lower() == category_filter.lower()]
    if date_filter:
        expenses = [expense for expense in expenses if expense['date']== date_filter]

    sort_by = request.args.get("sort_by")
    if sort_by == "amount_asc":
        expenses = sorted(expenses, key=lambda x: x['amount'])
    elif sort_by == "amount_desc":
        expenses = sorted(expenses, key=lambda x: x["amount"], reverse=True)
    elif sort_by == "date_asc":
        expenses = sorted(expenses, key=lambda x: x["date"])
    elif sort_by == "date_desc":
        expenses = sorted(expenses, key=lambda x: x["date"], reverse=True)
    elif sort_by == "name_asc":
        expenses = sorted(expenses, key=lambda x: x["name"].lower())
    elif sort_by == "name_desc":
        expenses = sorted(expenses, key=lambda x: x["name"].lower(), reverse=True)
    elif sort_by == "category_asc":
        expenses = sorted(expenses, key=lambda x: x["category"].lower())
    elif sort_by == "category_desc":
        expenses = sorted(expenses, key=lambda x: x["category"].lower(), reverse=True)

    return render_template('view_expenses.html', expenses=expenses)


if __name__ == "__main__":
    app.run(debug=True)

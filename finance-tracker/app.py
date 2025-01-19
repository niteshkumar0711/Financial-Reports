from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


expenses = []
total_budget = 10000


@app.route("/")
def index():
    total_expenses = sum([float(expense["amount"]) for expense in expenses])
    remaining_balance = total_budget - total_expenses
    return render_template(
        "index.html",
        expenses=expenses,
        total_budget=total_budget,
        remaining_balance=remaining_balance,
    )


@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    global expenses

    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description")

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
    global expenses
    return render_template('view_expenses.html', expenses=expenses)


if __name__ == "__main__":
    app.run(debug=True)

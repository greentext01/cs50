import os
import re
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT * FROM stocks WHERE userid = ?;", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?",
                      session["user_id"])[0]["cash"]
    total = 0
    for stock in stocks:
        info = lookup(stock["symbol"])
        total += info["price"] * stock["amount"]
        stock["price"] = info["price"]

    total += cash

    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("Symbol does not exist!")

        price = stock["price"]

        balance = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])

        if not request.form.get("shares").isdecimal():
            return apology('"Shares" is not a number')

        if balance[0]["cash"] < price * int(request.form.get("shares")):
            return apology("Can't afford!")

        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   balance[0]["cash"] - price * int(request.form.get("shares")), session["user_id"])

        db.execute("INSERT INTO transactions (symbol, amount, time, price, userid) VALUES (?, ?, ?, ?, ?)",
                   stock["symbol"], request.form.get("shares"), time.asctime(time.gmtime()), price, session["user_id"])

        selected = db.execute("SELECT userid FROM stocks WHERE symbol = ? AND userid = ?",
                              stock["symbol"], session["user_id"])
        if selected:
            db.execute("UPDATE stocks SET amount = amount + ? WHERE symbol = ? AND userid = ?",
                       request.form.get("shares"), stock["symbol"], session["user_id"])
        else:
            db.execute("INSERT INTO stocks (symbol, amount, name, userid) VALUES (?, ?, ?, ?);",
                       stock["symbol"], request.form.get("shares"), stock["name"], session["user_id"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE userid = ?;", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        resp = lookup(request.form.get("symbol"))
        if resp == None:
            return apology("Symbol does not exist")
        return render_template("quoted.html", name=resp["name"], symbol=resp["symbol"], price=usd(resp["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        check = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(check) != 0:
            return apology("Username already taken")
        
        if request.form.get("username") == "":
            return apology("Username is empty")

        if request.form.get("password") == "":
            return apology("Password is empty")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please select a stock")

        if not request.form.get("shares").isdecimal():
            return apology('"Shares" is not a number')

        amount = db.execute(
            "SELECT amount FROM stocks WHERE userid = ? AND symbol = ?;", session["user_id"], request.form.get("symbol"))

        if not amount:
            return apology("You don't own any shares of that stock")

        if amount[0]["amount"] - int(request.form.get("shares")) < 0:
            return apology("You dont own enough shares of that stock")

        if amount[0]["amount"] - int(request.form.get("shares")) == 0:
            db.execute("DELETE FROM stocks WHERE userid = ? AND symbol = ?;",
                       session["user_id"], request.form.get("symbol"))
        else:
            db.execute("UPDATE stocks SET amount = amount - ? WHERE userid = ? AND symbol = ?", request.form.get("shares"),
                       session["user_id"], request.form.get("symbol"))

        db.execute(
            "INSERT INTO transactions (symbol, amount, time, price, userid) VALUES (?, ?, ?, ?, ?)", request.form.get("symbol"), int(request.form.get("shares")) * -1, time.asctime(time.gmtime()), lookup(request.form.get("symbol"))["price"],
             session["user_id"])

        db.execute("UPDATE users SET cash = cash + ?", lookup(request.form.get("symbol"))["price"] * int(request.form.get("shares")))

        return redirect("/")
    else:
        stocks = db.execute(
            "SELECT * FROM stocks WHERE userid = ?;", session["user_id"])
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

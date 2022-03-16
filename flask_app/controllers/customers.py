from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.customer import Customer
from flask_app.models.product import Product
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")


@app.route('/login', methods=['POST'])
def login():
    customer = Customer.get_cust_by_email(request.form)
    if not customer:
        flash("Invalid Email", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(customer.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect("/")
    session['customer_id'] = customer.id
    return render_template('/dashboard.html', customer=customer)


@app.route('/dashboard')
def dashboard():
    if 'customer_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["customer_id"]
    }
    customer = Customer.get_one(data)
    return render_template("dashboard.html", customer=customer)


@app.route('/register', methods=['POST'])
def register():
    if not Customer.validate_register(request.form):
        return redirect('/')
    data = {
        "f_name": request.form['f_name'],
        "l_name": request.form['l_name'],
        "address": request.form['address'],
        "email": request.form['email'],
        "payment": request.form['payment'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Customer.create(data)
    session['customer_id'] = id
    return redirect('/dashboard')


@ app.route("/account")
def edit_customer():
    if 'customer_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['customer_id']
    }
    customer = Customer.get_one(data)

    return render_template("account.html", customer=customer)


@ app.route("/update", methods=["POST"])
def update():
    if 'customer_id' not in session:
        return redirect('/logout')
    if not Customer.validate_register(request.form):
        return redirect('/account')
    data = {
        "f_name": request.form['f_name'],
        "l_name": request.form['l_name'],
        "address": request.form['address'],
        "email": request.form['email'],
        "payment": request.form['payment'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    Customer.update(data)
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

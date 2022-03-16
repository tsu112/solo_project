from flask import render_template, redirect, request, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.product import Product
from flask_app.models.customer import Customer

from flask import flash
bcrypt = Bcrypt(app)


@ app.route("/check_out")
def check_out():
    if 'customer_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['customer_id']
    }
    customer = Customer.get_one(data)

    return render_template("checkout.html", customer=customer)


@app.route('/purchase', methods=['POST'])
def purchase():
    if 'customer_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/check_out')
    data = {
        "customers_id": session["customer_id"],
        "wood": request.form['wood'],
        "thickness": request.form['thickness'],
        "description": request.form['description']
    }
    Product.create(data)
    return redirect("/dashboard")


@ app.route("/orders")
def checkout():
    if 'customer_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['customer_id']
    }
    customer = Customer.get_one(data)
    product = Product.get_by_cust_id(data)
    return render_template("orders.html", customer=customer, product=product)


@ app.route("/cancel_product/<int:num>")
def cancel_product(num):
    data = {
        "id": num
    }
    Product.cancel(data)
    return redirect("/orders")

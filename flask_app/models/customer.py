from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Customer:
    db = "my_solo"

    def __init__(self, data):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.password = data['password']
        self.address = data['address']
        self.email = data['email']
        self.payment = data['payment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO customers (f_name, l_name, password, address, email, payment) VALUES (%(f_name)s, %(l_name)s, %(password)s, %(address)s, %(email)s, %(payment)s);"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        return results

    @classmethod
    def get_cust_by_email(cls, data):
        query = "SELECT * FROM customers WHERE customers.email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM customers WHERE customers.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE customers SET f_name= %(f_name)s, l_name= %(l_name)s, address= %(address)s, email= %(email)s, payment= %(payment)s, updated_at=NOW() WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @ staticmethod
    def validate_register(customer):
        is_valid = True
        query = "SELECT * FROM customers WHERE email = %(email)s;"
        results = connectToMySQL(
            "my_solo").query_db(query, customer)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(customer['email']):
            flash("Invalid email!", "register")
            is_valid = False
        if len(customer['email']) < 1:
            flash("Must enter email!", "register")
            is_valid = False
        if len(customer['f_name']) < 3:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(customer['l_name']) < 3:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(customer['address']) < 10:
            flash("Address must be at least 35 characthers long")
            is_valid = False
        if len(customer['payment']) < 4:
            flash("Payment must be at least 4 characthers long")
            is_valid = False
        if len(customer['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if customer['password'] != customer['con_pass']:
            flash("Passwords don't match", "register")
        return is_valid

    # @ staticmethod
    # def validate_update(customer):
    #     if not EMAIL_REGEX.match(customer['email']):
    #         flash("Invalid email!", "register")
    #         is_valid = False
    #     if len(customer['email']) < 1:
    #         flash("Must enter email!", "register")
    #         is_valid = False
    #     if len(customer['f_name']) < 3:
    #         flash("First name must be at least 2 characters", "register")
    #         is_valid = False
    #     if len(customer['l_name']) < 3:
    #         flash("Last name must be at least 2 characters", "register")
    #         is_valid = False
    #     if len(customer['address']) < 10:
    #         flash("Address must be at least 35 characthers long")
    #         is_valid = False
    #     if len(customer['payment']) < 4:
    #         flash("Payment must be at least 4 characthers long")
    #         is_valid = False
    #     if len(customer['password']) < 8:
    #         flash("Password must be at least 8 characters", "register")
    #         is_valid = False
    #     if customer['password'] != customer['con_pass']:
    #         flash("Passwords don't match", "register")
    #     return is_valid

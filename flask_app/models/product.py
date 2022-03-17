from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Product:
    db = "my_solo"

    def __init__(self, data):
        self.id = data['id']
        self.wood = data['wood']
        self.thickness = data['thickness']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.customers_id = data['customers_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO products (wood, thickness, description, customers_id) VALUES (%(wood)s, %(thickness)s, %(description)s, %(customers_id)s)"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        return results

    @classmethod
    def get_by_cust_id(cls, data):
        query = "SELECT * FROM products WHERE customers_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        list = []
        for row in results:
            list.append(cls(row))
        return list

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        results = connectToMySQL(
            cls.db).query_db(query, data)
        this_product = cls(results[0])
        return this_product

    @classmethod
    def cancel(cls, data):
        query = "DELETE FROM products WHERE id=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE products SET wood= %(wood)s, thickness= %(thickness)s, description= %(description)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @ staticmethod
    def validate_product(product):
        is_valid = True
        if len(product['wood']) < 1:
            flash("Please choose wood type!")
            is_valid = False
        if len(product['thickness']) < 1:
            flash("Thickness amount needed!")
            is_valid = False
        if len(product['description']) < 3:
            flash("Input at least 3 letters!")
            is_valid = False
        return is_valid

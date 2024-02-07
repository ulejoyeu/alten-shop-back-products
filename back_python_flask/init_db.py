import json, os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import Product

products_file = open('products.json', 'r')
products = json.load(products_file)['data']
products_file.close()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modele de donneees : Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), default='')
    name = db.Column(db.String(255), default='')
    description = db.Column(db.String(255), default='')
    price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Integer, default=0)
    inventoryStatus = db.Column(db.String(255), default='')
    category = db.Column(db.String(255), default='')
    image = db.Column(db.String(255), default='')
    rating = db.Column(db.Integer, default=0)

    def __init__(self, code, name, description, price, quantity, inventoryStatus, category, image, rating):
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.inventoryStatus = inventoryStatus
        self.category = category
        self.image = image
        self.rating = rating

with app.app_context():
    db.create_all()

# Schema : ProductSchema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'code', 'name', 'description', 'price', 'quantity', 'inventoryStatus', 'category', 'image', 'rating')


@app.get('/initdb')
def init_db():
    for product in products:
        new_product = Product(
            product['code'],
            product['name'],
            product['description'],
            product['price'],
            product['quantity'],
            product['inventoryStatus'],
            product['category'],
            product['image'],
            product['rating']
        )

        db.session.add(new_product)
        db.session.commit()
    return 'success', 200

# Run server
if __name__ == '__main__':
    app.run(debug=True)


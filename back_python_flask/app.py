from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SWAGGER'] = {'title': 'Swagger-UI', 'uiversion': 2}
# Base de donnees
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

# Swagger config
swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/swagger/'
}
swagger = Swagger(app, config=swagger_config)


# Init db et marshmallow
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

# with app.app_context():
#     db.create_all()

# Schema : ProductSchema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'code', 'name', 'description', 'price', 'quantity', 'inventoryStatus', 'category', 'image', 'rating')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Routes

# Get all products
@app.get('/products')
def get_products():
    """
    ---
    description: Get all products
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              code:
                type: string
              name:
                type: string
              description:
                type: string
              price:
                type: number
                format: float
              quantity:
                type: integer
              inventoryStatus:
                type: string
              category:
                type: string
              image:
                type: string
              rating:
                type: integer
    """
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return products_schema.jsonify(result), 200

# Create new product
@app.post('/products')
def create_product():
    """
    ---
    description: Create a new product
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            code:
              type: string
            name:
              type: string
            description:
              type: string
            price:
              type: number
              format: float
            quantity:
              type: integer
            inventoryStatus:
              type: string
            category:
              type: string
            image:
              type: string
            rating:
              type: integer
    responses:
      201:
        description: New product created
        schema:
          type: object
          properties:
            id:
              type: integer
            code:
              type: string
            name:
              type: string
            description:
              type: string
            price:
              type: number
              format: float
            quantity:
              type: integer
            inventoryStatus:
              type: string
            category:
              type: string
            image:
              type: string
            rating:
              type: integer
    """
    code = request.json['code']
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    inventoryStatus = request.json['inventoryStatus']
    category = request.json['category']
    if 'image' in request.json:
        image = request.json['image']
    else:
        image = ''
    if 'rating' in request.json:
        rating = request.json['rating']
    else:
        rating = 0

    new_product = Product(code, name, description, price, quantity, inventoryStatus, category, image, rating)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201

# Find product by id
@app.get('/products/<id>')
def get_product(id):
    """
    ---
    description: Get a product by its id
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: id of the product to be searched
    responses:
      200:
        description: Found the product
        schema:
          type: object
          properties:
            id:
              type: integer
            code:
              type: string
            name:
              type: string
            description:
              type: string
            price:
              type: number
              format: float
            quantity:
              type: integer
            inventoryStatus:
              type: string
            category:
              type: string
            image:
              type: string
            rating:
              type: integer
      404:
        description: Product not found
    """
    product = Product.query.get(id)
    if product is None:
        abort(404)

    return product_schema.jsonify(product)
    
# Update product
@app.patch('/products/<id>')
def update_product(id):
    """
    ---
    description: Update an existing product retrieved by its id
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: id of the product to be updated
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            code:
              type: string
            name:
              type: string
            description:
              type: string
            price:
              type: number
              format: float
            quantity:
              type: integer
            inventoryStatus:
              type: string
            category:
              type: string
            image:
              type: string
            rating:
              type: integer
    responses:
      200:
        description: Existing product has been updated
        schema:
          type: object
          properties:
            id:
              type: integer
            code:
              type: string
            name:
              type: string
            description:
              type: string
            price:
              type: number
              format: float
            quantity:
              type: integer
            inventoryStatus:
              type: string
            category:
              type: string
            image:
              type: string
            rating:
              type: integer
      404:
        description: Product not found
    """
    product = Product.query.get(id)
    if product is None:
        abort(404)

    code = request.json['code']
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    inventoryStatus = request.json['inventoryStatus']
    category = request.json['category']
    if 'image' in request.json:
        image = request.json['image']
    else:
        image = ''
    if 'rating' in request.json:
        rating = request.json['rating']
    else:
        rating = 0

    product.code = code
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    product.inventoryStatus = inventoryStatus
    product.category = category
    product.image = image
    product.rating = rating

    db.session.commit()

    return product_schema.jsonify(product), 200

# Delete a product
@app.delete('/products/<id>')
def delete_product(id):
    """
    ---
    description: Delete a product by its id
    parameters:
      - name: id
        in: path
        required: true
        description: id of the product to be deleted
    responses:
      200:
        description: Product has been successfully deleted
      404:
        description: Product has not been found
    """
    product = Product.query.get(id)
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': f'Product with id {id} has been successfully deleted'}), 200


# Run server
if __name__ == '__main__':
    app.run(debug=True)

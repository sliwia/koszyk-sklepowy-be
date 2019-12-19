# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), unique=True)
  photo = db.Column(db.String(300))
  price = db.Column(db.Float)
  category = db.Column(db.String(200))
  discount = db.Column(db.Boolean)
  discountValue = db.Column(db.Float)

  def __init__(self, name, photo, price, category, discount, discountValue):
    self.name = name
    self.photo = photo
    self.price = price
    self.category = category
    self.discount = discount
    self.discountValue = discountValue

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'photo', 'price', 'category', 'discount', 'discountValue')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
  name = request.json['name']
  photo = request.json['photo']
  price = request.json['price']
  category = request.json['category']
  discount = request.json['discount']
  discountValue = request.json['discountValue']

  new_product = Product(name, photo, price, category, discount, discountValue)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  photo = request.json['photo']
  price = request.json['price']
  category = request.json['category']
  discount = request.json['discount']
  discountValue = request.json['discountValue']

  product.name = name
  product.photo = photo
  product.price = price
  product.category = category
  product.discount = discount
  product.discountValue = discountValue


  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
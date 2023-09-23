#Shon Bennett 
#CMSC 455 Assignment 2 Product Service

import os
from flask import Flask, jsonify, request
import requests

# this creates a Flask web app object called app; initailized with name of current module (makes the root path of the app)  
app = Flask(__name__)

#Sample inventory to begin with (a list of dictionaries)
products = [
    {"product_id":1, "name":"Nintendo Switch", "price":299, "quantity":20},
    {"product_id":2, "name":"Pork Chops", "price":13, "quantity":5},
    {"product_id":3, "name":"Chicken", "price":8, "quantity":10},
    {"product_id":4, "name":"Play Station 5", "price":500, "quantity":3}
]

# Endpoint gets all products in inventory
@app.route('/products', methods=['GET'])
def get_all_products():
    app.logger.info("Getting all product information now")
    return jsonify({"Products": products})

#Endpoint gets product specified by product_id 
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product["product_id"] == product_id), None)
    if product:
        return jsonify({"product":product})
    else:
        return jsonify({"error": "Product not found (Shon)"}), 404

#Endpoint adds a specified amount to the user's cart while taking the specified amount away from the product service's inventory  
@app.route('/products', methods=['POST']) 
def add_product():
    new_product = {
        "product_id" : len(products) + 1,
        "name" : request.json.get('name'),
        "price" : request.json.get('price'),
        "quantity" : request.json.get('quantity')
    }
    #adds new product to the array 
    products.append(new_product)
    
    new_product_index = new_product['product_id'] - 1
    old_product_index = 0
    for x in range(0, len(products)): 
        if products[x]['name'] == new_product['name'] and x != new_product_index:
            products[x]['quantity'] = new_product['quantity']
            products.pop(new_product_index)
            return jsonify({"message": "Product added", "product": new_product}), 201

    #will return a JSON representation of the new Product object we created
    return jsonify({"message": "Product added", "product": new_product}), 201

if __name__ == '__main__':
    app.run(debug=True)
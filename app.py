from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

#Testing

@app.route('/ping')
def ping():
    return jsonify({'message':'pong'})

#####################################

@app.route('/products')
def getProducts():
    return jsonify({
        'message': "Product's List", 
        "products" : products
        })

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        return jsonify({"products": productsFound[0]})
    return jsonify({
        "message": "Product Not Found!!!"
    })

@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name" : request.json['name'],
        "price" : request.json['price'],
        "quantity" : request.json['quantity']
    }
    products.append(new_product)
    return jsonify({
        "Message": "Product Added Successfully",
        "Products": products
    })

@app.route('/products/<string:product_name>', methods = ['PUT'])
def updateProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "Message" : "Product Update Successfully",
            "Product" : productsFound[0]
        })
    return jsonify({
        "Message": "Product Not Found"
    })

@app.route('/products/<string:product_name>', methods = ['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            "Message":"Product Deleted Successfully",
            "Products": products
        })
    return jsonify({
        "Message":"Product Not Found"
    })
    
if __name__ == "__main__":
    app.run(debug=True, port = 4000)
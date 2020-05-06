#Import modules
from flask import Flask,request,jsonify
from products import products

#Save app value
app = Flask('__name__')

#Route to show product list
@app.route('/products', methods = ['GET'])
def showProducts():
    return jsonify({
        "Product List": products
    })

#Route to show one product from product list by it name
@app.route('/products/<string:product_name>', methods = ['GET'])
def showProduct(product_name):
    #Save in a variable called ProductFound a list with product name equal to id from url
    ProductFound = [product for product in products if product['name'] == product_name]
    #If there one product in the list
    if len(ProductFound) > 0:
        #Return it in JSON format 
        return jsonify({"Product Found": ProductFound[0]})
    #If there are not any, show a error message
    return jsonify({"Message " : "Product Not Found"})

@app.route('/products/<string:product_name>', methods = ['PUT'])
def editProduct(product_name):
    ProductFound = [product for product in products if product['name'] == product_name]
    if len(ProductFound) > 0:
        #In a ProductFound list in their properties, save json format received from client side with their properties
        ProductFound[0]['name'] = request.json['name']
        ProductFound[0]['price'] = request.json['price']
        ProductFound[0]['quantity'] = request.json['quantity']

        return jsonify({
            "Message": "Product " +  product_name + " Was Updated Successfully", 
            "Products List" : products
            })
    return jsonify({"Message " : "Product Not Found"})

@app.route('/products/<string:product_name>', methods = ['DELETE'])
def deleteProduct(product_name):
    ProductFound = [product for product in products if product['name'] == product_name]
    if len(ProductFound)  > 0:
        #from list products, using "remove property" inside parenthesis fist product found in the list ProductFound
        products.remove(ProductFound[0])

        return jsonify({
            "Message": "Product " + product_name + " Was Deleted Successfully",
            "Product List": products
        })        
    return jsonify({"Message " : "Product Not Found"})

@app.route('/products', methods = ['POST'])
def addProduct():
    #Create "new_product variable" and their properties by client side
    new_product = {
      "name": request.json['name'],
      "price": request.json['price'],
      "quantity": request.json['quantity']    
    }
    #Using "append" method, add a new product from variable "new_product"
    products.append(new_product)
    return jsonify({
        "Message": "Product " + request.json['name'] + " Was Added Successfully", 
        "Products" : products
    })

#If program is luaching like main
if __name__ == "__main__":
    #Run program in debug mode
    app.run(debug = True)
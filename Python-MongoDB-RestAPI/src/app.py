#request = get and manipulate JSON objects
from flask import Flask, jsonify, request, Response

#Integrating PyMongo from flask_pymongo
from flask_pymongo import PyMongo

#encrypt data
# from werkzeug module in security property, import two functions, GPH: receive a string data and it encrypt, CPH: you can see the string data 
from werkzeug.security import generate_password_hash, check_password_hash
 #from one library in bson format turn the bson data from MongoDB in a JSON
from bson import json_util
#from bson library inside objectid property import ObjectId class, to turn MongoDB data in a JSON
from bson.objectid import ObjectId

app = Flask(__name__)

#def property called MONGO_URI -- from mongodb protocol, ip server and database name
app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'

#Pass connection to PyMongo
mongo = PyMongo(app)

#Creating route to create users
@app.route('/users',methods=['POST'])
def create_users():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        #get string and encrypt it after
        hashed_password = generate_password_hash(password)
        #Create id object generate for MongoDB by each data
        #mongo: run mongo
        #db: one database from mongodb
        #users: one collection called users
        id = mongo.db.users.insert(
            {
                'username': username,
                'password': hashed_password,
                'email': email
            }
        )
        #Client side response by each data created
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }
        return response
    else:
        #if API doesn't receive any data lauch not_found function
        return not_found()
    return {'message':'received'}

#Get user list
@app.route('/users',methods = ['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

#Get user
@app.route('/users/<id>',methods=['GET'])
def get_user(id):
    #inside mongo variable for connections, log in a database connected, log in a collection called users
    #Get "id" in string format so we must change to JSON fromat
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    #find_one : first data found
    #turning in a json format with class json_util()
    response = json_util.dumps(user)
    #return response : response in format string
    #Response class for turn string in a JSON with a header application/json
    return Response(response,mimetype = "application/json")

@app.route('/users/<id>',methods = ['DELETE'])
def delete_users(id):
    user = mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message':'user '+ id + ' was deleted Successfully'})
    return response

@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    #get each data in json
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    #if they exist
    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id' : ObjectId(id)}, 
        #set is for replace data for one new
        {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'user '+id+' was update successfully'})
        return response

#Creating a route for default errors
@app.errorhandler(404)
#Creating a function it will receive an error by default in None then it will be activated
def not_found(error=None):
    #save error message in a jsonify object for get their properties
    response = jsonify({
        #request.url return route (localhost/users)
        "message":"Resource Not Found " + request.url,
        "status":"404"
    })
    response.status_code = 404
    return response
if __name__ == "__main__":
    app.run(debug=True)
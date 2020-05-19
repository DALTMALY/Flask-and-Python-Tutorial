#flask
from flask import Flask,request,jsonify
#use commands for mongodb from python
from flask_pymongo import PyMongo, ObjectId
#server react
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pythonreactdb'
mongo = PyMongo(app)

CORS(app)

#define users collection
db = mongo.db.users

@app.route('/users',methods = ['POST'])
def createUser():
    #id for each data created in collection 'users'
    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    #ObjectId get id in mongo format
    return jsonify(str(ObjectId(id)))

@app.route('/users',methods = ['GET'])
def getUsers():
    #list to print in client side
    users = []
    #instance db with find method is each data in usets collection 
    for doc in db.find():
        #adding with append method to users
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route('/user/<id>',methods = ['GET'])
def getUser(id):
    user = db.find_one({'_id':ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/users/<id>',methods = ['DELETE'])
def deleteUser(id):
    db.delete_one({"_id":ObjectId(id)})
    return jsonify({"msg": "User deleted"})

@app.route('/users/<id>',methods = ['PUT'])
def editUser(id):
    db.update_one({"_id": ObjectId(id)},{'$set':{
         "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    }})

    return jsonify({"msg":"User Updated"})


if __name__ == "__main__":
    app.run(debug = True)
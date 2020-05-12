#render_template: render html, request: get data from html form, redirect: return function, url_for: return url from function called home
from flask import Flask, render_template, request, redirect, url_for
#sqlalchemy is a module which allow us to do consults from a database, in this case sqlite3
from flask_sqlalchemy import SQLAlchemy

#set app variable
app = Flask(__name__)
#doc sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
#variable for consult DB
db = SQLAlchemy(app)

#Create an object it will be a table for our database
class Task(db.Model):
    #properties for Task object
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

#In our first route, we've created a variable called 'tasks' which will do a consult to our database  
@app.route('/')
def home():
    #tasks saves all data from our database
    tasks = Task.query.all()
    #render_template send tasks variable to html doc for use throgh jinja2
    return render_template('index.html', tasks = tasks)

#We create a route called 'create-task' using method called POST for add new tasks
@app.route('/create-task',methods = ['POST'])
def create():
    #task variable gets an instance from Task object, Object Task gets parameters for their properties 'content', 'done'
    task = Task(content = request.form['content'], done = False)
    #db instance using 'session' for use 'add' method, inside add(parameter to add in database) in this case 'task' object 
    db.session.add(task)
    #finish our request with 'commit' method
    db.session.commit()
    #redirect call to function 'home' after, home does its thing
    return redirect(url_for('home'))

#We create a route called 'done' which gets an 'id' for each data from our database
@app.route('/done/<id>')
#get 'id' in the function called 'done'
def done(id):
    #We get 'id' by URL and we make it an Integer, .first() method is for specify the first data which coincide
    task = Task.query.filter_by(id=int(id)).first()
    #add in 'task' (each data from database) in 'done' parameter the value inverted
    task.done = not(task.done)
    #finish our request with 'commit' method
    db.session.commit()
    #redirect call to function 'home' after, home does its thing
    return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    #We get 'id' by URL and we make it an Integer, .delete() method is for delete the first data which coincide
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
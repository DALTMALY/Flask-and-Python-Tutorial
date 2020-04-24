from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/blog')
def blog():
    return 'This is the blog'

@app.route('/blog/<string:blog_id>')
def blog_page(blog_id):
    return 'This is the blog number ' + blog_id

if __name__ == "__main__":
    app.run()

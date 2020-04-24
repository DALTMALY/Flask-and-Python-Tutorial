from flask import Flask, render_template

app = Flask('__name__',template_folder='Lesson-5/templates')

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/blog')
def b():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run()
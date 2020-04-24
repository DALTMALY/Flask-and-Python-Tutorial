from flask import Flask, render_template

app = Flask('__name__', template_folder = 'Lesson-3/templates')

@app.route('/')
def hom():
    return render_template('blog.html', author = 'Bob')

if __name__ == "__main__":
    app.run()
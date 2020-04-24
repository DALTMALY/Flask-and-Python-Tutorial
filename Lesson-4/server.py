from flask import Flask,render_template

app = Flask('__name__', template_folder= 'Lesson-4/templates')

@app.route('/')
def dictionary():
    posts = [{'name':'Book',
        'author':'Charly'
    },{
        'name':'Book',
        'author':'Juan'
    }]
    return render_template('dictionary.html',sunny = True, posts = posts )

if __name__ == '__main__':
    app.run()
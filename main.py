from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(900))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    posts = Blog.query.all() 
    return render_template('displayBP.html', posts = posts)

@app.route('/posts', methods=['POST','GET'])
def posts():

    entry_id = int(request.form['p_id'])

    entry = Blog.query.get(11)
    return render_template('displayBP.html', entry=entry)

@app.route('/todos', methods=['POST', 'GET'])
def display():

    title_error = ''

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        print(title)
        print(body)
        if title == '' or body == '':
            title_error = "Do not leave title or body empty"
            return render_template('todos.html')

        new_entry = Blog(title, body)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/')


    return render_template('todos.html')


if __name__ == '__main__':
    app.run()
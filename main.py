from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'wtf'


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

    single_post_num = request.args.get('entry_id')
    single_post = Blog.query.get(single_post_num)

    body = single_post.body
    title = single_post.name

    return render_template('posts.html', body=body, title=title)

@app.route('/todos', methods=['POST', 'GET'])
def display():

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']

        if title == '' or body == '':

            flash("Do not leave title or body empty")

            return render_template('todos.html')
        else:
            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()

            new_id = new_entry.id

            return redirect('/posts?entry_id='+ str(new_id))


    return render_template('todos.html')

@app.route('/login')
def login():
    Username = request.form['Username']
    Password = request.form['Password']
    #if password == password:
    print(Username)
    print(Password)
    flash("Successful Logged In")
    return render_template('login.html')
    


if __name__ == '__main__':
    app.run()
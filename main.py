from flask import Flask, request, redirect, render_template, flash, session
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
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'))


    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class Account(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    db_Username = db.Column(db.String(120))
    db_Password = db.Column(db.String(120))
    post = db.relationship('Blog', backref='owner')

    def __init__(self, db_Username, db_Password):
        self.db_Username = db_Username
        self.db_Password = db_Password

@app.before_request
def require_login():
    allowed_routes = ['login', 'createAccount']
    if request.endpoint not in allowed_routes and 'Username' not in session:
        return redirect('/login')

@app.route('/allPosts')
def allPosts():
    posts = Blog.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/', methods=['POST', 'GET'])
def index():

    users = Account.query.all()
    for user in users:
        print(user.db_Username)
    posts = Blog.query.all()

    return render_template('displayBP.html', users = users)


@app.route('/singleUser', methods=['GET', 'POST'])
def singleUser():
    if request.method == 'GET':
        value = request.args.get('owner_id')
        posts = Blog.query.filter_by(owner_id=value)
        return render_template('singleUser.html', posts=posts)
    return render_template('singleUser.html')


@app.route('/posts', methods=['POST','GET'])
def posts():

    single_post_num = request.args.get('entry_id')
    print(single_post_num)
    single_post = Blog.query.get(single_post_num)
    print(single_post)
    body = single_post.body
    title = single_post.name
    print(body)
    return render_template('post.html', body=body, title=title)

@app.route('/todos', methods=['POST', 'GET'])

def display():

    if request.method == 'POST':
        print(session['Username'])

        title = request.form['title']
        body = request.form['body']
        owner = Account.query.filter_by(db_Username=session['Username']).first()
        print(owner)
        print(title)
        print(body)
        if title == '' or body == '':

            flash("Do not leave title or body empty")

            return render_template('todos.html')
        else:
            new_entry = Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()


            new_id = new_entry.id

            return redirect('/posts?entry_id='+ str(new_id))


    return render_template('todos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        Username = request.form['Username']
        Password = request.form['Password']

        db_Username = Account.query.all()

        name = Account.query.filter_by(db_Username=Username).first()
        
        if name is not None:
            
            password_acc = Account.query.get(name.id)
            password = password_acc.db_Password
            if Password == password:
                
                session['Username'] = name.db_Username
                print(session['Username'])
                flash("Successful Logged In")
                return redirect('/todos')         
                
            else:
                flash("Wrong Password")

        elif Username not in db_Username:
            flash("User Does Not Exist")

        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/createAccount', methods=['POST', 'GET'])
def createAccount():

    if request.method == 'POST':

        Username = request.form['Username']
        Password = request.form['Password']
        cPassword = request.form['cPassword']

        db_Username = Account.query.all()
        
        name = Account.query.filter_by(db_Username=Username).first()
        print(name)
        
        if len(Username) > 3:
            if name is None:
                if Password == cPassword and Password != '':
                    new_user = Account(Username, Password)
                    db.session.add(new_user)
                    db.session.commit()

                    new_user_id = new_user.id
                    flash("Account Created")
                    return redirect('/todos')
                else:
                    flash('passwords do not match or feilds left empty')
            else:
                flash('Username already exists')
        else:
            flash('longer')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['Username']
    return redirect('/')
    


if __name__ == '__main__':
    app.run()
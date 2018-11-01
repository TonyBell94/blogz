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

@app.route('/allPosts', methods=['GET', 'POST'])
def allPosts():

    posts = Blog.query.all()
    account = Account.query.all()
    all_posts = list()
    for post in posts:
        entry_id = post.id
        owner_id = post.owner_id
        user = Account.query.get(owner_id)

        title = post.name
        body = post.body
        username = user.db_Username

        all_posts.append((username,title,body,owner_id,entry_id))

    return render_template('posts.html', all_posts=all_posts)
    #names = Account.query.filter_by(id=owner_id).first()

    #print(names)
    #u_name = Account.query.get(name_num)
    
    
    #return render_template('posts.html', posts=posts, account=account, names=names,num_list=num_list)
@app.route('/', methods=['POST', 'GET'])
def index():

    users = Account.query.all()
    #posts = Blog.query.all()
    
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
    if request.method == 'POST':

        return render_template('post.html')

    elif request.method == 'GET':

        single_post_num = request.args.get('entry_id')
        user_name_num = request.args.get('owner_id')

        single_post = Blog.query.get(single_post_num)
        user_name_A = Account.query.get(user_name_num)

        user_name = user_name_A.db_Username
        body = single_post.body
        title = single_post.name

        return render_template('post.html', body=body, title=title, user_name=user_name, single_post=single_post)

@app.route('/todos', methods=['POST', 'GET'])

def display():

    if request.method == 'POST':
        print(session['Username'])

        title = request.form['title']
        body = request.form['body']
        owner = Account.query.filter_by(db_Username=session['Username']).first()
        print(owner)
        if title == '' or body == '':

            flash("Do not leave title or body empty")

            return render_template('todos.html')
        else:
            new_entry = Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()

            owner_id = new_entry.owner_id
            new_id = new_entry.id
            print('fucker')
            print(new_id)
            return redirect('/posts?entry_id='+ str(new_id)+'&owner_id='+str(owner_id))


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
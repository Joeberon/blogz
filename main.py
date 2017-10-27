from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:MYNEWPASS@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "182382138"


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog','/']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    userError = ""
    passwordError = ""
    vpError= ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username == "" or len(username) == 0:
            userError = "type your username."
        if len(password) == 0:
            passwordError = "Please type your password"
        if vpError != password:
            vpError="must be the same as your password."
        if userError or passwordError or vpError:
            return render_template('login.html',userError=userError,passwordError=passwordError)
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    userError = ""
    passwordError = ""
    vpError= ""
    userError = ""
    passwordError = ""
    vpError= ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
    
        if not existing_user:
            if username == "" or len(username) == 0:
                userError = "type your username."
            if len(password) == 0:
                passwordError = "Please type your password"
            if verify != password:
                vpError="must be the same as your password."
            if userError or passwordError or vpError:
                return render_template('signup.html',userError=userError,passwordError=passwordError,vpError=vpError)
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')


@app.route('/', methods = ['GET', 'POST'])
def index():
    userId= request.args.get('users')
    if userId:
        singUser = User.query.filter_by(id=userId).first()
        return render_template('index.html',singUser=singUser)
    users= User.query.all()
    return render_template('index.html', users=users)

    return render_template('index.html',)
@app.route('/blog', methods = ['GET','POST'])
def blogid():
    userId= request.args.get('users')
    blogid = request.args.get('id')
    if userId:
        blogs = Blog.query.filter_by(owner_id=userId).all()
        return render_template('singleUser.html',blogs=blogs)
 
    if blogid:
        singBlog = Blog.query.filter_by(id=blogid).first()
        return render_template('blogPost.html',singBlog=singBlog)
    blogs = Blog.query.all()
    return render_template('cool.html',blogs=blogs)


@app.route('/newpost', methods = ['GET','POST'])
def newpost():
    titleError = ""
    bodyError = ""
    owner = User.query.filter_by(username=session['username']).first()
    
    if request.method == 'POST':
        title = request.form['Title:']
        body = request.form['body']
        if title == "" or len(title) == 0:
            titleError = "Please write a title."
        if len(body) == 0:
            bodyError = "Please write a body."
        if titleError or bodyError:
            return render_template('newpost.html',titleError=titleError,bodyError=bodyError)
        newBlog = Blog(title,body,owner)
        db.session.add(newBlog)
        db.session.commit()
        return redirect("/?id="+ str(newBlog.id))
    return render_template('newpost.html')


@app.route('/blogPost', methods = ['GET', 'POST'])
def blogPost():
   
    blogPost = request.args.get(id)
    return render_template('blogPost.html',blogPost=blogPost) 

if __name__ == '__main__':
    app.run()




    
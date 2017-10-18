from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MYNEWPASS@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self,title,body):
        self.title=title
        self.body=body
    #goes to home page title to link to seperate page. request.args.get(id)

@app.route('/', methods = ['GET','POST'])
def index():
    
    blogid = request.args.get('id')
    if blogid:
        singBlog = Blog.query.filter_by(id=blogid).first()
        return render_template('blogPost.html',singBlog=singBlog)
    blogs = Blog.query.all()
    return render_template('cool.html',blogs=blogs)

#this creates new pages and checks for errors. though its not checking any errors for body
@app.route('/newpost', methods = ['GET','POST'])
def newpost():
    titleError = ""
    bodyError = ""


    if request.method == 'POST':
        title = request.form['Title:']
        body = request.form['body']
        
        
        if title == "" or len(title) == 0:
            titleError = "Please write a title."
        if len(body) == 0:
            bodyError = "Please write a body."
        if titleError or bodyError:
            return render_template('newpost.html',titleError=titleError,bodyError=bodyError)
        newBlog = Blog(title,body)
        db.session.add(newBlog)
        db.session.commit()
        return redirect("/?id="+ str(newBlog.id))
    return render_template('newpost.html')

#Todo= make this code activate individual blog titles.
@app.route('/blogPost', methods = ['GET', 'POST'])
def blogPost():
   
    blogPost = reuqest.args.get(id)
    return render_template('blogPost.html',blogPost=blogPost) 
if __name__ == '__main__':
    app.run()




    
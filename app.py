from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somethingsecret'

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/view_all')
def view_all():
    posts = Post.query.all()
    return render_template('view_all.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('view_all'))
    
    return render_template('add.html')

@app.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    post = Post.query.get_or_404(id)
    return render_template('view.html', post=post)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('view_all'))
    return render_template('edit.html', post=post)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('view_post'))
    return render_template('addpost.html')

@app.route('/view_post')
def view_post():
    posts = Post.query.all()
    return render_template('viewpost.html', posts=posts)

@app.route('/view/<int:id>')
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
        return redirect(url_for('view_post'))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('view_post'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

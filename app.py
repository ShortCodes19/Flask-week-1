from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, nullable=True)


@app.route("/")
def hello_world():
    return render_template('base.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        content = request.form.get('content')
        
        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('add'))

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
     
        print(new_post.created_at)
        return redirect(url_for('view_all'))
    return render_template('add.html')

@app.route('/view_all')
def view_all():
    search = request.args.get('search', '')
    if search:
        posts = Post.query.filter(or_(Post.title.contains(search), Post.content.contains(search))).order_by(Post.created_at.desc()).all()
    else:
        posts = Post.query.order_by(Post.created_at.desc()).all()
    
    
    # Add relative_time to each post
    for post in posts:
        diff = datetime.now() - post.created_at
        if diff.days == 0:
            minutes = diff.seconds // 60
            if minutes < 60:
                post.relative_time = f"{minutes} {'min' if minutes == 1 else 'mins'} ago"
            else:
                hours = minutes // 60
                post.relative_time = f"{hours} {'hour' if hours == 1 else 'hours'} ago"
        else:
            post.relative_time = post.created_at.strftime('%B %d, %Y, %I:%M %p')
        post.updated_relative = ""
        if post.updated_at:
            diff = datetime.now() - post.updated_at
            if diff.days == 0:
                minutes = diff.seconds // 60
                if minutes < 60:
                    post.updated_relative = f"{minutes} {'min' if minutes == 1 else 'mins'} ago"
                else:
                    hours = minutes // 60
                    post.updated_relative = f"{hours} {'hour' if hours == 1 else 'hours'} ago"
            else:
                post.relative_time = post.created_at.strftime('%B %d, %Y, %I:%M %p')
    return render_template('view_all.html', posts=posts, search=search)


@app.route('/view/<int:id>')
def view(id):
    post = Post.query.get_or_404(id)
    # Format timestamp for detail page
    diff = datetime.now() - post.created_at
    if diff.days == 0:
        minutes = diff.seconds // 60
        if minutes < 60:
            post.relative_time = f"{minutes} {'min' if minutes == 1 else 'mins'} ago"
        else:
            hours = minutes // 60
            post.relative_time = f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    else:
        post.relative_time = post.created_at.strftime('%B %d, %Y, %I:%M %p')
        post.updated_relative = ""
        if post.updated_at:
            diff = datetime.now() - post.updated_at
            if diff.days == 0:
                minutes = diff.seconds // 60
                if minutes < 60:
                    post.updated_relative = f"{minutes} {'min' if minutes == 1 else 'mins'} ago"
                else:
                    hours = minutes // 60
                    post.updated_relative = f"{hours} {'hour' if hours == 1 else 'hours'} ago"
            else:
                post.relative_time = post.created_at.strftime('%B %d, %Y, %I:%M %p')
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

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('view_all'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
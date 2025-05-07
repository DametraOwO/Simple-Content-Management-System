from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    contents = Content.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', contents=contents)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/content/create', methods=['GET', 'POST'])
@login_required
def create_content():
    if request.method == 'POST':
        content = Content(
            title=request.form['title'],
            platform=request.form['platform'],
            status=request.form['status'],
            date=request.form['date'],
            user_id=current_user.id
        )
        db.session.add(content)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('content_form.html', action='Create')

@app.route('/content/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_content(id):
    content = Content.query.get_or_404(id)
    if request.method == 'POST':
        content.title = request.form['title']
        content.platform = request.form['platform']
        content.status = request.form['status']
        content.date = request.form['date']
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('content_form.html', action='Edit', content=content)

@app.route('/content/delete/<int:id>', methods=['POST'])
@login_required
def delete_content(id):
    content = Content.query.get_or_404(id)
    db.session.delete(content)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/content-board')
@login_required
def content_board():
    return render_template('content_board.html')

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@app.route('/contents')
@login_required
def contents():
    contents = Content.query.filter_by(user_id=current_user.id).all()
    return render_template('contents.html', contents=contents)

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    from werkzeug.security import check_password_hash
    posts_count = Content.query.filter_by(user_id=current_user.id).count()
    published_count = Content.query.filter_by(user_id=current_user.id, status='Published').count()
    drafts_count = Content.query.filter_by(user_id=current_user.id, status='Draft').count()
    if request.method == 'POST':
        username = request.form['username']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        # Update username
        current_user.username = username
        # Update password if provided and matches
        if new_password:
            if not check_password_hash(current_user.password, current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_new_password:
                flash('New passwords do not match.', 'danger')
            else:
                current_user.password = generate_password_hash(new_password)
                flash('Password updated successfully!', 'success')
        db.session.commit()
        flash('Profile updated!', 'success')
    return render_template('account.html', posts_count=posts_count, published_count=published_count, drafts_count=drafts_count)

@app.route('/test-link')
def test_link():
    return '<h1>Test Link Works!</h1>'

if __name__ == '__main__':
    if not os.path.exists('cms.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True) 
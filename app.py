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
    body = db.Column(db.Text, nullable=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
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
            user_id=current_user.id,
            body=request.form['body']
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
        content.body = request.form['body']
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
    contents = Content.query.order_by(Content.date.desc()).all()
    return render_template('content_board.html', contents=contents)

@app.route('/content/<int:id>')
@login_required
def view_content(id):
    content = Content.query.get_or_404(id)
    return render_template('view_content.html', content=content)

@app.route('/calendar')
@login_required
def calendar():
    events = [
        {"title": e.title, "start": e.date} for e in Event.query.filter_by(user_id=current_user.id).all()
    ]
    return render_template('calendar.html', events=events)

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

@app.route('/add-event', methods=['POST'])
@login_required
def add_event():
    title = request.form['title']
    date = request.form['date']
    event = Event(title=title, date=date, user_id=current_user.id)
    db.session.add(event)
    db.session.commit()
    return {"success": True}

if __name__ == '__main__':
    if not os.path.exists('cms.db'):
        with app.app_context():
            db.create_all()
            # Populate sample contents if empty
            if Content.query.count() == 0:
                sample_contents = [
                    Content(title='The Art of Bonsai', platform='Blog', status='Published', date='2025-05-07 17:39', user_id=1, body="Bonsai is the Japanese art of growing miniature trees in containers. It requires patience, skill, and a deep understanding of horticulture. This article explores the history, techniques, and philosophy behind bonsai cultivation."),
                    Content(title='Exploring Deep Sea Creatures', platform='Science', status='Published', date='2025-05-07 17:39', user_id=1, body="The deep sea is home to some of the most bizarre and fascinating creatures on Earth. From bioluminescent jellyfish to the mysterious giant squid, discover the wonders of the ocean's depths."),
                    Content(title='A Guide to Urban Gardening', platform='Lifestyle', status='Published', date='2025-05-07 17:39', user_id=1, body="Urban gardening is a growing trend among city dwellers. Learn how to start your own garden in small spaces, choose the right plants, and enjoy fresh produce year-round."),
                    Content(title='History of the Silk Road', platform='History', status='Published', date='2025-05-07 17:39', user_id=1, body="The Silk Road was an ancient network of trade routes that connected the East and West. It played a crucial role in cultural, commercial, and technological exchange for centuries."),
                    Content(title='Introduction to Origami', platform='Art', status='Published', date='2025-05-07 17:39', user_id=1, body="Origami, the art of paper folding, originated in Japan and has become popular worldwide. This guide covers basic folds, traditional models, and creative projects for all ages."),
                    Content(title='The Basics of Astronomy', platform='Science', status='Published', date='2025-05-07 17:39', user_id=1, body="Astronomy is the study of celestial objects and phenomena. Learn about stars, planets, galaxies, and the tools astronomers use to explore the universe."),
                    Content(title='How to Make Sourdough Bread', platform='Food', status='Published', date='2025-05-07 17:39', user_id=1, body="Sourdough bread is known for its tangy flavor and chewy texture. This article provides a step-by-step guide to making your own sourdough starter and baking delicious bread at home."),
                    Content(title='Wildlife of the Amazon Rainforest', platform='Nature', status='Published', date='2025-05-07 17:39', user_id=1, body="The Amazon rainforest is one of the most biodiverse places on Earth. Explore the unique animals and plants that inhabit this vast ecosystem."),
                    Content(title='Understanding Renewable Energy', platform='Technology', status='Published', date='2025-05-07 17:39', user_id=1, body="Renewable energy sources like solar, wind, and hydro are transforming the way we power our world. Discover the benefits and challenges of transitioning to clean energy."),
                    Content(title='The World of Competitive Chess', platform='Games', status='Published', date='2025-05-07 17:39', user_id=1, body="Chess is a game of strategy and intellect. This article delves into the world of competitive chess, famous grandmasters, and tips for improving your game."),
                    Content(title='Traveling in Scandinavia', platform='Travel', status='Published', date='2025-05-07 17:39', user_id=1, body="Scandinavia offers stunning landscapes, rich history, and vibrant cultures. Plan your next adventure with our guide to the best destinations in Norway, Sweden, and Denmark."),
                    Content(title='Basics of Digital Photography', platform='Photography', status='Published', date='2025-05-07 17:39', user_id=1, body="Digital photography has made capturing moments easier than ever. Learn about camera settings, composition, and editing techniques to take your photos to the next level."),
                    Content(title='The Science of Sleep', platform='Health', status='Published', date='2025-05-07 17:39', user_id=1, body="Sleep is essential for health and well-being. Explore the science behind sleep cycles, common disorders, and tips for getting a better night's rest."),
                    Content(title='Building Your First Birdhouse', platform='DIY', status='Published', date='2025-05-07 17:39', user_id=1, body="Birdhouses provide shelter for local wildlife and can be a fun DIY project. Follow our instructions to build a simple and effective birdhouse for your garden."),
                    Content(title='Learning Calligraphy', platform='Art', status='Published', date='2025-05-07 17:39', user_id=1, body="Calligraphy is the art of beautiful writing. This beginner's guide covers tools, basic strokes, and practice exercises to help you get started."),
                    Content(title='The Benefits of Meditation', platform='Wellness', status='Published', date='2025-05-07 17:39', user_id=1, body="Meditation can reduce stress, improve focus, and enhance overall well-being. Learn different meditation techniques and how to incorporate them into your daily routine."),
                    Content(title='Exploring Ancient Egypt', platform='History', status='Published', date='2025-05-07 17:39', user_id=1, body="Ancient Egypt is known for its pyramids, pharaohs, and rich mythology. Discover the fascinating history and culture of this ancient civilization."),
                    Content(title='Introduction to Coding with Python', platform='Technology', status='Published', date='2025-05-07 17:39', user_id=1, body="Python is a versatile programming language used in web development, data science, and more. This article introduces the basics of Python and how to write your first program."),
                ]
                db.session.bulk_save_objects(sample_contents)
                db.session.commit()
    app.run(debug=True) 
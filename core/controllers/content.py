from flask import Blueprint, request
from flask_login import login_required, current_user
from core.controllers.base import BaseController
from core.models.content import Content
from datetime import datetime

content_bp = Blueprint('content', __name__, url_prefix='/contents')
content_controller = BaseController(Content)

def initialize_dummy_contents(user_id):
    print("Memanggil initialize_dummy_contents, user_id:", user_id)
    sample_contents = [
        Content(
            title='The Art of Bonsai',
            platform='Blog',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Bonsai is the Japanese art of growing miniature trees in containers. It requires patience, skill, and a deep understanding of horticulture. This article explores the history, techniques, and philosophy behind bonsai cultivation."
        ),
        Content(
            title='Exploring Deep Sea Creatures',
            platform='Science',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="The deep sea is home to some of the most bizarre and fascinating creatures on Earth. From bioluminescent jellyfish to the mysterious giant squid, discover the wonders of the ocean's depths."
        ),
        Content(
            title='A Guide to Urban Gardening',
            platform='Lifestyle',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Urban gardening is a growing trend among city dwellers. Learn how to start your own garden in small spaces, choose the right plants, and enjoy fresh produce year-round."
        ),
        Content(
            title='History of the Silk Road',
            platform='History',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="The Silk Road was an ancient network of trade routes that connected the East and West. It played a crucial role in cultural, commercial, and technological exchange for centuries."
        ),
        Content(
            title='Introduction to Origami',
            platform='Art',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Origami, the art of paper folding, originated in Japan and has become popular worldwide. This guide covers basic folds, traditional models, and creative projects for all ages."
        ),
        Content(
            title='The Basics of Astronomy',
            platform='Science',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Astronomy is the study of celestial objects and phenomena. Learn about stars, planets, galaxies, and the tools astronomers use to explore the universe."
        ),
        Content(
            title='How to Make Sourdough Bread',
            platform='Food',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Sourdough bread is known for its tangy flavor and chewy texture. This article provides a step-by-step guide to making your own sourdough starter and baking delicious bread at home."
        ),
        Content(
            title='Wildlife of the Amazon Rainforest',
            platform='Nature',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="The Amazon rainforest is one of the most biodiverse places on Earth. Explore the unique animals and plants that inhabit this vast ecosystem."
        ),
        Content(
            title='Understanding Renewable Energy',
            platform='Technology',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Renewable energy sources like solar, wind, and hydro are transforming the way we power our world. Discover the benefits and challenges of transitioning to clean energy."
        ),
        Content(
            title='The World of Competitive Chess',
            platform='Games',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Chess is a game of strategy and intellect. This article delves into the world of competitive chess, famous grandmasters, and tips for improving your game."
        ),
        Content(
            title='Traveling in Scandinavia',
            platform='Travel',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Scandinavia offers stunning landscapes, rich history, and vibrant cultures. Plan your next adventure with our guide to the best destinations in Norway, Sweden, and Denmark."
        ),
        Content(
            title='Basics of Digital Photography',
            platform='Photography',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Digital photography has made capturing moments easier than ever. Learn about camera settings, composition, and editing techniques to take your photos to the next level."
        ),
        Content(
            title='The Science of Sleep',
            platform='Health',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Sleep is essential for health and well-being. Explore the science behind sleep cycles, common disorders, and tips for getting a better night's rest."
        ),
        Content(
            title='Building Your First Birdhouse',
            platform='DIY',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Birdhouses provide shelter for local wildlife and can be a fun DIY project. Follow our instructions to build a simple and effective birdhouse for your garden."
        ),
        Content(
            title='Learning Calligraphy',
            platform='Art',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Calligraphy is the art of beautiful writing. This beginner's guide covers tools, basic strokes, and practice exercises to help you get started."
        ),
        Content(
            title='The Benefits of Meditation',
            platform='Wellness',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Meditation can reduce stress, improve focus, and enhance overall well-being. Learn different meditation techniques and how to incorporate them into your daily routine."
        ),
        Content(
            title='Exploring Ancient Egypt',
            platform='History',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Ancient Egypt is known for its pyramids, pharaohs, and rich mythology. Discover the fascinating history and culture of this ancient civilization."
        ),
        Content(
            title='Introduction to Coding with Python',
            platform='Technology',
            status='Published',
            date='2025-05-07 17:39',
            user_id=user_id,
            body="Python is a versatile programming language used in web development, data science, and more. This article introduces the basics of Python and how to write your first program."
        )
    ]
    for content in sample_contents:
        content.save()
        print("Berhasil menyimpan:", content.title)

@content_bp.route('/')
@login_required
def index():
    print("==== MASUK FUNGSI INDEX CONTENTS ====")
    initialize_dummy_contents(current_user.id)
    all_contents = Content.query.order_by(Content.date.desc()).all()
    print('Jumlah konten di DB:', len(all_contents))
    for c in all_contents:
        print(c.title, c.user_id)
    return content_controller.render('content/index.html', contents=all_contents)

@content_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        content = Content(
            title=request.form['title'],
            platform=request.form['platform'],
            status=request.form['status'],
            date=request.form['date'],
            body=request.form['body'],
            user_id=current_user.id
        )
        content.save()
        content_controller.flash('Content created successfully!', 'success')
        return content_controller.redirect('content.index')
    
    return content_controller.render('content/form.html', action='Create')

@content_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    content = Content.get_by_id(id)
    if not content or content.user_id != current_user.id:
        content_controller.flash('Content not found or access denied', 'danger')
        return content_controller.redirect('content.index')
    
    if request.method == 'POST':
        content.update(
            title=request.form['title'],
            platform=request.form['platform'],
            status=request.form['status'],
            date=request.form['date'],
            body=request.form['body']
        )
        content_controller.flash('Content updated successfully!', 'success')
        return content_controller.redirect('content.index')
    
    return content_controller.render('content/form.html', content=content, action='Edit')

@content_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    content = Content.get_by_id(id)
    if content and content.user_id == current_user.id:
        content.delete()
        content_controller.flash('Content deleted successfully!', 'success')
    else:
        content_controller.flash('Content not found or access denied', 'danger')
    return content_controller.redirect('content.index')

@content_bp.route('/<int:id>')
@login_required
def view(id):
    content = Content.get_by_id(id)
    if not content or content.user_id != current_user.id:
        content_controller.flash('Content not found or access denied', 'danger')
        return content_controller.redirect('content.index')
    
    return content_controller.render('content/view.html', content=content)

@content_bp.route('/board')
@login_required
def board():
    contents = Content.get_published()
    return content_controller.render('content/board.html', contents=contents)

@content_bp.route('/generate_dummy', methods=['POST'])
@login_required
def generate_dummy():
    dummy_data = [
        {
            'title': 'The Art of Bonsai',
            'platform': 'Blog',
            'status': 'Published',
            'date': '2025-05-07 17:39',
            'body': 'Bonsai is the Japanese art of growing miniature trees in containers. It requires patience, skill, dan pemahaman hortikultura. Artikel ini membahas sejarah, teknik, dan filosofi bonsai.'
        },
        {
            'title': 'Exploring Deep Sea Creatures',
            'platform': 'Science',
            'status': 'Published',
            'date': '2025-05-07 17:39',
            'body': 'The deep sea is home to some of the most bizarre and fascinating creatures on Earth. From bioluminescent jellyfish to the mysterious giant squid, discover the wonders of the ocean.'
        },
        {
            'title': 'A Guide to Urban Gardening',
            'platform': 'Lifestyle',
            'status': 'Published',
            'date': '2025-05-07 17:39',
            'body': 'Urban gardening is a growing trend among city dwellers. Learn how to start your own garden in small spaces, choose the right plants, and enjoy fresh produce year-round.'
        },
        # ...tambahkan data lain sesuai kebutuhan...
    ]
    for data in dummy_data:
        content = Content(
            title=data['title'],
            platform=data['platform'],
            status=data['status'],
            date=data['date'],
            body=data['body'],
            user_id=current_user.id
        )
        content.save()
    content_controller.flash('Dummy contents created!', 'success')
    return content_controller.redirect('content.index') 
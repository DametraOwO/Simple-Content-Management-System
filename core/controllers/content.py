from flask import Blueprint, request
from flask_login import login_required, current_user
from core.controllers.base import BaseController
from core.models.content import Content

content_bp = Blueprint('content', __name__, url_prefix='/content')
content_controller = BaseController(Content)

@content_bp.route('/')
@login_required
def index():
    contents = Content.get_by_user(current_user.id)
    return content_controller.render('content/index.html', contents=contents)

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
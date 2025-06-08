from flask import Blueprint
from flask_login import login_required, current_user
from core.controllers.base import BaseController
from core.models.content import Content
from core.models.event import Event

dashboard_bp = Blueprint('dashboard', __name__)
dashboard_controller = BaseController()

@dashboard_bp.route('/')
@login_required
def index():
    # Get user's content statistics
    contents = Content.get_by_user(current_user.id)
    published_count = len([c for c in contents if c.status == 'Published'])
    draft_count = len([c for c in contents if c.status == 'Draft'])
    
    # Get upcoming events
    events = Event.get_upcoming()
    
    # Get recent contents
    recent_contents = Content.query.filter_by(user_id=current_user.id)\
        .order_by(Content.created_at.desc())\
        .limit(5)\
        .all()
    
    return dashboard_controller.render(
        'dashboard/index.html',
        contents=contents,
        published_count=published_count,
        draft_count=draft_count,
        events=events,
        recent_contents=recent_contents
    )

@dashboard_bp.route('/calendar')
@login_required
def calendar():
    events = Event.get_by_user(current_user.id)
    return dashboard_controller.render('dashboard/calendar.html', events=events)

@dashboard_bp.route('/account')
@login_required
def account():
    # Get user's content statistics
    contents = Content.get_by_user(current_user.id)
    published_count = len([c for c in contents if c.status == 'Published'])
    draft_count = len([c for c in contents if c.status == 'Draft'])
    
    return dashboard_controller.render(
        'dashboard/account.html',
        user=current_user,
        published_count=published_count,
        draft_count=draft_count
    ) 
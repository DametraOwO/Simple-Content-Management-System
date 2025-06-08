from flask import Blueprint
from flask_login import login_required, current_user
from core.controllers.base import BaseController
from core.models.content import Content
from core.models.user import User
from core.models.event import Event
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
dashboard_controller = BaseController()

@dashboard_bp.route('/')
@login_required
def index():
    # Get user's contents
    user_contents = Content.get_by_user(current_user.id)
    
    # Calculate content statistics
    total_contents = len(user_contents)
    published_contents = len([c for c in user_contents if c.status == 'Published'])
    draft_contents = len([c for c in user_contents if c.status == 'Draft'])
    
    # Get platform statistics
    platform_stats = {}
    for content in user_contents:
        platform = content.platform
        if platform not in platform_stats:
            platform_stats[platform] = 0
        platform_stats[platform] += 1
    
    # Get recent contents (last 5)
    recent_contents = user_contents[:5]
    
    # Get upcoming events (next 7 days)
    today = datetime.now()
    next_week = today + timedelta(days=7)
    upcoming_events = Event.query.filter(
        Event.date >= today,
        Event.date <= next_week
    ).order_by(Event.date.asc()).all()
    
    return dashboard_controller.render('dashboard/index.html',
        total_contents=total_contents,
        published_contents=published_contents,
        draft_contents=draft_contents,
        platform_stats=platform_stats,
        recent_contents=recent_contents,
        upcoming_events=upcoming_events
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
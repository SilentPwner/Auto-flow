from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html', title='لوحة التحكم')

@bp.route('/content-generator')
@login_required
def content_generator():
    return render_template('dashboard/content_generator.html', title='مولد المحتوى')

# ... صفحات فارغة للميزات الأخرى ...
@bp.route('/seo-optimizer')
@login_required
def seo_optimizer():
    return render_template('dashboard/placeholder.html', title='محسن SEO', page_name='محسن SEO')

@bp.route('/content-calendar')
@login_required
def content_calendar():
    return render_template('dashboard/placeholder.html', title='تقويم المحتوى', page_name='تقويم المحتوى')
    


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    # db.session.rollback() # قد تحتاج هذا في تطبيق حقيقي
    return render_template('errors/500.html'), 500
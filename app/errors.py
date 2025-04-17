from flask import Blueprint, render_template, current_app

bp = Blueprint('errors', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error('Server Error: %s', error)
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(429)
def too_many_requests(error):
    return render_template('errors/429.html'), 429 
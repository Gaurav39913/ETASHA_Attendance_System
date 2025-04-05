from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.auth.models import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Admin, User
from app import db

admin_bp = Blueprint('admin', __name__)

# Admin Login


@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Log out normal user automatically
        session.pop('username', None)
        session.pop('user_id', None)

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session.permanent = True  # optional: for auto-expire
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('admin_login.html')


# Admin Dashboard
@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('admin.admin_login'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


# Admin Logout
@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('admin.admin_login'))


# Delete User
@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('admin.admin_login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'info')
    return redirect(url_for('admin.admin_dashboard'))


# Edit User
@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'admin_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('admin.admin_login'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user.username = username
        if password:
            user.set_password(password)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin_edit_user.html', user=user)

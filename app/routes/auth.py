from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Log out admin automatically when a normal user logs in
        session.pop('admin_id', None)

        # Your user validation logic
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['user_id'] = user.id
            session.permanent = True  # optional: for auto-expire
            flash('Login Successful', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/delete_profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session:
        flash('You must be logged in to delete your profile', 'danger')
        return redirect(url_for('auth.login'))

    from app.models import User, Task

    user = User.query.get_or_404(session['user_id'])

    # Delete all tasks of the user
    Task.query.filter_by(user_id=user.id).delete()

    # Delete user
    db.session.delete(user)
    db.session.commit()

    # Clear session
    session.pop('username', None)
    session.pop('user_id', None)

    flash('Your profile and all tasks have been deleted!', 'info')
    return redirect(url_for('auth.login'))

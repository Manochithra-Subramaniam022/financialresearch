from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.message import EmailMessage
import os
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'error')
            return redirect(url_for('auth.signup'))
            
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'error')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, username=username, password_hash=generate_password_hash(password, method='scrypt'))

        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        flash('Username cannot be empty.', 'error')
        return redirect(url_for('settings'))

    existing_user = User.query.filter_by(username=username).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Username already exists.', 'error')
        return redirect(url_for('settings'))

    current_user.username = username

    if password:
        current_user.password_hash = generate_password_hash(password, method='scrypt')

    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('settings'))

def send_reset_email(user, token):
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg = EmailMessage()
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'noreply@researchportal.local'
    msg['To'] = user.email
    msg.set_content(f'''To reset your password, visit the following link:

{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
''')

    # Try sending via SMTP, fallback to console if unconfigured in development
    mail_server = os.environ.get('MAIL_SERVER')
    if mail_server:
        try:
            with smtplib.SMTP(mail_server, int(os.environ.get('MAIL_PORT', 587))) as server:
                if os.environ.get('MAIL_USE_TLS') == 'True':
                    server.starttls()
                if os.environ.get('MAIL_USERNAME'):
                    server.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        # Development fallback (Console preview)
        print("====== EMAIL DISPATCH PREVIEW ======")
        print(f"To: {user.email}")
        print(f"Subject: {msg['Subject']}")
        print(msg.get_content())
        print("====================================")

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        # We always display a success message to prevent email enumeration
        flash('If an account with that email exists, a password reset link has been sent.', 'success')
        
        if user:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(user.email, salt='reset-password')
            send_reset_email(user, token)
            
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='reset-password', max_age=3600) # 1 hour
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password or password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.reset_password', token=token))

        user = User.query.filter_by(email=email).first()
        if user:
            user.password_hash = generate_password_hash(password, method='scrypt')
            db.session.commit()
            flash('Your password has been securely updated. You may now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)

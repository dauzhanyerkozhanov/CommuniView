from flask import Blueprint, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400


    user = User.query.filter_by(username=data['username']).first()


    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return redirect(url_for('index'))
    else:
        return 'Invalid username or password', 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201


@auth_bp.route('/user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(username=current_user.username), 200


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

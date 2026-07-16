from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models.portfolio import Portfolio
from app import db
from datetime import datetime
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            name=data.get('name', data['email']),
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()
        
        portfolio = Portfolio(user_id=user.id)
        db.session.add(portfolio)
        
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'token': access_token,
            'userId': user.id,
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'token': access_token,
            'userId': user.id,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/google', methods=['POST'])
def google_login():
    try:
        data = request.get_json()
        
        user = User.query.filter_by(google_id=data.get('googleId')).first()
        
        if not user:
            user = User(
                name=data.get('name', 'Google User'),
                email=data.get('email'),
                google_id=data.get('googleId')
            )
            db.session.add(user)
            db.session.flush()
            
            portfolio = Portfolio(user_id=user.id)
            db.session.add(portfolio)
        
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'token': access_token,
            'userId': user.id,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
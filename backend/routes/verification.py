from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.verification import Verification
from app import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

verification_bp = Blueprint('verification', __name__)

UPLOAD_FOLDER = 'uploads/verification'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@verification_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_verification():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        verification = Verification.query.filter_by(user_id=user_id).first()
        
        if not verification:
            verification = Verification(user_id=user_id)
        
        verification.full_name = request.form.get('fullName')
        verification.date_of_birth = datetime.strptime(request.form.get('dateOfBirth'), '%Y-%m-%d').date()
        verification.twitter_handle = request.form.get('twitter')
        verification.discord_username = request.form.get('discord')
        verification.linkedin_url = request.form.get('linkedin')
        
        if 'idDocument' in request.files:
            file = request.files['idDocument']
            if file and allowed_file(file.filename):
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(f"{user_id}_{file.filename}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                verification.id_document_url = f"/uploads/verification/{filename}"
        
        verification.status = 'pending'
        verification.updated_at = datetime.utcnow()
        
        db.session.add(verification)
        db.session.commit()
        
        return jsonify({
            'message': 'Verification submitted successfully',
            'verification': verification.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@verification_bp.route('/status', methods=['GET'])
@jwt_required()
def get_verification_status():
    try:
        user_id = get_jwt_identity()
        verification = Verification.query.filter_by(user_id=user_id).first()
        
        if not verification:
            return jsonify({
                'status': 'not_started',
                'message': 'Verification not started'
            }), 200
        
        return jsonify({
            'status': verification.status,
            'verification': verification.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.forum import ForumThread, ForumResponse
from app import db
from datetime import datetime
from sqlalchemy import desc

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/threads', methods=['GET'])
def get_threads():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        threads = ForumThread.query.order_by(desc(ForumThread.created_at)).paginate(
            page=page, per_page=per_page
        )
        
        return jsonify({
            'threads': [thread.to_dict() for thread in threads.items],
            'total': threads.total,
            'pages': threads.pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@forum_bp.route('/threads', methods=['POST'])
@jwt_required()
def create_thread():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('title') or not data.get('content'):
            return jsonify({'error': 'Title and content required'}), 400
        
        thread = ForumThread(
            user_id=user_id,
            title=data['title'],
            content=data['content']
        )
        
        db.session.add(thread)
        db.session.commit()
        
        return jsonify({
            'message': 'Thread created successfully',
            'thread': thread.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@forum_bp.route('/threads/<thread_id>/responses', methods=['GET'])
def get_responses(thread_id):
    try:
        thread = ForumThread.query.get(thread_id)
        
        if not thread:
            return jsonify({'error': 'Thread not found'}), 404
        
        thread.views += 1
        db.session.commit()
        
        responses = ForumResponse.query.filter_by(thread_id=thread_id).order_by(
            ForumResponse.created_at
        ).all()
        
        return jsonify({
            'thread': thread.to_dict(),
            'responses': [response.to_dict() for response in responses]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@forum_bp.route('/threads/<thread_id>/responses', methods=['POST'])
@jwt_required()
def post_response(thread_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        thread = ForumThread.query.get(thread_id)
        if not thread:
            return jsonify({'error': 'Thread not found'}), 404
        
        if not data.get('content'):
            return jsonify({'error': 'Content required'}), 400
        
        response = ForumResponse(
            thread_id=thread_id,
            user_id=user_id,
            content=data['content']
        )
        
        db.session.add(response)
        db.session.commit()
        
        return jsonify({
            'message': 'Response posted successfully',
            'response': response.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@forum_bp.route('/contributors/top', methods=['GET'])
def get_top_contributors():
    try:
        from sqlalchemy import func
        
        top_users = db.session.query(
            User.id,
            User.name,
            func.count(ForumResponse.id).label('post_count')
        ).outerjoin(ForumResponse).group_by(User.id).order_by(
            desc(func.count(ForumResponse.id))
        ).limit(10).all()
        
        contributors = [
            {
                'id': user[0],
                'name': user[1],
                'postCount': user[2] or 0
            }
            for user in top_users
        ]
        
        return jsonify({'contributors': contributors}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
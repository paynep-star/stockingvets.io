from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.portfolio import Portfolio, Stock
from app import db

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/', methods=['GET'])
@jwt_required()
def get_portfolio():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        portfolio_data = user.portfolio.to_dict()
        portfolio_data['verified'] = user.verified
        
        return jsonify(portfolio_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/add', methods=['POST'])
@jwt_required()
def add_stock():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        data = request.get_json()
        
        existing_stock = Stock.query.filter_by(
            portfolio_id=user.portfolio.id,
            symbol=data['symbol'].upper()
        ).first()
        
        if existing_stock:
            existing_stock.shares += data.get('shares', 0)
            existing_stock.current_price = data.get('currentPrice', existing_stock.current_price)
        else:
            stock = Stock(
                portfolio_id=user.portfolio.id,
                symbol=data['symbol'].upper(),
                shares=data.get('shares', 1),
                purchase_price=data.get('purchasePrice', 0),
                current_price=data.get('currentPrice', data.get('purchasePrice', 0))
            )
            db.session.add(stock)
        
        db.session.commit()
        
        return jsonify({'message': 'Stock added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/<symbol>', methods=['DELETE'])
@jwt_required()
def remove_stock(symbol):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        stock = Stock.query.filter_by(
            portfolio_id=user.portfolio.id,
            symbol=symbol.upper()
        ).first()
        
        if not stock:
            return jsonify({'error': 'Stock not found'}), 404
        
        db.session.delete(stock)
        db.session.commit()
        
        return jsonify({'message': 'Stock removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
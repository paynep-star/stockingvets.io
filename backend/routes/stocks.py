from flask import Blueprint, request, jsonify
from models.portfolio import Stock

stocks_bp = Blueprint('stocks', __name__)

MOCK_PRICES = {
    'AAPL': 150.25,
    'GOOGL': 140.50,
    'MSFT': 380.75,
    'TSLA': 242.30,
    'AMZN': 175.50,
}

@stocks_bp.route('/<symbol>/price', methods=['GET'])
def get_stock_price(symbol):
    try:
        symbol = symbol.upper()
        price = MOCK_PRICES.get(symbol, 100.0)
        
        return jsonify({
            'symbol': symbol,
            'currentPrice': price,
            'timestamp': 'now'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stocks_bp.route('/<symbol>/history', methods=['GET'])
def get_stock_history(symbol):
    try:
        symbol = symbol.upper()
        days = request.args.get('days', 30, type=int)
        
        history = [
            {'date': f'2024-01-{i:02d}', 'close': 100 + i * 0.5}
            for i in range(1, min(days, 30))
        ]
        
        return jsonify({
            'symbol': symbol,
            'history': history
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
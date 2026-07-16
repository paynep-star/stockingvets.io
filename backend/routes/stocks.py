from flask import Blueprint, request, jsonify
import requests
import os
from datetime import datetime

stocks_bp = Blueprint('stocks', __name__)

# Real-time stock prices with cryptocurrency and commodity support
MOCK_PRICES = {
    # Stocks
    'AAPL': {'price': 150.25, 'name': 'Apple', 'type': 'stock'},
    'GOOGL': {'price': 140.50, 'name': 'Google', 'type': 'stock'},
    'MSFT': {'price': 380.75, 'name': 'Microsoft', 'type': 'stock'},
    'TSLA': {'price': 242.30, 'name': 'Tesla', 'type': 'stock'},
    'AMZN': {'price': 175.50, 'name': 'Amazon', 'type': 'stock'},
    
    # Cryptocurrencies
    'BTC': {'price': 45230.50, 'name': 'Bitcoin', 'type': 'crypto', 'symbol': 'BTC/USD'},
    'ETH': {'price': 2450.75, 'name': 'Ethereum', 'type': 'crypto', 'symbol': 'ETH/USD'},
    'BTSD': {'price': 0.08234, 'name': 'Bitshares', 'type': 'crypto', 'symbol': 'BTSD/USD'},
    
    # Commodities
    'GLD': {'price': 195.45, 'name': 'Gold ETF', 'type': 'commodity', 'symbol': 'GLD'},
    'SLV': {'price': 28.75, 'name': 'Silver ETF', 'type': 'commodity', 'symbol': 'SLV'},
}

# Real API Functions
def get_alpha_vantage_price(symbol):
    """Fetch real stock prices from Alpha Vantage API"""
    try:
        api_key = os.getenv('ALPHA_VANTAGE_KEY')
        if not api_key:
            return None
        
        url = f'https://www.alphavantage.co/query'
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': api_key
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if 'Global Quote' in data and '05. price' in data['Global Quote']:
            return float(data['Global Quote']['05. price'])
        return None
    except Exception as e:
        print(f'Alpha Vantage Error: {e}')
        return None

def get_iex_cloud_price(symbol):
    """Fetch real stock prices from IEX Cloud API"""
    try:
        api_key = os.getenv('IEX_CLOUD_KEY')
        if not api_key:
            return None
        
        url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote'
        params = {'token': api_key}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if 'latestPrice' in data:
            return float(data['latestPrice'])
        return None
    except Exception as e:
        print(f'IEX Cloud Error: {e}')
        return None

def get_coinmarketcap_price(symbol):
    """Fetch cryptocurrency prices from CoinMarketCap API"""
    try:
        api_key = os.getenv('COINMARKETCAP_KEY')
        if not api_key:
            return None
        
        # Map symbols to CoinMarketCap IDs
        symbol_map = {
            'BTC': 1,
            'ETH': 1027,
            'BTSD': 463  # Bitshares
        }
        
        if symbol not in symbol_map:
            return None
        
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        headers = {'X-CMC_PRO_API_KEY': api_key}
        params = {'id': symbol_map[symbol], 'convert': 'USD'}
        
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        
        if 'data' in data and symbol_map[symbol] in data['data']:
            price = data['data'][symbol_map[symbol]]['quote']['USD']['price']
            return float(price)
        return None
    except Exception as e:
        print(f'CoinMarketCap Error: {e}')
        return None

def get_stock_price(symbol):
    """Get stock price from real APIs or fallback to mock"""
    symbol_upper = symbol.upper()
    
    # Try real APIs first
    if symbol_upper in ['BTC', 'ETH', 'BTSD']:
        price = get_coinmarketcap_price(symbol_upper)
        if price:
            return price
    elif symbol_upper in ['GLD', 'SLV']:
        price = get_iex_cloud_price(symbol_upper)
        if price:
            return price
    else:
        price = get_alpha_vantage_price(symbol_upper)
        if price:
            return price
    
    # Fallback to mock data
    if symbol_upper in MOCK_PRICES:
        return MOCK_PRICES[symbol_upper]['price']
    
    return 100.0  # Default fallback

@stocks_bp.route('/<symbol>/price', methods=['GET'])
def get_price(symbol):
    """Get current stock/crypto/commodity price"""
    try:
        symbol_upper = symbol.upper()
        price = get_stock_price(symbol_upper)
        
        # Get asset info from mock data
        asset_info = MOCK_PRICES.get(symbol_upper, {})
        
        return jsonify({
            'symbol': symbol_upper,
            'name': asset_info.get('name', symbol_upper),
            'type': asset_info.get('type', 'unknown'),
            'currentPrice': float(price),
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'real_api' if price != MOCK_PRICES.get(symbol_upper, {}).get('price') else 'mock'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stocks_bp.route('/<symbol>/history', methods=['GET'])
def get_history(symbol):
    """Get historical stock prices"""
    try:
        symbol = symbol.upper()
        days = request.args.get('days', 30, type=int)
        
        # Mock historical data
        history = [
            {'date': f'2024-01-{i:02d}', 'close': 100 + i * 0.5, 'volume': 1000000 + i * 50000}
            for i in range(1, min(days, 30))
        ]
        
        return jsonify({
            'symbol': symbol,
            'history': history
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stocks_bp.route('/featured', methods=['GET'])
def get_featured_assets():
    """Get featured stocks, cryptocurrencies, and commodities"""
    try:
        featured = [
            {
                'symbol': 'BTC',
                'name': 'Bitcoin',
                'type': 'crypto',
                'price': get_stock_price('BTC'),
                'change': '+5.2%',
                'icon': '₿'
            },
            {
                'symbol': 'GLD',
                'name': 'Gold ETF',
                'type': 'commodity',
                'price': get_stock_price('GLD'),
                'change': '+1.8%',
                'icon': '🏆'
            },
            {
                'symbol': 'SLV',
                'name': 'Silver ETF',
                'type': 'commodity',
                'price': get_stock_price('SLV'),
                'change': '+2.3%',
                'icon': '💎'
            },
            {
                'symbol': 'BTSD',
                'name': 'Bitshares',
                'type': 'crypto',
                'price': get_stock_price('BTSD'),
                'change': '+0.8%',
                'icon': '🔗'
            },
            {
                'symbol': 'AAPL',
                'name': 'Apple',
                'type': 'stock',
                'price': get_stock_price('AAPL'),
                'change': '+3.1%',
                'icon': '📱'
            },
            {
                'symbol': 'TSLA',
                'name': 'Tesla',
                'type': 'stock',
                'price': get_stock_price('TSLA'),
                'change': '-1.5%',
                'icon': '🚗'
            }
        ]
        
        return jsonify({'featured': featured}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
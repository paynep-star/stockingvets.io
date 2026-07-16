from app import db
from datetime import datetime
import uuid

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    stocks = db.relationship('Stock', backref='portfolio', cascade='all, delete-orphan')
    
    def get_total_value(self):
        return sum(stock.get_value() for stock in self.stocks)
    
    def get_total_gain_loss(self):
        return sum(stock.get_gain_loss() for stock in self.stocks)
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'stocks': [stock.to_dict() for stock in self.stocks],
            'totalValue': self.get_total_value(),
            'totalGainLoss': self.get_total_gain_loss(),
            'createdAt': self.created_at.isoformat()
        }

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = db.Column(db.String(36), db.ForeignKey('portfolios.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_value(self):
        return self.current_price * self.shares
    
    def get_cost_basis(self):
        return self.purchase_price * self.shares
    
    def get_gain_loss(self):
        return self.get_value() - self.get_cost_basis()
    
    def get_gain_loss_percent(self):
        cost = self.get_cost_basis()
        if cost == 0:
            return 0
        return (self.get_gain_loss() / cost) * 100
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'shares': self.shares,
            'purchasePrice': self.purchase_price,
            'currentPrice': self.current_price,
            'value': self.get_value(),
            'costBasis': self.get_cost_basis(),
            'gainLoss': self.get_gain_loss(),
            'gainLossPercent': self.get_gain_loss_percent()
        }
    
    def __repr__(self):
        return f'<Stock {self.symbol}>'
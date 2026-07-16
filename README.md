# StockingVets - Live Portfolio Dashboard

A comprehensive stock portfolio management system with user verification, community forum, and real-time position tracking.

## Features

✅ **User Authentication**
- Email/password signup and login
- Social login (Google, Facebook, Apple)
- JWT-based authentication

✅ **Account Verification**
- ID verification with document upload
- Social media verification (Twitter, Discord, LinkedIn)
- Verification status tracking

✅ **Portfolio Management**
- Add/remove stocks from portfolio
- Real-time price updates
- Gain/loss calculations
- Portfolio performance charts

✅ **Community Forum**
- Create discussion threads
- Post responses
- View top contributors
- Thread view tracking

✅ **Live Stock Data**
- Real-time position updates
- Historical price data
- Performance analytics

## Setup

### Backend

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update `.env` with your credentials:
```
JWT_SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

4. Run the backend:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend

1. Open `index.html` in your browser or serve with a local server:
```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/google` - Login with Google
- `GET /api/auth/profile` - Get user profile

### Portfolio
- `GET /api/portfolio` - Get user portfolio
- `POST /api/portfolio/add` - Add stock
- `DELETE /api/portfolio/<symbol>` - Remove stock

### Verification
- `POST /api/verification/submit` - Submit verification
- `GET /api/verification/status` - Get verification status

### Forum
- `GET /api/forum/threads` - Get forum threads
- `POST /api/forum/threads` - Create thread
- `GET /api/forum/threads/<id>/responses` - Get thread responses
- `POST /api/forum/threads/<id>/responses` - Post response
- `GET /api/forum/contributors/top` - Get top contributors

### Stocks
- `GET /api/stocks/<symbol>/price` - Get stock price
- `GET /api/stocks/<symbol>/history` - Get stock history

## Database Schema

The application uses SQLAlchemy ORM with SQLite (development) or PostgreSQL (production).

### Tables
- **users** - User accounts and authentication
- **portfolios** - User portfolio containers
- **stocks** - Individual stock holdings
- **verifications** - User verification records
- **forum_threads** - Forum discussion threads
- **forum_responses** - Forum responses/replies

## Real Stock Data

Replace mock stock data in `backend/routes/stocks.py` with real API:

- **Alpha Vantage**: https://www.alphavantage.co/
- **IEX Cloud**: https://iexcloud.io/
- **Polygon.io**: https://polygon.io/
- **Finnhub**: https://finnhub.io/

## Security Notes

⚠️ **Development Only** - This is a demo application

For production:
- Change JWT_SECRET_KEY
- Use HTTPS
- Implement proper OAuth token verification
- Add rate limiting
- Implement proper file upload validation
- Use environment variables for all secrets
- Add CSRF protection
- Implement proper error handling

## License

MIT
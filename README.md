# RCM Payment Gateway Demo

A minimal full-stack web application demonstrating Clover Payment Gateway integration for recruiters.

## Features

- **OAuth Authentication**: Secure Clover merchant authentication
- **Order Management**: Create orders and add line items
- **Payment Processing**: Demo payment processing (no real charges)
- **Transaction Logging**: Local transaction history
- **React Frontend**: Simple checkout interface

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Vite
- **Payment Gateway**: Clover API (Sandbox)

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Clover Developer Account

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configure your Clover credentials
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Clover Setup

1. Create Clover Developer App at https://sandbox.dev.clover.com/developers/
2. Set Site URL: `http://localhost:5173`
3. Enable permissions: Orders Read/Write, Payments Read/Write
4. Add credentials to `backend/.env`

## API Endpoints

### Authentication
- `GET /auth/start` - Initiate OAuth flow
- `POST /auth/exchange` - Exchange authorization code

### Orders & Payments
- `POST /payment/order` - Create order
- `POST /payment/line-item` - Add item to order
- `POST /payment/pay` - Process payment (demo)
- `GET /payment/transactions` - View transaction logs

## Usage

1. Open http://localhost:5173
2. Click "Connect Clover" → Complete OAuth
3. Create order → Add items → Process payment
4. View transaction logs at `/payment/transactions`

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── core/                # Config & constants
│   ├── services/            # Business logic
│   ├── clients/             # API clients
│   ├── db/                  # Data storage
│   └── api/routes/          # API endpoints

frontend/
├── src/
│   └── App.tsx              # React checkout UI
```

## Demo Flow

1. **Authentication**: OAuth2 with Clover
2. **Order Creation**: REST API call to Clover
3. **Line Items**: Add products to order
4. **Payment**: Demo processing (simulated)
5. **Logging**: Local transaction storage

## Interview Talking Points

- **API Integration**: RESTful design with proper error handling
- **Authentication**: OAuth2 flow implementation
- **State Management**: React hooks for UI state
- **Data Persistence**: JSON-based local storage
- **Security**: Environment variables, CORS, input validation
- **Scalability**: Modular service architecture

## Production Considerations

- Replace demo payment with real Clover payment processing
- Add database (PostgreSQL/MongoDB)
- Implement proper error handling & logging
- Add authentication middleware
- Environment-specific configurations

---

Built for technical interviews. Simple, clean, and demonstrative.

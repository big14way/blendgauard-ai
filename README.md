# 🛡️ BlendGuard

**AI-Powered DeFi Position Protection for Stellar Blend Protocol**

BlendGuard is an intelligent risk management system that protects your DeFi positions from liquidation on the Stellar Blend Protocol. Using advanced AI monitoring and automated protection mechanisms, BlendGuard ensures your assets stay safe even during market volatility.

## 🌟 Features

- **🤖 AI-Powered Risk Detection**: Real-time monitoring of position health and market conditions
- **📱 Telegram Notifications**: Instant alerts when your positions need attention
- **🛡️ Automated Protection**: Smart contract execution to prevent liquidations
- **⚡ Lightning Fast**: Sub-second response times for critical market movements
- **🔐 Secure**: HMAC-signed deeplinks and secure contract interactions
- **📊 Real-time Dashboard**: Beautiful web interface for position monitoring

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/big14way/blendgauard-ai.git
cd blendgauard-ai
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
python telegram_bot.py
```

### 3. Frontend Setup

```bash
cd blend-ui
npm install
npm run dev
```

### 4. Environment Configuration

Create a `.env` file in the backend directory:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
HMAC_SECRET_KEY=your_32_character_secret_key
FRONTEND_URL=https://your-app.vercel.app
STELLAR_NETWORK=testnet
```

## 🏗️ Architecture

### Backend Components
- **Risk Engine**: AI-powered position monitoring
- **Telegram Bot**: Real-time notifications and user interaction
- **Safety Vault**: Smart contract for automated protection
- **API Layer**: Secure communication between components

### Frontend Components
- **Protection Dashboard**: Real-time position monitoring
- **Risk Visualization**: Interactive charts and metrics
- **Action Interface**: One-click protection activation

## 📱 Telegram Bot Commands

- `/start` - Initialize the bot
- `/working_demo` - Test protection flow
- `/ping` - Check bot status

## 🔧 Deployment

### Vercel Deployment (Frontend)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main

### Backend Deployment

The backend can be deployed on any Python-compatible platform:
- Railway
- Heroku
- DigitalOcean App Platform
- AWS Lambda

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd blend-ui
npm test
```

## 🛡️ Security

- All sensitive data is stored in environment variables
- HMAC-signed deeplinks for secure communication
- No hardcoded secrets in the codebase
- Secure smart contract interactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🌟 Built for Stellar Hackathon 2025

BlendGuard showcases the power of the Stellar ecosystem for building sophisticated DeFi protection tools.

---

**🚀 Experience the future of DeFi protection with BlendGuard!** 
# 🚀 BlendGuard Deployment Guide

## Frontend Deployment (Vercel)

### 1. Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import `big14way/blendgauard-ai` repository
4. Select "blend-ui" as the root directory
5. Framework preset: Next.js
6. Build command: `npm run build`
7. Output directory: `.next`

### 2. Environment Variables

Add these environment variables in Vercel dashboard:

```env
NODE_ENV=production
NEXT_PUBLIC_STELLAR_NETWORK=testnet
NEXT_PUBLIC_STELLAR_RPC_URL=https://soroban-testnet.stellar.org
NEXT_PUBLIC_STELLAR_PASSPHRASE=Test SDF Network ; September 2015
```

### 3. Deploy

Click "Deploy" - Vercel will automatically build and deploy your app.

Your app will be available at: `https://your-project-name.vercel.app`

## Backend Deployment Options

### Option 1: Railway

1. Go to [Railway](https://railway.app)
2. Create new project from GitHub
3. Select `big14way/blendgauard-ai` repository
4. Set root directory to `backend`
5. Add environment variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
HMAC_SECRET_KEY=your_32_character_secret_key
FRONTEND_URL=https://your-vercel-app.vercel.app
STELLAR_NETWORK=testnet
STELLAR_RPC_URL=https://soroban-testnet.stellar.org
DEPLOYER_SECRET_KEY=your_stellar_secret_key
DEPLOYER_ADDRESS=your_stellar_address
```

6. Deploy with start command: `python telegram_bot.py`

### Option 2: Heroku

1. Create new Heroku app
2. Connect to GitHub repository
3. Set buildpack to Python
4. Add environment variables in Heroku dashboard
5. Create `Procfile` in backend directory:

```
worker: python telegram_bot.py
```

### Option 3: DigitalOcean App Platform

1. Create new app on DigitalOcean
2. Connect to GitHub repository
3. Set source directory to `backend`
4. Set run command: `python telegram_bot.py`
5. Add environment variables

## Environment Variables Setup

### Required Variables

```env
# Telegram Bot (Get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Security (Generate 32-character random string)
HMAC_SECRET_KEY=your_32_character_secret_key

# Frontend URL (Your Vercel deployment URL)
FRONTEND_URL=https://your-vercel-app.vercel.app

# Stellar Configuration
STELLAR_NETWORK=testnet
STELLAR_RPC_URL=https://soroban-testnet.stellar.org
STELLAR_NETWORK_PASSPHRASE=Test SDF Network ; September 2015

# Stellar Account (Optional - for advanced features)
DEPLOYER_SECRET_KEY=your_stellar_secret_key
DEPLOYER_ADDRESS=your_stellar_address
```

### How to Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token provided
5. Set bot commands using `/setcommands`:

```
start - Initialize the bot
working_demo - Test protection flow
ping - Check bot status
```

### How to Generate HMAC Secret

```bash
# Using Python
python -c "import secrets; print(secrets.token_hex(16))"

# Using OpenSSL
openssl rand -hex 16
```

## Testing Deployment

### 1. Test Frontend

1. Visit your Vercel URL
2. Check that the protection dashboard loads
3. Test the protection flow

### 2. Test Backend

1. Send `/start` to your Telegram bot
2. Send `/ping` to verify it's running
3. Send `/working_demo` to test the full flow

### 3. Test Integration

1. Use `/working_demo` in Telegram
2. Click "Activate Protection"
3. Verify the protection link opens your Vercel app
4. Complete the protection flow

## Monitoring

### Vercel Analytics

- Enable Vercel Analytics in your dashboard
- Monitor page views and performance
- Check for errors in the Functions tab

### Backend Monitoring

- Check your hosting platform's logs
- Monitor Telegram bot response times
- Set up alerts for bot downtime

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check environment variables and logs
2. **Frontend not loading**: Verify Vercel build logs
3. **Protection links not working**: Check HMAC secret key consistency
4. **CORS errors**: Ensure frontend URL is correctly set in backend

### Support

For deployment issues, check:
- Vercel documentation
- Your hosting platform's documentation
- GitHub repository issues

## Production Checklist

- [ ] Frontend deployed on Vercel
- [ ] Backend deployed and running
- [ ] All environment variables set
- [ ] Telegram bot responding
- [ ] Protection flow working end-to-end
- [ ] Monitoring set up
- [ ] Domain configured (optional)

🎉 **Congratulations! BlendGuard is now live!** 
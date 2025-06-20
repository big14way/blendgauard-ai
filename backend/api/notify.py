#!/usr/bin/env python3
"""
Notification API for BlendGuard
Handles POST /notify-telegram endpoint for success notifications
"""
import os
import logging
from flask import Flask, request, jsonify
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM")
bot = Bot(token=TELEGRAM_TOKEN)

app = Flask(__name__)

def notify_success(user_id, tx_hash, position_id, new_health):
    """Enhanced notification function for successful protection"""
    try:
        message = (
            f"✅ *Position Protected!*\n\n"
            f"• Position: `{position_id}`\n"
            f"• TX Hash: `{tx_hash}`\n"
            f"• New Health Factor: `{new_health:.2f}`"
        )
        
        keyboard = [[
            InlineKeyboardButton("View Transaction", 
                url=f"https://stellar.expert/explorer/testnet/tx/{tx_hash}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send notification using asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
            )
            return True
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Failed to notify success: {str(e)}")
        return False

@app.route('/notify-telegram', methods=['POST'])
def notify_user():
    """
    Enhanced notification endpoint:
    POST /notify-telegram
    {
      "userId": "telegram-5678",
      "message": "✅ Protection complete! TX: d1f2a...",
      "txHash": "d1f2a3b4c5e6f7890123456789abcdef",
      "positionId": "high-risk-123",
      "newHealth": 1.85
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        if not data or 'userId' not in data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: userId, message'
            }), 400
        
        user_id = data['userId']
        message = data.get('message', '')
        tx_hash = data.get('txHash')
        position_id = data.get('positionId')
        new_health = data.get('newHealth')
        
        logger.info(f"Sending notification to user {user_id} for position {position_id}")
        
        # Use enhanced notification if we have all required data
        if tx_hash and position_id and new_health:
            success = notify_success(user_id, tx_hash, position_id, new_health)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Enhanced notification sent successfully',
                    'chatId': user_id,
                    'txHash': tx_hash,
                    'newHealth': new_health
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to send enhanced notification'
                }), 500
        
        # Fallback to basic notification
        # Create keyboard with TX explorer link if hash provided
        keyboard = []
        if tx_hash:
            keyboard.append([
                InlineKeyboardButton(
                    "🔍 View Transaction", 
                    url=f"https://stellar.expert/explorer/testnet/tx/{tx_hash}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        # Send notification using asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            )
            
            logger.info(f"Notification sent successfully to {user_id}")
            return jsonify({
                'success': True,
                'message': 'Notification sent successfully',
                'chatId': user_id,
                'messageId': result.message_id,
                'txHash': tx_hash
            })
            
        finally:
            loop.close()
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to send notification: {error_msg}")
        
        # Handle common Telegram errors
        if "Chat not found" in error_msg or "Forbidden" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Chat not found',
                'details': f'User {user_id} not found in Telegram or bot blocked'
            }), 500
        
        return jsonify({
            'success': False,
            'error': 'Failed to send notification',
            'details': error_msg
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'BlendGuard Notification API',
        'telegram_configured': bool(TELEGRAM_TOKEN)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 
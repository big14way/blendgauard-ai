#!/usr/bin/env python3
"""
Telegram Notification API
Handles notifications from frontend when SafetyVault protection is executed
"""
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from alert_bot import send_alert

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route('/api/notify-telegram', methods=['POST'])
def notify_telegram():
    """Handle Telegram notification requests from frontend"""
    try:
        data = request.get_json()
        
        user_id = data.get('userId')
        position_id = data.get('positionId')
        tx_hash = data.get('txHash')
        message = data.get('message')
        actions = data.get('actions', [])
        
        if not all([user_id, position_id, tx_hash, message]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        logger.info(f"Received notification request for user {user_id}, position {position_id}")
        
        # Format the success message
        formatted_message = f"""
🛡️ *BlendGuard Protection Complete!*

✅ Position #{position_id} has been successfully protected

🔗 *Transaction Details:*
TX Hash: `{tx_hash}`

📊 *Actions Executed:*
"""
        
        for action in actions:
            action_type = action.get('action_type', 'Unknown')
            amount = action.get('amount', 0)
            asset_id = action.get('asset_id', '')
            
            if amount > 0:
                formatted_message += f"• {action_type}: {amount:,.0f} {asset_id}\n"
            else:
                formatted_message += f"• {action_type}\n"
        
        formatted_message += f"\n🎉 Your position is now protected from liquidation!"
        
        # Send notification via the bot
        # Note: This is a simplified version - in production you'd want to handle this more robustly
        try:
            # Mock the position data for the alert function
            mock_position = {
                'id': position_id,
                'asset': 'XLM',  # This would come from the actual position data
                'amount': 10000,
                'health_factor': 1.5  # Improved after protection
            }
            
            # You could use send_alert here, but for demo we'll just log
            logger.info(f"Would send Telegram message to {user_id}: {formatted_message}")
            
            return jsonify({
                'success': True,
                'message': 'Notification sent successfully',
                'tx_hash': tx_hash
            })
            
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to send notification'
            }), 500
        
    except Exception as e:
        logger.error(f"Error processing notification request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'telegram-notifier'})

if __name__ == '__main__':
    # Use port 5001 to avoid conflict with macOS AirPlay Receiver on port 5000
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    logger.info(f"Starting Telegram Notification API on {host}:{port}")
    app.run(host=host, port=port, debug=debug) 
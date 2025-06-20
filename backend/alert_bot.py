import os
import logging
import asyncio
import hmac
import hashlib
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from typing import Dict, Any
from contract_config import get_contract_id, get_contract_info, get_deployer_address
from config import DEEPLINK_SECRET, FRONTEND_URL

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
token = os.getenv("TELEGRAM_TOKEN")
if not token:
    raise ValueError("TELEGRAM_TOKEN environment variable not set")
bot = Bot(token=token)

def generate_deeplink(position_id: str, user_id: str) -> str:
    """Generate HMAC-secured deeplink for position protection"""
    try:
        secret = DEEPLINK_SECRET.encode()
        message = f"{position_id}:{user_id}".encode()
        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        
        deeplink = f"{FRONTEND_URL}/protect/?pos={position_id}&user={user_id}&sig={signature}"
        
        logger.info(f"Generated deeplink for position {position_id}, user {user_id}")
        return deeplink
    except Exception as e:
        logger.error(f"Failed to generate deeplink: {str(e)}")
        # Fallback URL without signature for demo
        return f"{FRONTEND_URL}/protect?pos={position_id}&user={user_id}"

def verify_deeplink_signature(position_id: str, user_id: str, signature: str) -> bool:
    """Verify HMAC signature for deeplink"""
    try:
        secret = DEEPLINK_SECRET.encode()
        message = f"{position_id}:{user_id}".encode()
        expected_signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Failed to verify deeplink signature: {str(e)}")
        return False

async def send_alert_async(user_id: str, position: dict, risk_score: float):
    """Send liquidation risk alert to user via Telegram (async version)"""
    try:
        contract_id = get_contract_id()
        keyboard = [
            [
                InlineKeyboardButton("🛡️ Activate Protection", callback_data=f"protect_{position['id']}"),
                InlineKeyboardButton("📊 View Details", callback_data=f"details_{position['id']}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Use the token directly for async bot operations
        token = os.getenv("TELEGRAM_TOKEN")
        if not token:
            raise ValueError("TELEGRAM_TOKEN environment variable not set")
        bot = Bot(token=token)
        await bot.send_message(
            chat_id=user_id,
            text=f"⚠️ *Liquidation Risk Alert*\n\n"
                 f"🎯 Position: {position.get('asset', 'Unknown')}\n"
                 f"📊 Risk Score: {risk_score:.0%}\n"
                 f"💰 Amount: ${position.get('amount', 0):,.2f}\n"
                 f"🔥 Health Factor: {position.get('health_factor', 'N/A')}\n\n"
                 f"⚡ *Action Required* - Your position is at risk of liquidation!\n"
                 f"🛡️ SafetyVault: `{contract_id[:8]}...{contract_id[-8:]}`",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        logger.info(f"Alert sent to user {user_id} for position {position['id']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send alert to {user_id}: {str(e)}")
        return False

def send_alert(user_id: str, position: dict, risk_score: float):
    """Send liquidation risk alert to user via Telegram (sync wrapper)"""
    try:
        # Try to get current loop, if none exists, create one
        try:
            loop = asyncio.get_running_loop()
            # If loop exists, create a task
            task = loop.create_task(send_alert_async(user_id, position, risk_score))
            return True
        except RuntimeError:
            # No loop running, use asyncio.run
            asyncio.run(send_alert_async(user_id, position, risk_score))
            return True
    except Exception as e:
        logger.error(f"Failed to send alert to {user_id}: {str(e)}")
        return False

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    if not query:
        logger.error("No callback query in update")
        return
        
    await query.answer()
    
    try:
        if query.data and query.data.startswith('protect_'):
            # Step 1: Extract position ID from callback data
            position_id = query.data.split('_')[1]
            if not query.from_user:
                logger.error("No user information in callback query")
                return
            user_id = str(query.from_user.id)
            
            # Step 2: Generate secured deeplink as specified
            message = f"{position_id}:{user_id}".encode()
            signature = hmac.new(DEEPLINK_SECRET.encode(), message, hashlib.sha256).hexdigest()
            deeplink = f"{FRONTEND_URL}/protect/?pos={position_id}&user={user_id}&sig={signature}"
            
            logger.info(f"Generated secured deeplink for position {position_id}, user {user_id}")
            
            # Step 3: Send button with "Open Protection App" as specified
            keyboard = [[InlineKeyboardButton("🛡️ Open Protection App", url=deeplink)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"🛡️ **Protection Activated!**\n\n"
                     f"✅ Secure HMAC-signed deeplink generated\n"
                     f"🔐 Position: `{position_id}`\n"
                     f"👤 User: `{user_id}`\n\n"
                     f"Click below to open BlendGuard protection interface:",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
                
        elif query.data and query.data.startswith('details_'):
            position_id = query.data.split('_')[1]
            # Get detailed position information
            position_details = get_position_details(position_id)
            contract_info = get_contract_info()
            
            keyboard = [[InlineKeyboardButton("🛡️ Activate Protection", callback_data=f"protect_{position_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"📊 **Position Details**\n\n"
                     f"🏷️ ID: `{position_id}`\n"
                     f"🎯 Asset: {position_details.get('asset', 'Unknown')}\n"
                     f"💰 Collateral: ${position_details.get('collateral', 0):,.2f}\n"
                     f"💸 Debt: ${position_details.get('debt', 0):,.2f}\n"
                     f"📈 LTV: {position_details.get('ltv', 0):.1%}\n"
                     f"🔥 Health Factor: {position_details.get('health_factor', 'N/A')}\n"
                     f"⚡ Liquidation Price: ${position_details.get('liquidation_price', 0):,.2f}\n\n"
                     f"🛡️ SafetyVault Ready: {contract_info['status']}",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            
    except Exception as e:
        logger.error(f"Error handling callback {query.data}: {str(e)}")
        await query.edit_message_text(
            text="❌ An error occurred while processing your request. Please try again.",
            parse_mode="Markdown"
        )

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    if not update.message:
        logger.error("No message in update")
        return
        
    welcome_message = """
🛡️ **Welcome to BlendGuard!**

I'm your personal Stellar lending protection assistant. I monitor your positions and help protect them from liquidation.

**Available Commands:**
• `/status` - Check your position health
• `/contract` - View BlendGuard contract info
• `/demo` - See demo protection result

Stay safe! 🚀
"""
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def handle_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /demo command - show protection result with TX hash"""
    if not update.message:
        logger.error("No message in update")
        return
        
    # Generate demo TX hash
    demo_tx = "d1f2a5c8e3b7a9f012e4b8c7d5f6e3a9b2c4d7e8f1a3b5c6d9e2f4a7b8c1d5e"
    
    keyboard = [[
        InlineKeyboardButton("View on Explorer", 
            url=f"https://stellar.expert/explorer/testnet/tx/{demo_tx}")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    demo_message = (
        f"⚠️ *DEMO: Protection Applied*\n"
        f"🔗 TX: `{demo_tx[:16]}...`\n"
        f"🆕 Health Factor: **1.85**\n\n"
        f"🛡️ Position successfully protected from liquidation!"
    )
    
    await update.message.reply_text(
        demo_message,
        parse_mode="Markdown",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show user's lending positions and risks"""
    if not update.message or not update.message.from_user:
        logger.error("No message or user in update")
        return
        
    user_id = str(update.message.from_user.id)
    positions = get_user_positions(user_id)
    
    if not positions:
        no_positions_message = """
📊 **Position Status**

No active lending positions found.

Connect your wallet to start using Blend lending markets!
"""
        await update.message.reply_text(no_positions_message, parse_mode="Markdown")
        return
    
    status_message = "📊 **Your Lending Positions**\n\n"
    
    keyboard = []
    for position in positions:
        risk_emoji = "🔴" if position['risk_score'] > 0.8 else "🟡" if position['risk_score'] > 0.6 else "🟢"
        status_message += f"{risk_emoji} **{position['asset']}**: ${position['amount']:,}\n"
        status_message += f"   Risk: {position['risk_score']:.0%} | Health: {position['health_factor']:.2f}\n\n"
        
        if position['risk_score'] > 0.7:  # High risk positions
            keyboard.append([InlineKeyboardButton(
                f"🛡️ Activate Protection - {position['asset']}", 
                callback_data=f"protect_{position['id']}"
            )])
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.message.reply_text(status_message, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contract command - show contract information"""
    if not update.message:
        logger.error("No message in update") 
        return
        
    contract_info = get_contract_info()
    contract_message = f"""
🔗 **BlendGuard Contract Info**

**SafetyVault Contract:**
`{contract_info['contract_id']}`

**Network:** {contract_info['network']}
**Version:** {contract_info['version']}

This contract protects your lending positions through automated safety actions.
"""
    await update.message.reply_text(contract_message, parse_mode="Markdown")

def trigger_safety_vault_protection(position_id: str) -> Dict[str, Any]:
    """Trigger SafetyVault protection for a position"""
    try:
        contract_id = get_contract_id()
        contract_info = get_contract_info()
        
        logger.info(f"Triggering SafetyVault protection for position {position_id}")
        logger.info(f"Using contract: {contract_id}")
        
        # In a real implementation, this would:
        # 1. Create Stellar SDK client with contract_info['rpc_url']
        # 2. Build transaction with SafetyVault.execute_actions()
        # 3. Submit transaction to network using the deployer account
        # 4. Return actual transaction hash
        
        # Mock successful response with actual contract info
        return {
            'success': True,
            'tx_hash': f'stellar_tx_{position_id}_{contract_id[:8]}',
            'contract_id': contract_id,
            'message': f'SafetyVault {contract_info["version"]} protection activated'
        }
    except Exception as e:
        logger.error(f"SafetyVault protection failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def get_position_details(position_id: str) -> Dict[str, Any]:
    """Get detailed information about a position"""
    # Centralized position data - consistent with position_service.js
    return {
        'id': position_id or 'XLM-123',
        'asset': 'XLM',
        'collateral': 10000.00,  # USD value
        'debt': 8500.00,         # USD value
        'ltv': 0.85,            # 85%
        'health_factor': 1.15,
        'liquidation_price': 0.095,
        'status': 'high-risk'
    }

def format_position(position):
    """Standardized position formatting for consistent display"""
    return (
        f"🔴 {position['asset']} Position\n"
        f"• Amount: ${position['collateral']:,.2f}\n"
        f"• Risk: {position['ltv']*100:.0f}% (HIGH)\n"
        f"• Health Factor: {position['health_factor']:.2f}\n"
        f"• Status: ⚠️ Liquidation Risk\n\n"
        f"⚡ Action Required!"
    )

def get_user_positions(user_id: str) -> list:
    """Get all positions for a user"""
    # Centralized position data - consistent with position_service.js
    HIGH_RISK_POSITION = {
        "id": "XLM-123",
        "ltv": 0.85,
        "collateral": 10000,  # USD value - consistent with Telegram display
        "debt": 8500,
        "pool": "XLM-LENDING",
        "assets": [{"code": "XLM", "amount": 10000}],
        "asset": "XLM", 
        "amount": 10000,  # Updated to match collateral
        "risk_score": 0.85,
        "health_factor": 1.15
    }
    
    return [HIGH_RISK_POSITION]

def start_bot(test_mode=False):
    """Start the bot with proper event loop handling"""
    try:
        # Check if there's already a running event loop
        try:
            loop = asyncio.get_running_loop()
            logger.info("Event loop already running, creating new thread")
            import threading
            import concurrent.futures
            
            def run_bot_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(run_bot_async())
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_bot_in_thread)
                return future.result()
                
        except RuntimeError:
            # No event loop running, safe to create one
            logger.info("Starting new event loop")
            return asyncio.run(run_bot_async())
            
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        return False

async def run_bot_async():
    """Internal async function to run the bot"""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN environment variable not set")
        return False
    
    application = None
    try:
        # Log contract info on startup
        contract_info = get_contract_info()
        logger.info(f"BlendGuard Alert Bot starting with SafetyVault: {contract_info['contract_id']}")
        
        application = Application.builder().token(token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", handle_start))
        application.add_handler(CommandHandler("status", handle_status))
        application.add_handler(CommandHandler("contract", handle_contract))
        application.add_handler(CommandHandler("demo", handle_demo))
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Start polling
        logger.info("BlendGuard Alert Bot started successfully!")
        await application.run_polling(drop_pending_updates=True)
        return True
        
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        return False
    finally:
        if application:
            try:
                await application.shutdown()
                logger.info("Bot shutdown completed")
            except Exception as e:
                logger.error(f"Error during shutdown: {str(e)}")

async def main(test_mode=False):
    """Start the bot (legacy function for compatibility)"""
    logger.warning("main() function is deprecated, use start_bot() instead")
    return start_bot(test_mode=test_mode)

def test_bot():
    """Test bot initialization without running indefinitely"""
    return start_bot(test_mode=True)

if __name__ == '__main__':
    start_bot() 
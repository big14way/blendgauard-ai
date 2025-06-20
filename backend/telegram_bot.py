#!/usr/bin/env python3
"""
Working callback bot - NO markdown parsing issues
"""
import logging
import traceback
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM"

async def working_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Working callback handler - no markdown issues"""
    print(f"\n🔔 CALLBACK: {update.callback_query.data if update.callback_query else 'No data'}")
    
    query = update.callback_query
    if not query:
        return
    
    try:
        # Step 1: Answer the callback
        await query.answer("🛡️ Protection activated!")
        print("✅ Callback answered")
        
        # Step 2: Process the action
        if query.data in ["protect_demo", "protect_XLM-123"]:
            user_id = query.from_user.id if query.from_user else "123456789"
            protection_link = f"http://localhost:3000/protect?pos=XLM-123&user={user_id}&sig=a2661dd772013edbfac150f29adf8685b3c2c7ba8e561512dbf550c1e1831d75"
            
            # Simple text without markdown to avoid parsing issues
            success_text = f"""🛡️ Protection Activated Successfully!

✅ Position: XLM-123
👤 User ID: {user_id}
🔐 Secure Link Generated
🕐 Generated: Now

🌐 Protection Link:
{protection_link}

📱 Instructions:
1. Copy the link above
2. Open in your browser
3. Complete protection setup

🚀 Your position is now being protected by BlendGuard!"""
            
            # NO parse_mode to avoid markdown errors
            await query.edit_message_text(success_text)
            print("✅ Protection link sent successfully!")
            
        else:
            await query.edit_message_text(f"❌ Unknown action: {query.data}")
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        print(traceback.format_exc())
        
        try:
            await query.edit_message_text(f"❌ Error: {str(e)}")
        except:
            print("❌ Failed to send error message")

async def working_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Working demo command - no markdown issues"""
    if not update.message:
        return
    
    keyboard = [[InlineKeyboardButton("🛡️ Activate Protection", callback_data="protect_XLM-123")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Plain text without markdown
    demo_text = """⚠️ LIQUIDATION ALERT

🎯 Position: XLM Lending
💰 Collateral: $10,000
📉 LTV: 85%
🩺 Health Factor: 1.15
🔥 Risk Level: CRITICAL

🛡️ BlendGuard Protection Ready!

Click to activate protection"""
    
    # NO parse_mode to avoid markdown errors
    await update.message.reply_text(demo_text, reply_markup=reply_markup)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - no markdown issues"""
    if not update.message:
        return
    
    # Plain text without markdown
    welcome = """🛡️ BlendGuard Protection Bot

Commands:
• /start - This message
• /working_demo - Test protection flow
• /ping - Connection test

This bot protects your DeFi positions from liquidation."""
    
    # NO parse_mode to avoid markdown errors
    await update.message.reply_text(welcome)

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ping test"""
    if update.message:
        await update.message.reply_text("🏓 Pong! Bot is working perfectly.")

def main():
    """Run working bot"""
    print("✅ Starting WORKING Protection Bot...")
    print("✅ No markdown parsing - completely stable")
    print("="*50)
    
    try:
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("working_demo", working_demo))
        app.add_handler(CommandHandler("ping", ping_command))
        app.add_handler(CallbackQueryHandler(working_callback))
        
        print("✅ Handlers registered")
        print("🚀 Starting polling...")
        print("\n📋 TEST STEPS:")
        print("1. Send /working_demo to the bot")
        print("2. Click 'Activate Protection' button")
        print("3. Copy the protection link from response")
        print("4. Open link in browser")
        print("="*50)
        
        # Run with proper error handling
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Bot error: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main() 
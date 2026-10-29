import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Get Token from environment variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message that complies with ad guidelines (avoiding imperative commands, using 'you')"""
    user = update.effective_user
    
    # Note: The following text avoids "Click" and "Follow", using neutral descriptions instead
    welcome_text = (
        f"Hello, {user.first_name}.\n\n"
        "Welcome to IA DEL REY.\n"
        "This is a smart assistant designed to provide you with information services.\n\n"
        "You can learn about related features through the menu below."
    )
    
    keyboard = [
        [InlineKeyboardButton("Feature Introduction", callback_data="feature")],
        [InlineKeyboardButton("Usage Guide", callback_data="guide")],
        [InlineKeyboardButton("Return to Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks to ensure interactivity"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "feature":
        text = "The main features of IA DEL REY include intelligent Q&A and information aggregation.\nThe specific experience will be launched gradually in subsequent versions."
        keyboard = [[InlineKeyboardButton("Return to Menu", callback_data="menu")]]
    elif query.data == "guide":
        text = "Usage: You can directly send text, and the system will provide feedback based on the current functionality."
        keyboard = [[InlineKeyboardButton("Return to Menu", callback_data="menu")]]
    else:
        text = "You have returned to the main menu."
        keyboard = [
            [InlineKeyboardButton("Feature Introduction", callback_data="feature")],
            [InlineKeyboardButton("Usage Guide", callback_data="guide")]
        ]
    
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

def main() -> None:
    """Start the bot"""
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable not set")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Use polling to run (Railway worker mode)
    application.run_polling()

if __name__ == "__main__":
    main()

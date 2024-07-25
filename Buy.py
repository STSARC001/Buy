import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import threading

# Replace 'YOUR_TELEGRAM_TOKEN' with your actual bot token
TOKEN = '7323141793:AAHbGgPfOEmmLUnMe-7I9X5MPjuhqiAfxYQ'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running!'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = ("Hello sir 🌟\n\n"
               "Welcome to the Stake Payment Gateway! 🎧\n\n"
               "💎 Get your Premium Bot 🤖 License Key 🔒\n"
               "💰 Bot Price: $XX.XX\n\n"
               "For contact and support, please reach out to us through this channel. "
               "We're here to assist you every step of the way! 🤝\n\n"
               "Now, let's proceed with the payment:\n\n"
               "🧾 Payment Method:\n\n"
               "Credit/Debit Card 💳\n"
               "PayPal 💸\n"
               "Cryptocurrency 💰\n"
               "Bank Transfer 🏦\n\n"
               "Simply select your preferred payment method, and we'll guide you through the rest!")

    keyboard = [
        [InlineKeyboardButton("Credit/Debit Card 💳", callback_data='credit_card')],
        [InlineKeyboardButton("PayPal 💸", callback_data='paypal')],
        [InlineKeyboardButton("Cryptocurrency 💰", callback_data='crypto')],
        [InlineKeyboardButton("Bank Transfer 🏦", callback_data='bank_transfer')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)

async def payment_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Based on the user's choice, show the next set of buttons
    keyboard = [
        [InlineKeyboardButton("QR", callback_data='qr')],
        [InlineKeyboardButton("UPI ID", callback_data='upi')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"You selected {query.data.replace('_', ' ').title()}.\nPlease choose a payment method:",
        reply_markup=reply_markup
    )

async def payment_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'qr':
        qr_image_path = 'qr.jpg'  # Replace with the actual path to your QR code image
        await query.message.reply_photo(photo=open(qr_image_path, 'rb'),
                                        caption="Scan the QR code to make the payment.")
    elif query.data == 'upi':
        await query.message.reply_text(text="Our UPI ID: 9370162316@paytm")

def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(payment_option, pattern='^(credit_card|paypal|crypto|bank_transfer)$'))
    application.add_handler(CallbackQueryHandler(payment_detail, pattern='^(qr|upi)$'))

    application.run_polling()

if __name__ == '__main__':
    # Start the Telegram bot in a separate thread
    threading.Thread(target=run_bot).start()

    # Start the Flask server
    port = int(os.environ.get('PORT', 4000))  # Use PORT env variable or default to 4000
    app.run(host='0.0.0.0', port=port)

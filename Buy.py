import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Directly assign your bot token for testing
TOKEN = '7323141793:AAHbGgPfOEmmLUnMe-7I9X5MPjuhqiAfxYQ'  # Replace with your actual bot token

START_MESSAGE = (
    '''
Hello, GameMaster! 🎮✨

Welcome to the GameMaster Payment Gateway! 🎧

🌟 Unlock Your Premium Bot License Key Now! 🤖🔒
💰 **Special Price**: Only 456 RS!

Need help? Our support team is here to assist you every step of the way! 🤝

Let's get started with your payment:

🧾 **Payment Methods:**
- UPI 📱
- PhonePe 📲
- PayPal 💸
- Paytm 💰
- Bank Transfer 🏦

Choose your preferred method, and we’ll guide you through the rest!

💸 **Referral Bonus:**
Invite a friend and earn ₹100 when they purchase the bot! Just send us a screenshot of the referral and purchase to claim your bonus.

Ready to elevate your gaming experience? Let's go! 🚀
    '''
)

HELP_MESSAGE = (
    "For any inquiries or support, please contact us via this channel $https://t.me/gamemasterbuy "
    "We are here to help you!"
)

PAYMENT_OPTIONS = [
    InlineKeyboardButton("UPI ", callback_data='credit_card'),
    InlineKeyboardButton("PhonePe 💸", callback_data='paypal'),
    InlineKeyboardButton("Paytm 💰", callback_data='crypto'),
    InlineKeyboardButton("Bank Transfer 🏦", callback_data='bank_transfer')
]

PAYMENT_METHODS = [
    InlineKeyboardButton("QR", callback_data='qr'),
    InlineKeyboardButton("UPI ID", callback_data='upi')
]

PAYMENT_CONFIRMATION_MESSAGE = (
    '''
📸 After Payment:

Once you've completed the payment, please send a screenshot to our Telegram ID. 📲

⏳ Quick Access:
We'll provide you with your username within 10 minutes! Enter the username and unlock ultimate access to the bot. 🚀

Thank you for choosing GameMaster! Let's make your gaming experience legendary! 🌟
    '''
)

REDIRECT_BUTTON = InlineKeyboardButton("Contact Support Bot", url='https://t.me/gamemasterbuy')  # Replace with your actual bot link

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = InlineKeyboardMarkup([PAYMENT_OPTIONS])
    await update.message.reply_text(START_MESSAGE, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_MESSAGE)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    feedback_message = update.message.text
    # Here, you can save the feedback to a database or send it to an admin
    await update.message.reply_text("Thank you for your feedback!")

async def payment_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup([PAYMENT_METHODS])
    await query.edit_message_text(
        text=f" \nPlease choose a payment method:",
        reply_markup=reply_markup
    )

async def payment_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'qr':
        qr_image_path = 'qr.jpg'  # Replace with the actual path to your QR code image
        reply_markup = InlineKeyboardMarkup([[REDIRECT_BUTTON]])
        await query.message.reply_photo(photo=open(qr_image_path, 'rb'),
                                        caption=f"Scan the QR code to make the payment.\n\n{PAYMENT_CONFIRMATION_MESSAGE}",
                                        reply_markup=reply_markup)
    elif query.data == 'upi':
        reply_markup = InlineKeyboardMarkup([[REDIRECT_BUTTON]])
        await query.message.reply_text(text=f"Our UPI ID: coderd60@okicici\n\n{PAYMENT_CONFIRMATION_MESSAGE}",
                                       reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, feedback))
    application.add_handler(CallbackQueryHandler(payment_option, pattern='^(credit_card|paypal|crypto|bank_transfer)$'))
    application.add_handler(CallbackQueryHandler(payment_detail, pattern='^(qr|upi)$'))

    application.run_polling()

if __name__ == '__main__':
    main()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3

# توکن ربات خود را در اینجا قرار دهید
TOKEN = '7441072447:AAF6sWKCJIhDakR4g0B0yoIHR5aFJV8EnPo'

# توابع پایگاه داده
def create_wallet(user_id):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO wallets (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute('SELECT balance FROM wallets WHERE user_id = ?', (user_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance

def update_balance(user_id, amount):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute('UPDATE wallets SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

# دستورات ربات
def start(update, context):
    user_id = update.message.chat_id
    create_wallet(user_id)
    update.message.reply_text('Welcome! Your wallet has been created.')

def balance(update, context):
    user_id = update.message.chat_id
    bal = get_balance(user_id)
    update.message.reply_text(f'Your balance is {bal} units.')

def add(update, context):
    user_id = update.message.chat_id
    try:
        amount = float(context.args[0])
        update_balance(user_id, amount)
        update.message.reply_text(f'{amount} units added to your wallet.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <amount>')

def subtract(update, context):
    user_id = update.message.chat_id
    try:
        amount = float(context.args[0])
        update_balance(user_id, -amount)
        update.message.reply_text(f'{amount} units subtracted from your wallet.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /subtract <amount>')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('balance', balance))
    dp.add_handler(CommandHandler('add', add))
    dp.add_handler(CommandHandler('subtract', subtract))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

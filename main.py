import os
import telebot

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, 'مرحباً بك! البوت يعمل الآن بشكل متواصل 24/7.')


if __name__ == '__main__':
  print('Bot is running...')
  bot.infinity_polling()

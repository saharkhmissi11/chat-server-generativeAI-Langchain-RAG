import telebot


def telegram(message):
    bot = telebot.TeleBot("6994318049:AAGk4tmd-NsZY3KWc0hwOdrdfp6SGG61VKU")
    chat_id = 6246467376
    bot.send_message(chat_id, message)


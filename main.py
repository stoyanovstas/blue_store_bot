import telebot
import os
from dotenv import load_dotenv
from google_client import GoogleClient

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS").split(",")
SHEET_ID = os.getenv("SHEET_ID")

bot = telebot.TeleBot(BOT_TOKEN)
gc = GoogleClient(os.getenv("GOOGLE_CREDENTIALS_JSON_PATH"), SHEET_ID)

@bot.message_handler(commands=['start'])
def handle_start(message):
    telegram_id = str(message.from_user.id)
    name = message.from_user.first_name
    user = gc.find_user(telegram_id)

    if user:
        bot.send_message(message.chat.id, f"👋 Привет, {name}! Ты уже зарегистрирован.")
    else:
        gc.register_user(telegram_id, name)
        bot.send_message(message.chat.id, f"👋 Добро пожаловать в Blue Store, {name}! 🎉\nТвой аккаунт создан.")

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("💰 Мой баланс", "📜 История заказов")
    keyboard.row("🎁 Пригласить друга", "🧾 Использовать бонусы")
    bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "💰 Мой баланс")
def handle_balance(message):
    telegram_id = str(message.from_user.id)
    user = gc.find_user(telegram_id)
    if user:
        balance = user.get("Баланс Blue Coins", "0")
        bot.send_message(message.chat.id, f"💰 У тебя {balance} blue coins.")
    else:
        bot.send_message(message.chat.id, "Ты ещё не зарегистрирован. Напиши /start")

@bot.message_handler(func=lambda message: message.text == "📜 История заказов")
def handle_history(message):
    bot.send_message(message.chat.id, "🕓 История заказов скоро появится!")

@bot.message_handler(func=lambda message: message.text == "🎁 Пригласить друга")
def handle_refer(message):
    telegram_id = str(message.from_user.id)
    bot.send_message(message.chat.id, f"🔗 Поделись этой ссылкой: t.me/YourBotUsername?start={telegram_id}")

@bot.message_handler(func=lambda message: message.text == "🧾 Использовать бонусы")
def handle_use_bonus(message):
    bot.send_message(message.chat.id, "⚠️ Списание бонусов будет доступно в следующем обновлении.")

bot.polling(none_stop=True)

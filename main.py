import logging
from aiogram import Bot, Dispatcher, executor, types
from google_client import GoogleClient
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS").split(",")
SHEET_ID = os.getenv("SHEET_ID")
JSON_KEYFILE = os.getenv("GOOGLE_KEYFILE")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

gc = GoogleClient(JSON_KEYFILE, SHEET_ID)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    telegram_id = str(msg.from_user.id)
    name = msg.from_user.full_name

    user = gc.find_user(telegram_id)
    if user:
        await msg.answer(f"👋 Привет, {name}! Ты уже зарегистрирован.")
    else:
        gc.register_user(telegram_id, name)
        await msg.answer(f"👋 Добро пожаловать в Blue Store, {name}! 🎉\nТвой аккаунт создан.")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💰 Мой баланс", "📜 История заказов")
    keyboard.add("🎁 Пригласить друга", "🧾 Использовать бонусы")
    await msg.answer("Что хочешь сделать?", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "💰 Мой баланс")
async def show_balance(msg: types.Message):
    telegram_id = str(msg.from_user.id)
    user = gc.find_user(telegram_id)
    if user:
        balance = user.get("Баланс Blue Coins", "0")
        await msg.answer(f"💰 У тебя {balance} blue coins.")
    else:
        await msg.answer("Ты ещё не зарегистрирован. Напиши /start")

@dp.message_handler(lambda msg: msg.text == "📜 История заказов")
async def history(msg: types.Message):
    await msg.answer("🕓 История заказов скоро появится!")

@dp.message_handler(lambda msg: msg.text == "🎁 Пригласить друга")
async def refer(msg: types.Message):
    await msg.answer("🔗 Поделись этой ссылкой: t.me/YourBotUsername?start=" + str(msg.from_user.id))

@dp.message_handler(lambda msg: msg.text == "🧾 Использовать бонусы")
async def use_bonus(msg: types.Message):
    await msg.answer("⚠️ Списание бонусов будет доступно в следующем обновлении.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
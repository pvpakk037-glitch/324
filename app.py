import telebot
from flask import Flask, request
import os

# Токен берется из настроек сервера
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- ГЛАВНЫЙ ВХОД ДЛЯ TELEGRAM ---
@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    
    # МЫ БОЛЬШЕ НЕ ДОВЕРЯЕМ telebot. МЫ ВЫЗЫВАЕМ ОБРАБОТЧИК ВРУЧНУЮ, НАХУЙ.
    # Это грязный, но 100% рабочий способ.
    if update.message:
        echo_all(update.message)
        
    return "!", 200

# --- НАШ ОБРАБОТЧИК СТАЛ ОБЫЧНОЙ ФУНКЦИЕЙ ---
# Мы убрали декоратор @bot.message_handler, потому что он нас наебал
def echo_all(message):
    bot.reply_to(message, 'ЗАРАБОТАЛО, СУКА!')

# --- Вебхук-сеттер ---
@app.route("/")
def webhook_setter():
    bot.remove_webhook()
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.set_webhook(url=f"{render_url}/{BOT_TOKEN}")
    return "код победы на месте", 200

# Эта часть нужна, чтобы Render мог запустить сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

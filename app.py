import telebot
from flask import Flask, request
import os # Добавили os для работы с переменными окружения

# ==========================================================
# ТОКЕН ТЕПЕРЬ БЕРЕТСЯ ИЗ НАСТРОЕК СЕРВЕРА, А НЕ ИЗ КОДА
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# ==========================================================

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'привет с рендера')

@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook_setter():
    bot.remove_webhook()
    # URL для Render будет другим, его мы тоже возьмем из настроек сервера
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.set_webhook(url=f"{render_url}/{BOT_TOKEN}")
    return "вебхук для рендера установлен", 200

# Эта часть нужна, чтобы Render мог запустить сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
import telebot
from flask import Flask, request
import os
import traceback # Инструмент для вывода ошибок

# Токен берется из настроек сервера
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- НАШ ОБРАБОТЧИК ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("--- !!! HANDLER 'echo_all' CALLED !!! ---") # Если мы увидим это, то все заработало
    bot.reply_to(message, 'привет с рендера')

# --- ГЛАВНЫЙ ВХОД ДЛЯ TELEGRAM ---
@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    print("\n--- >>>>>>>>> get_message CALLED! Request received. <<<<<<<<< ---")
    try:
        # 1. Распечатаем то, что прислал Telegram
        json_string = request.stream.read().decode("utf-8")
        print(f"--- Raw JSON from Telegram: {json_string} ---")

        # 2. Попытаемся разобрать это
        update = telebot.types.Update.de_json(json_string)
        print("--- JSON parsed successfully. Update object created. ---")

        # 3. Отдадим это telebot для обработки
        bot.process_new_updates([update])
        print("--- process_new_updates finished without crashing. ---")

    except Exception as e:
        # Если что-то сломалось, мы увидим это в логах
        print("--- !!! EXCEPTION INSIDE get_message !!! ---")
        print(traceback.format_exc())
    
    print("--- >>>>>>>>> get_message finished. Returning '200 OK'. <<<<<<<<< ---\n")
    return "!", 200

# --- Вебхук-сеттер ---
@app.route("/")
def webhook_setter():
    bot.remove_webhook()
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.set_webhook(url=f"{render_url}/{BOT_TOKEN}")
    return "диагностический бот на месте", 200

# Эта часть нужна, чтобы Render мог запустить сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

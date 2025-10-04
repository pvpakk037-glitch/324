import telebot
import os
from flask import Flask, request

# ==========================================================
# ↓↓↓ Берем данные из настроек Render ↓↓↓
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
# ==========================================================

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


# <<< ИЗМЕНЕНИЕ 1: Твои функции теперь без декораторов >>>
# Это просто обычные функции. Мы будем вызывать их сами.

def send_welcome(message):
    bot.reply_to(message, "Здравствуйте, официальный бот https://t.me/MBOYSOSH2Steers отправляйте свой пост и он попадет в канал!")

def handle_text(message):
    username = f"@{message.from_user.username}" if message.from_user.username else "Юз не найден"
    user_info = (
        f"👤 *Новое сообщение от пользователя:*\n"
        f"*Имя:* `{message.from_user.first_name}`\n"
        f"*Юз:* `{username}`\n"
        f"*ID:* `{message.from_user.id}`"
    )
    bot.send_message(message.chat.id, "Отлично! Сообщение передано админу.")
    bot.send_message(ADMIN_CHAT_ID, user_info, parse_mode="Markdown")
    bot.send_message(ADMIN_CHAT_ID, message.text)

def handle_photo(message):
    username = f"@{message.from_user.username}" if message.from_user.username else "Юз не найден"
    user_info = (
        f"👤 *Новое сообщение от пользователя:*\n"
        f"*Имя:* `{message.from_user.first_name}`\n"
        f"*Юз:* `{username}`\n"
        f"*ID:* `{message.from_user.id}`"
    )
    bot.send_message(message.chat.id, "Отлично! Сообщение передано админу.")
    bot.send_message(ADMIN_CHAT_ID, user_info, parse_mode="Markdown")
    bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=message.caption)


# <<< ИЗМЕНЕНИЕ 2: Создаем "диспетчера", который решает, какую функцию вызвать >>>

def route_message(message):
    # Если в сообщении есть текст
    if message.text:
        if message.text == '/start':
            send_welcome(message)
        else:
            handle_text(message)
    # Если в сообщении есть фото
    elif message.photo:
        handle_photo(message)


# <<< ИЗМЕНЕНИЕ 3: Главный вход для Telegram теперь вызывает нашего "диспетчера" >>>

@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    
    # Вручную вызываем нашего диспетчера
    if update.message:
        route_message(update.message)
        
    return "!", 200


# <<< ИЗМЕНЕНИЕ 4: Вебхук-сеттер теперь правильный, для Render >>>

@app.route("/")
def webhook_setter():
    bot.remove_webhook()
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.set_webhook(url=f"{render_url}/{BOT_TOKEN}")
    return "БОТ-ПЕРЕСЫЛЬЩИК НА МЕСТЕ", 200

# Эта часть нужна, чтобы Render мог запустить сервер
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

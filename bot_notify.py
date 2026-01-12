import os
import telebot
import firebase_admin
import json
from firebase_admin import credentials, firestore

BOT_TOKEN = os.getenv('BOT_TOKEN')
FIREBASE_JSON_STR = os.getenv('FIREBASE_JSON')

def test_push():
    cred_dict = json.loads(FIREBASE_JSON_STR)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(cred_dict))
    
    db = firestore.client()
    bot = telebot.TeleBot(BOT_TOKEN)
    
    users = db.collection("users").stream()
    
    for user in users:
        user_id = user.id
        print(f"Пытаюсь отправить сообщение на ID: {user_id}")
        try:
            bot.send_message(user_id, "🔔 ТЕСТ: Бот видит тебя и может отправлять уведомления!")
            print("Успешно отправлено!")
        except Exception as e:
            print(f"Ошибка отправки: {e}. Возможно, пользователь не нажал /start в боте.")

if __name__ == "__main__":
    test_push()

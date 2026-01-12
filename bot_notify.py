import os
import time
import telebot
import firebase_admin
import json
from firebase_admin import credentials, firestore

# Секреты
BOT_TOKEN = os.getenv('BOT_TOKEN')
FIREBASE_JSON_STR = os.getenv('FIREBASE_JSON')

def run_notify():
    try:
        if not firebase_admin._apps:
            cred_dict = json.loads(FIREBASE_JSON_STR.strip())
            firebase_admin.initialize_app(credentials.Certificate(cred_dict))

        db = firestore.client()
        bot = telebot.TeleBot(BOT_TOKEN)
        users_ref = db.collection("users")
        docs = users_ref.stream()

        for doc in docs:
            data = doc.to_dict()
            user_id = doc.id
            hunger = data.get('hunger', 100)
            last_update = data.get('lastUpdate')
            was_notified = data.get('was_notified', False)

            if last_update:
                # Считаем текущий голод (1% за 10 мин = 600 сек)
                seconds_passed = time.time() - last_update.timestamp()
                lost_hunger = int(seconds_passed / 600)
                current_hunger = hunger - lost_hunger
                
                print(f"ID {user_id}: Голод {current_hunger}%, Уведомлен: {was_notified}")

                # НОВАЯ ЛОГИКА: Пишем если голод меньше 30% (даже если 0 или минус)
                if current_hunger <= 30 and not was_notified:
                    try:
                        bot.send_message(user_id, "🐾 Твой котик очень голоден! Зайди покормить его, пока есть время! 🍖")
                        db.collection("users").doc(user_id).update({"was_notified": True})
                        print(f"Отправлено для {user_id}")
                    except Exception as e:
                        print(f"Ошибка ТГ: {e}")
                
                # Сброс метки, если покормили выше 80%
                elif current_hunger > 80 and was_notified:
                    db.collection("users").doc(user_id).update({"was_notified": False})

    except Exception as e:
        print(f"Ошибка сервера: {e}")

if __name__ == "__main__":
    run_notify()

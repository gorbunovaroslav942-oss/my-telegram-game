import os
import time
import telebot
import firebase_admin
import json
from firebase_admin import credentials, firestore

# Секреты из GitHub
BOT_TOKEN = os.getenv('BOT_TOKEN')
FIREBASE_JSON_STR = os.getenv('FIREBASE_JSON')

def run_notify():
    if not BOT_TOKEN or not FIREBASE_JSON_STR:
        print("Ошибка: Секреты не найдены!")
        return

    try:
        # Инициализация
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
            
            if 'hunger' in data and 'lastUpdate' in data:
                # Считаем оффлайн-голод (1% в 10 минут)
                last_update_ts = data['lastUpdate'].timestamp()
                seconds_passed = time.time() - last_update_ts
                lost_hunger = int(seconds_passed / 600)
                current_hunger = data['hunger'] - lost_hunger
                
                print(f"Пользователь {user_id}: Голод {current_hunger}%")

                # УСЛОВИЕ: Пишем, если голод упал ниже 30%, но кот еще жив (выше 0)
                # Мы проверяем диапазон 20-30, чтобы не спамить, когда совсем 0
                if 20 <= current_hunger <= 30:
                    try:
                        bot.send_message(user_id, "🐾 Твой котик проголодался! (Осталось меньше 30%)\nЗайди в игру, чтобы покормить его! 🍖")
                        print(f"Уведомление отправлено для {user_id}")
                    except Exception as e:
                        print(f"Ошибка отправки: {e}")
                elif current_hunger <= 0:
                    print(f"Кот пользователя {user_id} совсем голоден (0%), уведомление не шлем, чтобы не надоедать.")

    except Exception as e:
        print(f"Ошибка скрипта: {e}")

if __name__ == "__main__":
    run_notify()

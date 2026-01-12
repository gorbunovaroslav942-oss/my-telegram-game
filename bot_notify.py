import os
import time
import telebot
import firebase_admin
import json
from firebase_admin import credentials, firestore

# Загружаем секреты
BOT_TOKEN = os.getenv('BOT_TOKEN')
FIREBASE_JSON_STR = os.getenv('FIREBASE_JSON')

def check_hunger():
    print("Проверка голода котиков...")
    
    if not firebase_admin._apps:
        cred_dict = json.loads(FIREBASE_JSON_STR)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    bot = telebot.TeleBot(BOT_TOKEN)

    users_ref = db.collection("users")
    docs = users_ref.stream()

    for doc in docs:
        # ВОТ ТУТ ИСПРАВЛЕНО: используем to_dict()
        data = doc.to_dict()
        user_id = doc.id
        
        if 'hunger' in data and 'lastUpdate' in data:
            last_update_ts = data['lastUpdate'].timestamp()
            seconds_passed = time.time() - last_update_ts
            
            # 1% за 10 минут
            lost_hunger = int(seconds_passed / 600)
            current_hunger = data['hunger'] - lost_hunger
            
            print(f"Пользователь {user_id}: Голод ~{current_hunger}%")

            # Если голод низкий (для теста поставим < 95%)
            if 0 < current_hunger < 95:
                try:
                    bot.send_message(user_id, "Твой котик проголодался! 🍖\nЗайди покормить его!")
                    print(f"Уведомление отправлено для {user_id}")
                except Exception as e:
                    print(f"Ошибка отправки пользователю {user_id}: {e}")

if __name__ == "__main__":
    check_hunger()

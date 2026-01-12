import os
import time
import telebot
import firebase_admin
import json
from firebase_admin import credentials, firestore

# Загружаем данные из секретов GitHub
BOT_TOKEN = os.getenv('BOT_TOKEN')
FIREBASE_JSON_STR = os.getenv('FIREBASE_JSON')

# Инициализация Firebase
if not firebase_admin._apps:
    cred_dict = json.loads(FIREBASE_JSON_STR)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
bot = telebot.TeleBot(BOT_TOKEN)

def check_hunger():
    print("Проверка голода котиков...")
    users_ref = db.collection("users")
    docs = users_ref.stream()

    for doc in docs:
        data = doc.data()
        user_id = doc.id
        
        # Проверяем, есть ли данные
        if 'hunger' in data and 'lastUpdate' in data:
            # Считаем оффлайн голод
            last_update_ts = data['lastUpdate'].timestamp()
            seconds_passed = time.time() - last_update_ts
            
            # Кот теряет 1% каждые 10 минут (600 сек)
            lost_hunger = int(seconds_passed / 600)
            current_hunger = data['hunger'] - lost_hunger
            
            # Если голод низкий (от 10% до 20%), шлем уведомление
            # Мы ставим диапазон, чтобы не спамить каждую проверку
            if 10 < current_hunger < 25:
                try:
                    bot.send_message(user_id, "Твой котик проголодался! 🍖\nЗайди в игру, пока он не упал в обморок!")
                    print(f"Уведомление отправлено пользователю {user_id}")
                except Exception as e:
                    print(f"Не удалось отправить сообщение {user_id}: {e}")

if __name__ == "__main__":
    check_hunger()
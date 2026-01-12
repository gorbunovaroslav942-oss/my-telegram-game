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
    if not BOT_TOKEN or not FIREBASE_JSON_STR:
        print("Ошибка: Секреты не найдены!")
        return

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
            
            # Получаем текущие показатели
            hunger = data.get('hunger', 100)
            last_update = data.get('lastUpdate')
            # Метка: отправляли ли мы уже уведомление о низком голоде?
            was_notified = data.get('was_notified', False)

            if last_update:
                # Считаем реальный голод с учетом времени (1% в 10 минут)
                seconds_passed = time.time() - last_update.timestamp()
                lost_hunger = int(seconds_passed / 600)
                current_hunger = hunger - lost_hunger
                
                print(f"Пользователь {user_id}: Голод {current_hunger}%, Уведомлен: {was_notified}")

                # УСЛОВИЕ 1: Если кот проголодался ниже 30% и мы еще НЕ спамили
                if current_hunger <= 30 and current_hunger > 0 and not was_notified:
                    try:
                        bot.send_message(user_id, "🐾 Твой котик проголодался! (Меньше 30%)\nЗайди покормить его, пока он не загрустил! 🍖")
                        # Ставим метку в базу, что уведомление отправлено
                        db.collection("users").doc(user_id).update({"was_notified": True})
                        print(f"Уведомление отправлено для {user_id}")
                    except Exception as e:
                        print(f"Ошибка отправки: {e}")
                
                # УСЛОВИЕ 2: Если кота покормили (голод стал выше 80%), сбрасываем метку для следующего раза
                elif current_hunger > 80 and was_notified:
                    db.collection("users").doc(user_id).update({"was_notified": False})
                    print(f"Метка уведомления сброшена для {user_id}")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    run_notify()

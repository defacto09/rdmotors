import os
import sqlite3
import logging
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MANAGER_ID = os.getenv("MANAGER_ID")

MESSAGE_LIMIT = 5
TIME_LIMIT = timedelta(minutes=1)
user_message_count = defaultdict(list)

# 📦 Ініціалізація SQLite
def init_db():
    conn = sqlite3.connect('client_messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_id INTEGER,
            username TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logger.debug("SQLite база даних ініціалізована.")

def init_car_status_db():
    conn = sqlite3.connect('car_status.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_status (
            vin TEXT PRIMARY KEY,
            status TEXT,
            updated_at TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logger.debug("SQLite база даних car ініціалізовано")

# 💾 Збереження повідомлення в SQLite
def save_message_to_db(user_id, username, message_text):
    try:
        conn = sqlite3.connect('client_messages.db')
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO messages (timestamp, user_id, username, message)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, user_id, username, message_text))
        conn.commit()
        logger.debug(f"Збережено повідомлення від @{username} (ID: {user_id})")
    except Exception as e:
        logger.error(f"Не вдалося зберегти повідомлення в БД: {e}")
    finally:
        conn.close()

# 🔒 Антиспам
def is_spam(user_id):
    now = datetime.now()
    user_message_count[user_id] = [t for t in user_message_count[user_id] if now - t < TIME_LIMIT]
    if len(user_message_count[user_id]) >= MESSAGE_LIMIT:
        return True
    user_message_count[user_id].append(now)
    return False

async def update_vin_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MANAGER_ID:
        await update.message.reply_text("❌ У вас немає доступу.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Формат: /vinstatus <VIN> <статус>")
        return

    vin = context.args[0].upper()
    status = " ".join(context.args[1:])
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = sqlite3.connect('car_status.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO car_status (vin, status, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(vin) DO UPDATE SET status = excluded.status, updated_at = excluded.updated_at
        ''', (vin, status, now))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ Статус для VIN {vin} оновлено:\n📍 {status}")
    except Exception as e:
        logger.error(f"Помилка при оновленні car_status: {e}")
        await update.message.reply_text("⚠️ Не вдалося оновити статус.")

def get_car_status_by_vin(vin):
    try:
        conn = sqlite3.connect('car_status.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status, updated_at FROM car_status WHERE vin = ?", (vin,))
        result = cursor.fetchone()
        conn.close()
        if result:
            logger.debug(f"Знайдений статус для VIN {vin}: {result}")
        else:
            logger.debug(f"Не знайдено статусу для VIN {vin}")
        return result
    except Exception as e:
        logger.error(f"Помилка при пошуку VIN у car_status.db: {e}")
        return None


# 📩 Обробка повідомлень
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    username = user.username or "(без username)"

    if is_spam(user_id):
        await update.message.reply_text("❗ Ви перевищили ліміт повідомлень. Спробуйте пізніше.")
        return

    elif len(text) == 17 and text.isalnum():
        result = get_car_status_by_vin(text.upper())
        if result:
            status, updated = result
            await update.message.reply_text(
                f"🔎 Статус авто (VIN: {text.upper()}):\n📍 {status}\n🕒 Оновлено: {updated}")
        else:
            await update.message.reply_text(
                "⚠️ Авто з таким VIN-кодом не знайдено в базі. Зачекайте оновлення менеджером.")

    keyboard_texts = [
        "📥 Хочу авто зі США", "❓FAQ", "📞 Контакт",
        "📋 В наявності", "🚗 Де авто?"
    ]

    if user_id != MANAGER_ID:
        save_message_to_db(user_id, username, text)

        msg = f"✉️ Повідомлення від @{username} (ID: {user_id}):\n{text}"
        try:
            await context.bot.send_message(chat_id=MANAGER_ID, text=msg)
        except Exception as e:
            logger.error(f"Не вдалося переслати менеджеру: {e}")

        lowered = text.lower()

        if text in keyboard_texts:
            if "де авто" in lowered:
                await update.message.reply_text("🚗 Щоб дізнатись статус доставки, надайте VIN-код або номер замовлення.")
            elif "хочу авто зі сша" in lowered:
                await update.message.reply_text(
                    "👋 Щоб розпочати процес доставки авто, заповніть форму: https://forms.gle/BXkuZr9C5qEJHijd7\n\n"
                    "❗️Обов'язково ознайомтесь з нашим договором перед заповненням! /agreement"
                )
            elif "контакт" in lowered or "телефон" in lowered:
                await update.message.reply_text("📞 Наш менеджер зв'яжеться з вами. Телефон: +380673951195")
            elif "в наявності" in lowered or "які авто" in lowered:
                cars = [
                    {"photo": "available_cars/bmwx5.jpg", "caption": "BMW X5 2013, $17,200"},
                    {"photo": "available_cars/audia4.jpg", "caption": "Audi A4 2017, $24,500"},
                    {"photo": "available_cars/tiguan.jpg", "caption": "Volkswagen Tiguan 2018, $22,700"}
                ]
                for car in cars:
                    try:
                        with open(car["photo"], "rb") as photo_file:
                            await update.message.reply_photo(photo=photo_file, caption=car["caption"])
                    except Exception as e:
                        logger.error(f"Не вдалося надіслати фото {car['photo']}: {e}")
            elif "faq" in lowered or "питання" in lowered:
                await update.message.reply_text("❓ Щоб дізнатись статус замовлення, натисніть '🚗 Де авто?'")
        else:
            await update.message.reply_text("✅ Ваше повідомлення надіслано менеджеру.")
    else:
        pass  # менеджер нічого не робить тут

# 📄 Відправка договору
async def agreement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = "https://docs.google.com/document/d/1VSmsVevCBc0BCSVnsJgdkwlZRWDY_hhjIbcnzPpsOVg/edit?usp=sharing/view"
    await update.message.reply_text(
        f"📄 Ось наш договір:\n\n[Посилання]({link})",
        parse_mode="Markdown"
    )

# 🧾 Показ останніх повідомлень
async def show_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MANAGER_ID:
        await update.message.reply_text("❌ У вас немає доступу.")
        return

    try:
        conn = sqlite3.connect('client_messages.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, user_id, username, message
            FROM messages
            ORDER BY id DESC
            LIMIT 10
        ''')
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await update.message.reply_text("⚠️ Повідомлень ще немає.")
            return

        text = "🗂 Останні 10 повідомлень:\n\n"
        for row in rows:
            ts, uid, uname, msg = row
            text += f"🕒 {ts}\n👤 @{uname} (ID: {uid})\n💬 {msg}\n\n"

        await update.message.reply_text(text[:4096])
    except Exception as e:
        logger.error(f"Помилка при читанні з БД: {e}")
        await update.message.reply_text("⚠️ Не вдалося отримати повідомлення з бази.")

# 🔁 Відповідь менеджера користувачу
async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MANAGER_ID:
        await update.message.reply_text("❌ У вас немає доступу.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Формат: /reply <user_id> <текст>")
        return

    user_id = context.args[0]
    reply_text = " ".join(context.args[1:])
    try:
        await context.bot.send_message(chat_id=int(user_id), text=f"📩 Відповідь від менеджера:\n{reply_text}")
        await update.message.reply_text("✅ Повідомлення надіслано.")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"⚠️ Не вдалося надіслати повідомлення: {e}")

# 🔘 Кнопки
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["📥 Хочу авто зі США", "❓FAQ"],
        ["🚗 Де авто?", "📞 Контакт"],
        ["📋 В наявності"]
    ], resize_keyboard=True)

# ▶️ Команда старту
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Вас вітає підтримка RDMOTORS. Оберіть дію або напишіть повідомлення.",
        reply_markup=get_main_keyboard()
    )

# 🚀 Запуск
def main():
    init_db()  # Ініціалізуємо базу
    init_car_status_db() # Ініціалізуємо базу даних статусу авто
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agreement", agreement))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(CommandHandler("messages", show_messages))
    app.add_handler(CommandHandler("vinstatus", update_vin_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    logger.info("Бот запущено.")
    app.run_polling()

if __name__ == "__main__":
    main()

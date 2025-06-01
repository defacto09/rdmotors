import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

# Створення базового класу для моделей
Base = declarative_base()

# Створення таблиць через SQLAlchemy
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, index=True)
    username = Column(String)
    message = Column(String)

class CarStatus(Base):
    __tablename__ = 'car_status'

    vin = Column(String, primary_key=True)
    status = Column(String)
    updated_at = Column(DateTime)

# Налаштування пулу підключень до SQLite
DATABASE_URL = "sqlite:///database/rdmotors.db"

# Створюємо engine для з'єднання з базою даних
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10, echo=True)

# Створюємо сесію
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функція для отримання сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Створення таблиць, якщо вони ще не існують
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MANAGER_ID = int(os.getenv("MANAGER_ID"))

MESSAGE_LIMIT = 7
TIME_LIMIT = timedelta(minutes=1)
user_message_count = defaultdict(list)

def save_message_to_db(user_id, username, message_text):
    try:
        # Отримуємо сесію
        with SessionLocal() as db:
            # Створюємо новий об'єкт повідомлення
            message = Message(
                user_id=user_id,
                username=username,
                message=message_text,
                timestamp=datetime.now()
            )
            # Додаємо повідомлення до сесії
            db.add(message)
            # Комітимо зміни
            db.commit()
            # Оновлюємо об'єкт після коміту, щоб отримати id
            db.refresh(message)
            logger.info(f"Повідомлення від @{username} успішно збережене.")
    except Exception as e:
        logger.error(f"Помилка при збереженні повідомлення в базу: {e}")


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
    now = datetime.now()

    try:
        with SessionLocal() as db:  # Отримуємо сесію з пулу
            existing_car_status = db.query(CarStatus).filter(CarStatus.vin == vin).first()

            if existing_car_status:
                existing_car_status.status = status
                existing_car_status.updated_at = now
            else:
                car_status = CarStatus(vin=vin, status=status, updated_at=now)
                db.add(car_status)

            db.commit()
            db.refresh(existing_car_status or car_status)

        await update.message.reply_text(f"✅ Статус для VIN {vin} оновлено:\n📍 {status}")
    except Exception as e:
        logger.error(f"Помилка при оновленні car_status: {e}")
        await update.message.reply_text("⚠️ Не вдалося оновити статус.")

def get_car_status_by_vin(vin):
    try:
        with SessionLocal() as db:  # Отримуємо сесію з пулу
            car_status = db.query(CarStatus).filter(CarStatus.vin == vin).first()
            if car_status:
                logger.debug(f"Знайдений статус для VIN {vin}: {car_status.status}")
                return car_status.status, car_status.updated_at
            else:
                logger.debug(f"Не знайдено статусу для VIN {vin}, або ще немає інформації")

                db.commit()
        return None
    except Exception as e:
        logger.error(f"Помилка при пошуку VIN у car_status.db: {e}")
        return None

# 📩 Обробка повідомлень
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    username = user.username or "(без username)"

    # 🔒 Антиспам
    if is_spam(user_id):
        await update.message.reply_text("❗ Ви перевищили ліміт повідомлень. Спробуйте пізніше.")
        return


    # 🔍 Перевірка, чи це VIN-код
    if len(text) == 17 and text.isalnum():
        result = get_car_status_by_vin(text.upper())
        if result:
            status, updated = result

            # Розділяємо статус на крайню й наступну локацію
            parts = status.split("|")
            last_location = parts[0].strip() if len(parts) > 0 else "Невідомо"
            next_location = parts[1].strip() if len(parts) > 1 else "Невідомо"

            await update.message.reply_text(
                f"🚗 *Статус авто*\n"
                f"🔎 *VIN:* `{text.upper()}`\n"
                f"📍 *Крайня локація:* {last_location}\n"
                f"🧭 *Наступна зупинка:* {next_location}\n"
                f"🕒 *Оновлено:* {updated.strftime('%d/%m/%Y %H:%M')}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "⚠️ Авто з таким VIN-кодом не знайдено в базі. Зачекайте оновлення менеджером.")
        return

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
                    "❗️Обов'язково ознайомтесь з нашим договором перед заповненням!\n /договір\n\n"
                    "👋 Щоб розпочати процес доставки авто, заповніть форму\n /форма"
                )
            elif "контакт" in lowered or "телефон" in lowered:
                await update.message.reply_text("📞 Наш менеджер зв'яжеться з вами. Телефон: +380673951195")
            elif "в наявності" in lowered or "які авто" in lowered:
                cars = [
                    {"photo": "available_cars/bmwx5.jpg", "caption": "BMW X5 2013, $17,200"},
                    {"photo": "available_cars/audia4.jpg", "caption": "Audi A4 2017, $24,500"},
                    {"photo": "available_cars/tiguan.jpg", "caption": "Volkswagen Tiguan 2018, $22,700"},
                    {"photo": "available_cars/sonata2020.jpg", "caption": "Hyundai Sonata 2020, $23,500"},
                    {"photo": "available_cars/sonata400.jpg", "caption": "Hyundai Sonata 2016, $7500$"},
                    {"photo": "available_cars/megane3.jpg", "caption": "Renault Megane 3"}
                ]
                for car in cars:
                    try:
                        with open(car["photo"], "rb") as photo_file:
                            await update.message.reply_photo(photo=photo_file, caption=car["caption"])
                    except Exception as e:
                        logger.error(f"Не вдалося надіслати фото {car['photo']}: {e}")
            elif "faq" in lowered or "питання" in lowered:
                        link = "https://docs.google.com/document/d/1VSmsVevCBc0BCSVnsJgdkwlZRWDY_hhjIbcnzPpsOVg/edit?usp=sharing"
                        await update.message.reply_text(
                            f"🚙 Натиснувши *'📥 Хочу авто зі США'* ви зможете розпочати процес покупки авто.\n\n"
                            f"❓ Щоб дізнатись статус замовлення, натисніть *'🚗 Де авто?'*.\n\n"
                            f"💵 Всі ціни залежать від багатьох факторів, щоб більше дізнатись про це, перегляньте наш [договір]({link}).\n\n"
                            f"☎️ Якщо ви хочете термінову відповідь по вашому запиті, то можете звернутись за контактом у *📞 Контакт*\n\n"
                            f"🚘 Бажаєте дізнатись про наявні авто RDMOTORS у продажі? Знайдете відповідь у *'📋 В наявності'*\n\n"
                            f"_За інакшими питаннями пишіть в чат, менеджер зв'яжеться з вами_",
                            parse_mode="Markdown",
                            disable_web_page_preview = True
                        )
        else:
            await update.message.reply_text("✅ Ваше повідомлення надіслано менеджеру.")
    else:
        pass  # менеджер нічого не робить тут

# 📄 Відправка договору
async def agreement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = "https://docs.google.com/document/d/1VSmsVevCBc0BCSVnsJgdkwlZRWDY_hhjIbcnzPpsOVg/edit?usp=sharing/view"
    await update.message.reply_text(
        f"📄 Ось наш договір:\n\n[Посилання]({link})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# 🧾 Показ останніх повідомлень
async def get_last_messages(update: Update, context: ContextTypes.DEFAULT_TYPE, limit=10):
    try:
        with SessionLocal() as db:
            messages = db.query(Message).order_by(Message.id.desc()).limit(limit).all()
        if not messages:
            await update.message.reply_text("⚠️ Повідомлень ще немає.")
            return

        text = "🗂 Останні 10 повідомлень:\n\n"
        for m in messages:
            text += f"🕒 {m.timestamp}\n👤 @{m.username} (ID: {m.user_id})\n💬 {m.message}\n\n"

        await update.message.reply_text(text[:4096])
    except Exception as e:
        logger.error(f"Помилка при запиті: {e}")
        await update.message.reply_text("⚠️ Не вдалося отримати повідомлення з бази.")
# Відповідь менеджера користувачу
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
    if not API_TOKEN:
        logger.error("❌ Не задано TELEGRAM_API_TOKEN у .env")
        return
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("договір", agreement))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(CommandHandler("messages", get_last_messages))
    app.add_handler(CommandHandler("vinstatus", update_vin_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    logger.info("Бот запущено.")
    app.run_polling()

if __name__ == "__main__":
    main()
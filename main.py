import os
import logging
import shutil
import pathlib
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import quote_plus

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Get config from .env
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MANAGER_ID = int(os.getenv("MANAGER_ID"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# ============================================================================
# DATABASE SETUP - SHARED WITH API
# ============================================================================

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, index=True)
    username = Column(String(100))
    message = Column(Text)


class CarStatus(Base):
    __tablename__ = 'car_status'

    vin = Column(String(17), primary_key=True)
    status = Column(String(500))
    container_number = Column(String(50))
    updated_at = Column(DateTime, default=datetime.utcnow)


class BotUser(Base):
    __tablename__ = 'bot_users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    first_name = Column(String(100))
    is_manager = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


# MySQL Connection (Same as API!)
db_password_escaped = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{db_password_escaped}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Test connection before use
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables on startup
Base.metadata.create_all(bind=engine)
logger.info(f"✅ Connected to MySQL database: {DB_NAME}")

# ============================================================================
# ANTI-SPAM CONFIG
# ============================================================================

MESSAGE_LIMIT = 7
TIME_LIMIT = timedelta(minutes=1)
user_message_count = defaultdict(list)


def is_spam(user_id):
    """Check if user is spamming"""
    now = datetime.now()
    user_message_count[user_id] = [t for t in user_message_count[user_id] if now - t < TIME_LIMIT]
    if len(user_message_count[user_id]) >= MESSAGE_LIMIT:
        return True
    user_message_count[user_id].append(now)
    return False


# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def save_message_to_db(user_id, username, message_text):
    """Save user message to MySQL"""
    db = SessionLocal()
    try:
        message = Message(
            user_id=user_id,
            username=username,
            message=message_text,
            timestamp=datetime.now()
        )
        db.add(message)
        db.commit()
        logger.info(f"✅ Message from @{username} saved to MySQL")
    except Exception as e:
        logger.error(f"❌ Error saving message: {e}")
        db.rollback()
    finally:
        db.close()


def get_car_status_by_vin(vin):
    """Get car status from MySQL by VIN"""
    db = SessionLocal()
    try:
        car_status = db.query(CarStatus).filter(CarStatus.vin == vin).first()
        if car_status:
            logger.debug(f"✅ Знайшли статус для цього VIN {vin}")
            return car_status.status, car_status.container_number, car_status.updated_at
        else:
            logger.debug(f"⚠️ Нічого не знайдено за вашим запитом {vin}")
        return None
    except Exception as e:
        logger.error(f"❌ Error querying car status: {e}")
        return None
    finally:
        db.close()


def save_bot_user(user_id, username, first_name, is_manager=0):
    """Save or update bot user"""
    db = SessionLocal()
    try:
        existing = db.query(BotUser).filter(BotUser.user_id == user_id).first()
        if existing:
            existing.username = username
            existing.first_name = first_name
        else:
            bot_user = BotUser(
                user_id=user_id,
                username=username,
                first_name=first_name,
                is_manager=is_manager
            )
            db.add(bot_user)
        db.commit()
    except Exception as e:
        logger.error(f"❌ Error saving bot user: {e}")
        db.rollback()
    finally:
        db.close()

# ============================================================================
# MESSAGE HANDLER
# ============================================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    save_bot_user(user.id, user.username or "unknown", user.first_name or "User")
    await update.message.reply_text(
        "👋 Привіт! Вас вітає підтримка RDMOTORS. Оберіть дію або напишіть повідомлення.",
        reply_markup=get_main_keyboard()
    )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    save_bot_user(user.id, user.username or "unknown", user.first_name or "User")
    await update.message.reply_text(
        "👋 Привіт! Вас вітає підтримка RDMOTORS. Оберіть дію або напишіть повідомлення.",
        reply_markup=get_main_keyboard()
    )

async def dogovir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send agreement link"""
    link = "https://docs.google.com/document/d/1VSmsVevCBc0BCSVnsJgdkwlZRWDY_hhjIbcnzPpsOVg/edit?usp=sharing"
    await update.message.reply_text(
        f"📄 Ось наш договір:\n\n[Link]({link})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def forma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send form link"""
    link = "https://forms.gle/BXkuZr9C5qEJHijd7"
    await update.message.reply_text(
        f"📄 Ось наша форма:\n\n[Link]({link})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def update_vin_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manager command: Update car status by VIN"""
    if update.effective_user.id != MANAGER_ID:
        await update.message.reply_text("❌ Access denied.")
        return

    full_text = update.message.text
    parts = full_text.split(maxsplit=3)
    if len(parts) < 4:
        await update.message.reply_text("⚠️ Format: /vinstatus <VIN> <container> <status>")
        return

    vin = parts[1].upper()
    container = parts[2]
    status = parts[3]
    now = datetime.now()

    db = SessionLocal()
    try:
        existing = db.query(CarStatus).filter(CarStatus.vin == vin).first()
        if existing:
            existing.status = status
            existing.container_number = container
            existing.updated_at = now
        else:
            car_status = CarStatus(
                vin=vin,
                status=status,
                container_number=container,
                updated_at=now
            )
            db.add(car_status)

        db.commit()
        await update.message.reply_text(
            f"✅ Status updated for VIN {vin}:\n📦 Container: {container}\n📍 Status: {status}"
        )
        logger.info(f"✅ VIN {vin} status updated")
    except Exception as e:
        logger.error(f"❌ Error updating VIN status: {e}")
        db.rollback()
        await update.message.reply_text("⚠️ Failed to update status.")
    finally:
        db.close()

async def get_last_messages(update: Update, context: ContextTypes.DEFAULT_TYPE, limit=10):
    """Manager command: View last messages"""
    if update.effective_user.id != MANAGER_ID:
        await update.message.reply_text("❌ Access denied.")
        return

    db = SessionLocal()
    try:
        messages = db.query(Message).order_by(Message.id.desc()).limit(limit).all()
        if not messages:
            await update.message.reply_text("⚠️ No messages yet.")
            return

        text = "🗂 Last 10 messages:\n\n"
        for m in messages:
            text += f"🕒 {m.timestamp}\n👤 @{m.username} (ID: {m.user_id})\n💬 {m.message}\n\n"

        await update.message.reply_text(text[:4096])
    except Exception as e:
        logger.error(f"❌ Error querying messages: {e}")
        await update.message.reply_text("⚠️ Failed to retrieve messages.")
    finally:
        db.close()

async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manager command: Reply to user"""
    if update.effective_user.id != MANAGER_ID:
        await update.message.reply_text("❌ Access denied.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Format: /reply <user_id> <text>")
        return

    user_id = context.args[0]
    reply_text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"📩 Reply from manager:\n{reply_text}"
        )
        await update.message.reply_text("✅ Message sent.")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        await update.message.reply_text(f"⚠️ Failed to send: {e}")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    username = user.username or user.first_name or "(No name)"

    save_bot_user(user_id, user.username, user.first_name)

    if is_spam(user_id):
        await update.message.reply_text("❗ Ви перевищили ліміт повідомлень. Спробуйте пізніше.")
        return

    if len(text) == 17 and text.isalnum():
        result = get_car_status_by_vin(text.upper())
        if result:
            status, container_number, updated = result
            parts = status.split("|")
            last_location = parts[0].strip() if len(parts) > 0 and parts[0].strip() else "Невідомо"
            next_location = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "Невідомо"
            await update.message.reply_text(
                f"🚗 *Статус авто*\n"
                f"🔎 *VIN:* `{text.upper()}`\n"
                f"🔎 *МОРСЬКА ЛІНІЯ:* `MSC`\n"
                f"📦 *Контейнер:* {container_number}\n"
                f"📍 *Крайня локація:* {last_location}\n"
                f"🧭 *Наступна зупинка:* {next_location}\n"
                f"🕒 Актуально на: {updated.strftime('%d.%m.%Y %H:%M')}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "⚠️ Авто з таким VIN-кодом не знайдено в базі. Зачекайте оновлення менеджером."
            )
        return

    keyboard_texts = [
        "📥 Хочу авто зі США", "❓FAQ", "📞 Контакт",
        "📋 В наявності", "🚗 Де авто?"
    ]
    lowered = text.lower()
    if text in keyboard_texts:
        if "де авто" in lowered:
            await update.message.reply_text(
                "🚗 Щоб дізнатись статус доставки, надайте VIN-код або номер замовлення."
            )
        elif "хочу авто зі сша" in lowered:
            await update.message.reply_text(
                "❗Обов'язково ознайомтесь з нашим договором перед заповненням!\n\n"
                "👋 Щоб розпочати процес доставки авто, заповніть форму\n\n"
                "/dogovir\n\n"
                "/forma"
            )
        elif "контакт" in lowered or "телефон" in lowered:
            await update.message.reply_text("📞 Наш менеджер зв'яжеться з вами. Телефон: +380673951195")
        elif "в наявності" in lowered or "які авто" in lowered or "📋" in text:
            cars = [
                {"photo": "available_cars/sonata2021.jpg", "caption": "Hyundai Sonata 2021, $24,000"}
            ]
            for car in cars:
                try:
                    with open(car["photo"], "rb") as photo_file:
                        await update.message.reply_photo(photo=photo_file, caption=car["caption"])
                except Exception as e:
                    logger.error(f"Не вдалося надіслати фото {car['photo']}: {e}")
        elif "faq" in lowered or "питання" in lowered or "❓" in text:
            link = "https://docs.google.com/document/d/1VSmsVevCBc0BCSVnsJgdkwlZRWDY_hhjIbcnzPpsOVg/edit?usp=sharing"
            await update.message.reply_text(
                f"🚙 Натиснувши *'📥 Хочу авто зі США'* ви зможете розпочати процес покупки авто.\n\n"
                f"❓ Щоб дізнатись статус замовлення, натисніть *'🚗 Де авто?'*.\n\n"
                f"💵 Всі ціни залежать від багатьох факторів, а щоб більше дізнатися про це, перегляньте наш [договір]({link}).\n\n"
                f"☎️ Якщо вам потрібна термінова відповідь по запиту, зверніться за контактом у *📞 Контакт*.\n\n"
                f"🚘 Щоб дізнатись про наявні авто RDMOTORS у продажі — дивіться *'📋 В наявності'*.\n\n"
                f"_Якщо виникли питання — пишіть у чат, менеджер зв'яжеться з вами._",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        return

    # --- Якщо не спрацював жоден сценарій меню ---
    save_message_to_db(user_id, username, text)
    msg = f"✉️ Повідомлення від @{username} (ID: {user_id}):\n{text}"
    try:
        await context.bot.send_message(chat_id=MANAGER_ID, text=msg)
    except Exception as e:
        logger.error(f"Не вдалося переслати менеджеру: {e}")
    await update.message.reply_text("✅ Ваше повідомлення надіслано менеджеру.")

# ============================================================================
# KEYBOARD LAYOUT
# ============================================================================

def get_main_keyboard():
    """Main menu keyboard"""
    return ReplyKeyboardMarkup([
        ["📥 Хочу авто зі США", "❓FAQ"],
        ["🚗 Де авто?", "📞 Контакт"],
        ["📋 В наявності"]
    ], resize_keyboard=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Start the bot"""
    if not API_TOKEN:
        logger.error("❌ TELEGRAM_API_TOKEN not set in .env")
        return

    if not MANAGER_ID:
        logger.error("❌ MANAGER_ID not set in .env")
        return

    app = Application.builder().token(API_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dogovir", dogovir))
    app.add_handler(CommandHandler("forma", forma))
    app.add_handler(CommandHandler("vinstatus", update_vin_status))
    app.add_handler(CommandHandler("messages", get_last_messages))
    app.add_handler(CommandHandler("reply", reply_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    logger.info("🚀 Bot started successfully!")
    app.run_polling()


if __name__ == "__main__":
    main()

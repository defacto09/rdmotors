import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

API_TOKEN = "7805771710:AAHa5zCA6qNgo1Q_5eOaqeYZNJUavqRxpSc"
MANAGER_ID = 1376857543  # Ваш ID менеджера

# Авторизація Google Sheets

def authorize_message_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "/Users/defacto092/Downloads/RDMotors IAM Admin.json", scope)
    return gspread.authorize(creds)

# Отримання даних авто

def get_spreadsheet_data():
    try:
        client = authorize_message_sheet()
        sheet = client.open("test").sheet1
        data = sheet.get_all_records(expected_headers=["АВТО", "ЦІНА"])

        formatted = "🔹 *База даних авто:* 🔹\n\n"
        for r in data:
            formatted += f"🚗 *{r['АВТО']}*\n💰 *Ціна:* {r['ЦІНА']}$\n\n"
        return formatted
    except Exception as e:
        logger.error(f"Помилка при отриманні даних з Google Sheets: {e}")
        return "⚠️ Сталася помилка при отриманні даних з бази авто."

# Збереження повідомлень у Google Sheets

def save_message_to_db(user_id, username, message_text):
    try:
        client = authorize_message_sheet()
        sheet = client.open("ClientMessages").sheet1
        sheet.append_row([str(datetime.now()), user_id, username, message_text])
        logger.info("Повідомлення додано до бази даних повідомлень.")
    except Exception as e:
        logger.error(f"Не вдалося зберегти повідомлення: {e}")

# Обробка повідомлень

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    username = user.username or "(без username)"

    keyboard_texts = [
        "📥 Пригін авто", "💰 Ціна", "📞 Контакт",
        "📋 В наявності", "🚗 Де авто?"
    ]

    if text not in keyboard_texts and user_id != MANAGER_ID:
        save_message_to_db(user_id, username, text)
        msg = f"✉️ Повідомлення від @{username} (ID: {user_id}):\n{text}"
        try:
            await context.bot.send_message(chat_id=MANAGER_ID, text=msg)
            await update.message.reply_text("✅ Повідомлення надіслано менеджеру. Очікуйте відповідь.")
        except Exception as e:
            logger.error(f"Не вдалося переслати менеджеру: {e}")
            await update.message.reply_text("⚠️ Сталася помилка при відправці повідомлення.")
        return

    lowered = text.lower()
    if "де авто" in lowered or "статус доставки" in lowered:
        reply_text = (
            "🚗 Щоб дізнатись статус доставки, надайте VIN-код або номер замовлення.\n"
            "Ми перевіримо і зателефонуємо вам найближчим часом."
        )
        if "де авто" in lowered:
            reply_text += "\n📍 Якщо авто ще не на місці, ми надамо вам точну інформацію."
        await update.message.reply_text(reply_text)
    elif "пригін авто" in lowered:
        await update.message.reply_text(
            "👋 Щоб розпочати процес пригону авто, заповніть форму: https://forms.gle/BXkuZr9C5qEJHijd7")
    elif "ціна" in lowered:
        await update.message.reply_text("💰 Ціни залежать від авто. Напишіть, яка марка вас цікавить.")
    elif "контакт" in lowered or "телефон" in lowered:
        await update.message.reply_text("📞 Наш менеджер зателефонує найближчим часом. Телефон: +380XXXXXXXXX")
    elif "в наявності" in lowered or "які авто" in lowered:
        await update.message.reply_text("📋 Ось список авто:\nНатисніть /database")

# Команда /database

async def database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_spreadsheet_data()
    await update.message.reply_text(data, parse_mode="Markdown")

# Команда /history

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id != MANAGER_ID:
        await update.message.reply_text("❌ У вас немає доступу до цієї команди.")
        return

    client = authorize_message_sheet()
    sheet = client.open("ClientMessages").sheet1

    try:
        data = sheet.get_all_records()
    except Exception as e:
        logger.error(f"Помилка при отриманні даних з таблиці: {e}")
        await update.message.reply_text("⚠️ Сталася помилка при отриманні історії повідомлень.")
        return

    if not data:
        await update.message.reply_text("❌ Немає повідомлень в історії.")
        return

    user_history = [row for row in data if str(row.get('User ID')) == str(user_id)]

    if not user_history:
        await update.message.reply_text("❌ Немає історії повідомлень для вашого ID.")
        return

    history_text = "📝 Ваші повідомлення:\n\n"
    for row in user_history:
        timestamp = row.get('Timestamp', 'Невідомо')
        message = row.get('Message', 'Немає повідомлення')
        history_text += f"🕒 {timestamp} - {message}\n"

    await update.message.reply_text(history_text)

# Клавіатура

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["📥 Пригін авто", "💰 Ціна"],
        ["🚗 Де авто?", "📞 Контакт"],
        ["📋 В наявності"]
    ], resize_keyboard=True)

# Стартова команда

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Вас вітає підтримка RDMOTORS! Оберіть одне з частих питань або напишіть своє.",
        reply_markup=get_main_keyboard()
    )

# Команда /reply

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

# Головна функція

def main():
    app = Application.builder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("database", database))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    app.run_polling()

if __name__ == "__main__":
    main()

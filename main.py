import os
import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
MANAGER_ID = 1376857543  # Ваш ID менеджера

# Авторизація Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.getenv("GOOGLE_CREDS_PATH"), scope)
gs_client = gspread.authorize(creds)

# Отримання даних авто
def get_spreadsheet_data():
    try:
        sheet = gs_client.open("test").sheet1
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
        sheet = gs_client.open("ClientMessages").sheet1
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
        "📥 Хочу авто зі США", "❓FAQ", "📞 Контакт",
        "📋 В наявності", "🚗 Де авто?"
    ]

    # Якщо це клієнт (не менеджер)
    if user_id != MANAGER_ID:
        # Зберігаємо повідомлення
        save_message_to_db(user_id, username, text)

        # Пересилаємо менеджеру
        msg = f"✉️ Повідомлення від @{username} (ID: {user_id}):\n{text}"
        try:
            await context.bot.send_message(chat_id=MANAGER_ID, text=msg)
        except Exception as e:
            logger.error(f"Не вдалося переслати менеджеру: {e}")

        lowered = text.lower()

        # Якщо натиснув кнопку — даємо відповідь по кнопці
        if text in keyboard_texts:
            if "де авто" in lowered:
                await update.message.reply_text(
                    "🚗 Щоб дізнатись статус доставки, надайте VIN-код або номер замовлення.\nМи перевіримо і повідомимо вам найближчим часом."
                )
            elif "хочу авто зі сша" in lowered:
                await update.message.reply_text(
                    "👋 Щоб розпочати процес доставки авто, заповніть форму: https://forms.gle/BXkuZr9C5qEJHijd7 "
                    "\n\n ❗️Обов'язково прогляньте наш договір перед тим як заповнювати анкету! \n Натисніть: /agreement"
                )
            elif "контакт" in lowered or "телефон" in lowered:
                await update.message.reply_text("📞 Наш менеджер зателефонує найближчим часом. Телефон: +380673951195")
            elif "в наявності" in lowered or "які авто" in lowered:
                await update.message.reply_text("📋 Ось список авто:\nНатисніть /database")
            elif "faq" in lowered or "питання" in lowered:
                await update.message.reply_text("Ром, де машина? - виберіть кнопку 'де авто', і ми надамо вам відповідь")
        else:
            # Якщо це не кнопка — пишемо про надсилання повідомлення
            await update.message.reply_text("✅ Повідомлення надіслано менеджеру. Очікуйте відповідь.")

    # Якщо це менеджер
    else:
        pass

# Команда /agreement для надсилання посилання на Google Docs документ
# Команда /agreement для надсилання посилання на Google Docs документ з гіперпосиланням
async def agreement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    agreement_link = "https://docs.google.com/document/d/1VSmsVevCBc0BCSVnsJgdkwlZRWDY_hhjIbcnzPpsOVg/edit?usp=sharing/view"  # Замінити на реальний ID документа
    await update.message.reply_text(
        f"📄 Ось наш договір \n\n [Посилання]({agreement_link})\n\nПеред тим як заповнити форму, будь ласка, ознайомтесь з умовами договору.",
        parse_mode="Markdown"
    )

# Клавіатура
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["📥 Хочу авто зі США", "❓FAQ"],
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
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(CommandHandler("agreement", agreement))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    app.run_polling()

if __name__ == "__main__":
    main()

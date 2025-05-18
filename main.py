
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# הגדרת לוגים
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# טעינת הנתונים מקובץ JSON
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# חיפוש תשובה לשאלה
def find_answer(question, data):
    question = question.strip()
    for item in data:
        item_question = item['query'].strip()
        if question == item_question or question in item_question or item_question in question:
            return item['answer']
    return "אני עדיין לא יודע את התשובה לשאלה הזו."

# טוקן של הבוט (החלף ב־TOKEN שלך)
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# נתיב לקובץ הנתונים
DATA_FILE_PATH = 'learned_data_cleaned.json'
data = load_data(DATA_FILE_PATH)

# התחלה
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('שלום, אני פה על מנת לענות לך על פי פסקי הרב יצחק יוסף שליט"א.')

# טיפול בהודעות
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = update.message.text
    answer = find_answer(question, data)
    await update.message.reply_text(answer)

# טיפול בשגיאות
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="שגיאה:", exc_info=context.error)
    await update.message.reply_text('אירעה שגיאה. אנא נסה שוב מאוחר יותר.')

# הפעלת הבוט
def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8690252361:AAFQod6BKhHdcI_Pu73glU_6YEsnE9S7DwM"
CHANNEL_USERNAME = "@tishkevicdoc"
METODICHKA_URL = "https://t.me/tishkevicdoc/141"


def check_subscription(user_id: int, context: CallbackContext) -> bool:
    try:
        member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    if check_subscription(user_id, context):
        update.message.reply_text(
            f"Привет, {first_name}! 🎉\n\n"
            f"Ты подписан на канал — держи методичку:\n\n"
            f"👉 {METODICHKA_URL}"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/tishkevicdoc")],
            [InlineKeyboardButton("✅ Я подписался!", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"Привет, {first_name}! 👋\n\n"
            f"Чтобы получить методичку, нужно подписаться на канал.\n\n"
            f"1️⃣ Подпишись на канал\n"
            f"2️⃣ Нажми кнопку «Я подписался!»",
            reply_markup=reply_markup
        )


def check_sub_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    first_name = query.from_user.first_name

    if check_subscription(user_id, context):
        query.edit_message_text(
            f"Отлично, {first_name}! Подписка подтверждена 🎉\n\n"
            f"Держи методичку:\n\n"
            f"👉 {METODICHKA_URL}"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/tishkevicdoc")],
            [InlineKeyboardButton("✅ Я подписался!", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "❌ Ты ещё не подписан на канал.\n\n"
            "Подпишись и нажми кнопку снова!",
            reply_markup=reply_markup
        )


def handle_message(update: Update, context: CallbackContext):
    start(update, context)


def main():
    updater = Updater(token=BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_sub_callback, pattern="check_sub"))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    logger.info("Бот запущен!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

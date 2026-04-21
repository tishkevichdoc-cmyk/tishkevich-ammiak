import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8690252361:AAFQod6BKhHdcI_Pu73glU_6YEsnE9S7DwM"
CHANNEL_USERNAME = "@tishkevicdoc"
METODICHKA_URL = "https://t.me/tishkevicdoc/141"


async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    is_subscribed = await check_subscription(user_id, context)

    if is_subscribed:
        await update.message.reply_text(
            f"Привет, {first_name}! 🎉\n\n"
            f"Ты подписан на канал — держи методичку:\n\n"
            f"👉 {METODICHKA_URL}"
        )
    else:
        keyboard = [[InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/tishkevicdoc")]]
        keyboard.append([InlineKeyboardButton("✅ Я подписался!", callback_data="check_sub")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Привет, {first_name}! 👋\n\n"
            f"Чтобы получить методичку, нужно подписаться на канал.\n\n"
            f"1️⃣ Подпишись на канал\n"
            f"2️⃣ Нажми кнопку «Я подписался!»",
            reply_markup=reply_markup
        )


async def check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    first_name = query.from_user.first_name
    is_subscribed = await check_subscription(user_id, context)

    if is_subscribed:
        await query.edit_message_text(
            f"Отлично, {first_name}! Подписка подтверждена 🎉\n\n"
            f"Держи методичку:\n\n"
            f"👉 {METODICHKA_URL}"
        )
    else:
        keyboard = [[InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/tishkevicdoc")]]
        keyboard.append([InlineKeyboardButton("✅ Я подписался!", callback_data="check_sub")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "❌ Ты ещё не подписан на канал.\n\n"
            "Подпишись и нажми кнопку снова!",
            reply_markup=reply_markup
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_sub_callback, pattern="check_sub"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()

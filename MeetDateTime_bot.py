from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Йо, напиши тут коли ми накінець зустрінемось отако: 'yyyy-mm-dd hh:mm'.")

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_time = context.user_data.get('input_time')
    if not input_time:
        await update.message.reply_text("Спершу заведи мене командою /start")
    else:
        current_time = datetime.now()
        remaining_time = input_time - current_time
        remaining_seconds = remaining_time.seconds
        days = remaining_time.days
        hours, remainder = divmod(remaining_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        message = f"Залишилось почекати до {input_time.strftime('%Y-%m-%d %H:%M')} всього лиш:\n{days} днів, {hours} годин, {minutes} хвилин, {seconds} секунд."
        await update.message.reply_text(message)

async def handle_countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input_time = datetime.strptime(update.message.text, '%Y-%m-%d %H:%M')
        context.user_data['input_time'] = input_time
        await update.message.reply_text(f"Тобто ми зустрінемось {input_time.strftime('%Y-%m-%d %H:%M')}, поняв")
        await countdown(update, context)
    except ValueError:
        await update.message.reply_text("Написала не у правильному форматі. Напиши ще раз отако 'yyyy-mm-dd hh:mm'.")

def main():
    application = ApplicationBuilder().token('6157022440:AAE9v45CMjguIP9Cg_0HrqtlGTuAykBgKaw').build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_countdown))
    application.run_polling()
    application.idle()


if __name__ == '__main__':
    main()


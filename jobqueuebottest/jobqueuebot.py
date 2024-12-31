import os
import logging

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler

# Enable logging
log_filename = os.path.splitext(os.path.basename(__file__))[0]+".log"
logging.basicConfig(
    filename=log_filename, filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Retrieve token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

async def callback_30_seconds(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text='One message in 30 seconds from start') 

async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text='One message every minute after 10 seconds from start')

async def callback_beep(context: ContextTypes.DEFAULT_TYPE):
    user_chat_id = context.job.chat_id
    time = context.job.data[0]
    fullname = context.job.data[1]
    await context.bot.send_message(chat_id=user_chat_id, text=f'Beep after {time} seconds for {fullname}')

async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_chat_id = update.effective_chat.id
    name = update.effective_chat.full_name
    try:
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=user_chat_id, text='Please provide a number')
            return
        elif len(context.args) > 1:
            await context.bot.send_message(chat_id=user_chat_id, text='Please provide only one number')
            return
        timer_int = int(context.args[0])
    except ValueError:
        await context.bot.send_message(chat_id=user_chat_id, text='Please provide a valid number')
        return
    await context.bot.send_message(chat_id=user_chat_id, text=f'Hello {name}, your timer is set for {timer_int} seconds')
    context.job_queue.run_once(callback_beep, timer_int, data=(timer_int, update.effective_chat.full_name), chat_id=user_chat_id)

async def callback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_chat_id = update.effective_chat.id
    my_text = """
        Hello! I am a timer bot\n
        Use /timer 5 to set a timer for 5 seconds\n
        I also send a message 30 seconds after start command\n
        And every minute after 10 seconds from start command.
        """
    context.job_queue.run_once(callback_30_seconds, when=30, chat_id=user_chat_id)
    context.job_queue.run_repeating(callback_minute, interval=60, first=10, chat_id=user_chat_id)
    
    await context.bot.send_message(chat_id=user_chat_id, text=my_text)

def main():
    logger.info("Starting jobqueuebot")
    application = Application.builder().token(TOKEN).build()
    timer_hander = CommandHandler("timer", callback_timer)
    start_handler = CommandHandler("start", callback_start)
    application.add_handler(timer_hander)
    application.add_handler(start_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
import os
import logging
import datetime as dtm

import pytz

from telegram.constants import ParseMode
from telegram.ext import MessageHandler, filters, Defaults, Application

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


async def job(context):
    chat_id = context.job.chat_id
    timezone = context.bot.defaults.tzinfo
    local_now = dtm.datetime.now(timezone)
    utc_now = dtm.datetime.now(dtm.timezone.utc)
    text = (
        f"Running job at {local_now.strftime('%Y-%m-%d %H:%M:%S')}"
        f" in timezone {timezone}, which equals {utc_now.strftime('%Y-%m-%d %H:%M:%S')} UTC."
    )
    await context.bot.send_message(chat_id=chat_id, text=text)


async def echo(update, context):
    text = update.message.text
    # Send with default parse mode
    await update.message.reply_text(f'html: <u><em><strong>{text}</strong></em></u>')
    # Override default parse mode locally
    await update.message.reply_text(f'markdown: `{text}`', parse_mode=ParseMode.MARKDOWN)
    # Send with no parse mode
    await update.message.reply_text(f'none: <u>{text}</u>', parse_mode=None)

    # Schedule job
    context.job_queue.run_once(
        job, when=dtm.timedelta(seconds=5), chat_id=update.effective_chat.id
    )


def main():
    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Europe/Berlin'))

    application = (
        Application.builder()
        .token(TOKEN)
        .defaults(defaults)
        .build()
    )

    # on non command text message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()

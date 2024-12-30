import os
import logging

from uuid import uuid4
from telegram.ext import Application, CommandHandler

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

async def put(update, context):
    """Usage: /put value"""
    # Generate ID and separate value from command
    key = str(uuid4())
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value
    # Send the key to the user
    logger.info('Stored %s: %s for %s', key, value, update.effective_user.first_name)
    await update.message.reply_text(key)

async def get(update, context):
    """Usage: /get uuid"""
    # Separate ID from command
    key = context.args[0]

    # Load value and send it to the user
    value = context.user_data.get(key, 'Not found')
    logger.info('Retrieved %s: %s for %s', key, value, update.effective_user.first_name)
    await update.message.reply_text(value)

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('put', put))
    application.add_handler(CommandHandler('get', get))
    application.run_polling()

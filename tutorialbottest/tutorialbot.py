import os
import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, constants
from telegram.ext import (Application, CommandHandler, MessageHandler,
                        CallbackContext, CallbackQueryHandler, filters)


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

# Pre-assign menu text
FIRST_MENU = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button."
SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."

# Pre-assign button text
NEXT_BUTTON = "Next"
BACK_BUTTON = "Back"
TUTORIAL_BUTTON = "Tutorial"

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
]])
SECOND_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton(TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")]
])


async def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the application as a handler for messages coming from the Bot API
    """

    logger.info('%s wrote %s', update.message.from_user.first_name, update.message.text)

    try:
        screaming = context.user_data[update.effective_user.id]['screaming']
    except KeyError:
        context.user_data[update.effective_user.id] = {'screaming': None}
        screaming = None
    if screaming is None and update.message.text:
        await context.bot.send_message(
            update.message.chat_id,
            update.message.text,
            entities=update.message.entities
        )
    elif screaming and update.message.text:
        await context.bot.send_message(
            update.message.chat_id,
            update.message.text.upper(),
            entities=update.message.entities
        )
    elif not screaming and update.message.text:
        await context.bot.send_message(
            update.message.chat_id,
            update.message.text,
            entities=update.message.entities
        )


async def scream(update: Update, context: CallbackContext) -> None:
    """
    This function handles the /scream command
    """
    user_id = update.effective_user.id
    context.user_data[user_id]['screaming'] = True
    await context.bot.send_message(user_id, text="Scream mode set")

async def whisper(update: Update, context: CallbackContext) -> None:
    """
    This function handles /whisper command
    """
    user_id = update.effective_user.id
    context.user_data[user_id]['screaming'] = False
    await context.bot.send_message(user_id, text="Whisper mode set")


async def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """

    await context.bot.send_message(
        update.message.from_user.id,
        FIRST_MENU,
        parse_mode=constants.ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )


async def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    data = update.callback_query.data
    text = ''
    markup = None

    if data == NEXT_BUTTON:
        text = SECOND_MENU
        markup = SECOND_MENU_MARKUP
    elif data == BACK_BUTTON:
        text = FIRST_MENU
        markup = FIRST_MENU_MARKUP

    # Close the query to end the client-side loading animation
    await update.callback_query.answer()

    # Update message content with corresponding menu section
    await update.callback_query.message.edit_text(
        text,
        constants.ParseMode.HTML,
        reply_markup=markup
    )


def main() -> None:
    # Initialize the application instance
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("scream", scream))
    application.add_handler(CommandHandler("whisper", whisper))
    application.add_handler(CommandHandler("menu", menu))

    # Register handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_tap))

    # Echo any message that is not a command
    application.add_handler(MessageHandler(~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()

import asyncio
import json
import os

from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()  # take environment variables from .env.


application = Application.builder().token(os.getenv("TOKEN")).build()


def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
    # Add conversation, command, and any other handlers
    add_user_handlers()

    try:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )

        return {"statusCode": 200, "body": "Success"}

    except Exception as exc:
        return {"statusCode": 500, "body": "Failure"}


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text=":D",
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return -1


def add_user_handlers():
    # Track commands
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", home)],
        states={},
        fallbacks=[
            CommandHandler("start", home),
        ],
        per_message=False,
        per_user=True,
    )
    application.add_handler(conv_handler)


if __name__ == "__main__":
    add_user_handlers()
    application.run_polling()

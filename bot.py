import asyncio

from dotenv import load_dotenv
from telegram.ext import Application

load_dotenv()  # take environment variables from .env.


application = Application.builder().token(TELEGRAM_API_KEY).build()


def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
    # Add conversation, command, and any other handlers

    try:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )

        return {"statusCode": 200, "body": "Success"}

    except Exception as exc:
        return {"statusCode": 500, "body": "Failure"}

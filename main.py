import logging

from revChatGPT.V1 import Chatbot

import config

from telegram import Update, Message
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

users: dict[int, Chatbot] = {}
logger = logging.getLogger("main")


def cache_chat_bot(user_id: int):
    if user_id not in users:
        users[user_id] = Chatbot(config={
            "access_token": config.env["GPT_ACCESS_TOKEN"],
            "model": "gpt-4",
        })


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    cache_chat_bot(update.effective_user.id)

    user = update.effective_user
    await update.message.reply_html(
        rf"Welcome {user.mention_html()}!"
        rf"You can now start chatting with GPT.",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help yourself!")


async def ask_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask GPT."""
    cache_chat_bot(update.effective_user.id)
    logger.info(f"[ask] {update.effective_user.username}: {update.message.text}")

    chat = users[update.effective_user.id]
    sent_message = None

    max_chars = 4096
    msg_count = 1
    edit_threshold = 42

    msg = ""

    try:
        for data in chat.ask(update.message.text):
            msg = data["message"]
            if msg == "":
                continue

            if sent_message is None:
                sent_message = await update.message.reply_text(msg)
            else:
                if len(msg) > msg_count * max_chars:
                    await context.bot.edit_message_text(
                        msg[(msg_count - 1) * max_chars: msg_count * max_chars],
                        chat_id=sent_message.chat_id,
                        message_id=sent_message.message_id
                    )
                    msg_count += 1
                    sent_message = await update.message.reply_text(msg[(msg_count - 1) * max_chars: msg_count * max_chars])
                else:
                    if len(msg) % edit_threshold == 0:
                        msg_tmp = msg[(msg_count - 1) * max_chars: msg_count * max_chars]

                        if sent_message.text != msg_tmp:
                            edited_msg = await context.bot.edit_message_text(
                                msg_tmp,
                                chat_id=sent_message.chat_id,
                                message_id=sent_message.message_id
                            )
                            if isinstance(edited_msg, Message):
                                sent_message = edited_msg

        if sent_message.text != msg[(msg_count - 1) * max_chars: msg_count * max_chars]:
            await context.bot.edit_message_text(
                msg[(msg_count - 1) * max_chars: msg_count * max_chars],
                chat_id=sent_message.chat_id,
                message_id=sent_message.message_id
            )
    except Exception as e:
        print('Error:', e)
        try:
            await update.message.reply_text(e)
        except Exception as e1:
            print('TgSent err:', e1)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.env["TG_TOKEN"]).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_gpt))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

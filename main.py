import os
import logging
import telegram
from dotenv import load_dotenv
import json

load_dotenv(verbose=True)


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    Updater,
    ContextTypes
)

from emoji import emojize

# Predefined emojis
bookmark = emojize(":bookmark:", use_aliases=True)
bell = emojize(":bell:", use_aliases=True)
lightning = emojize(":high_voltage:", use_aliases=True)
good = emojize(":smiling_face_with_sunglasses:", use_aliases=True)
siren = emojize(":police_car_light:", use_aliases=True)
plus = emojize(":plus:", use_aliases=True)
minus = emojize(":minus:", use_aliases=True)
party = emojize(":party_popper:", use_aliases=True)


def update_user_db(user_db: dict) -> bool:
    with open(DB_FILE, "w+") as f:
        temp = json.dumps(user_db, ensure_ascii=False, sort_keys=True, indent=4)
        f.write(temp)
    print("user_db.json is written successfully!")


# Get chat_id to send message under each context
def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        # text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        chat_id = context.bot_data[update.poll.id]
    return str(chat_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat_id = get_chat_id(update, context)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="당신의 여행을 도와주는 챗봇입니다.")

    # user_db = handler.get_user(chat_id)

    # user = update.message.from_user


    options = [
        [
            # InlineKeyboardButton(text="키워드 편집", callback_data="1"),
            InlineKeyboardButton(
                text=f"{bookmark} 나만의 봇 만들기 {bookmark}", callback_data="2"
            ),
        ],
        [
            InlineKeyboardButton(text=f"{bell} 여행계획 세우기 {bell}", callback_data="3"),
        ],
        # [
        #     InlineKeyboardButton(
        #         text=f"{lightning}  {lightning}", callback_data="4"
        #     ),
        # ],
    ]

    # Buttons' layout markup
    reply_markup = InlineKeyboardMarkup(options)

    # Message with the buttons
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="원하는 작업을 선택하세요.",
        reply_markup=reply_markup,
    )

    



def main() -> None:

    # bot = telegram.Bot(TELEGRAM_TOKEN)
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # updater = Updater(bot=bot,update_queue=None)
    # dp = updater.dispatcher
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()

    # dp.add_handler(CommandHandler("start", start))

    chat_id = 62786931
    # chat_id = getUpdates()
    # bot.sendMessage(chat_id=chat_id, text="Hello World")

    # updater.start_polling()
    # updater.idle()


if __name__ == "__main__":
    main()

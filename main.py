import os
import logging
from utils import send_action, facts_to_str
from chat import MyTravelAgent
from dotenv import load_dotenv
from emoji import emojize

import time

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)

from telegram.constants import ChatAction

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
)


load_dotenv(verbose=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Predefined emojis
bookmark = emojize(":bookmark:", use_aliases=True)
bell = emojize(":bell:", use_aliases=True)
lightning = emojize(":high_voltage:", use_aliases=True)
good = emojize(":smiling_face_with_sunglasses:", use_aliases=True)
siren = emojize(":police_car_light:", use_aliases=True)
plus = emojize(":plus:", use_aliases=True)
minus = emojize(":minus:", use_aliases=True)
party = emojize(":party_popper:", use_aliases=True)


# Create an agent with a given template: template_01
agent = MyTravelAgent("template_01")


send_typing_action = send_action(ChatAction.TYPING)


######################

START, EMOJI, POLITE, VERBOSE, PLAN = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    options = [
        [
            InlineKeyboardButton(
                text=f"{good} 나만의 챗봇 만들기 {good}", callback_data="customize"
            ),
            InlineKeyboardButton(
                text=f"{siren} 여행계획 세우기 {siren}", callback_data="plan"
            ),
        ],
    ]
    markup = InlineKeyboardMarkup(options)

    await update.message.reply_text(
        text="안녕하세요, 당신의 여행을 도와주는 챗봇🤖입니다. 무엇을 할까요?", reply_markup=markup
    )

    return START


async def callback_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user = update.effective_user
    await query.answer()

    if query.data == "customize":
        logger.info(query.data)
        await query.edit_message_text(text=f"좋아요! 나만의 챗봇을 만들어볼까요?{good}")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"지금부터 {user.first_name}님이 선호하는 챗봇으로 만들어주세요!",
        )

        return EMOJI

    elif query.data == "plan":
        logger.info(query.data)
        await query.edit_message_text(text=f"네, 알겠습니다! 이제 저와 함께 여행계획을 세워보아요{good}")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{user.first_name}님이 계획하고자 하는 여행에 대해서 알려주세요!",
        )

        return PLAN


async def emoji_tf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    options = [
        [
            InlineKeyboardButton(
                text=f"{good}이모티콘도 사용해주세요.{good}", callback_data="emoji_on"
            ),
            InlineKeyboardButton(text=f"텍스트로만 대답해주세요.", callback_data="emoji_off"),
        ],
    ]

    # Buttons' layout markup
    reply_markup = InlineKeyboardMarkup(options)

    # Message with the buttons
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="이모티콘도 사용해볼까요?",
        reply_markup=reply_markup,
    )

    return POLITE


async def emoji_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    logger.info("emoji_callback")

    if query.data == "emoji_on":
        context.user_data["emoji"] = True
        await query.edit_message_text(text=f"좋아요! 이모티콘도 사용해볼게요{good}")
    elif query.data == "emoji_off":
        context.user_data["emoji"] = False
        await query.edit_message_text(text=f"네, 텍스트로만 대답할게요{siren}")
    # logger.info(context.user_data["emoji"])

    return POLITE


async def polite_tf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    options = [
        [
            InlineKeyboardButton(
                text=f"{good} 존댓말로 공손하게 {good}", callback_data="polite_on"
            ),
            InlineKeyboardButton(
                text=f"{siren} 반말로 친근하게 {siren}", callback_data="polite_off"
            ),
        ],
    ]

    # Buttons' layout markup
    reply_markup = InlineKeyboardMarkup(options)

    # Message with the buttons
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="이렇게 대답해주세요",
        reply_markup=reply_markup,
    )
    return VERBOSE


async def polite_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["polite"] = None
    query = update.callback_query
    await query.answer()

    if query.data == "polite_on":
        context.user_data["polite"] = "존댓말로 공손하게 대답해주세요"
        await query.edit_message_text(text=f"존댓말로 공손하게 대답해드려요{good}")
    elif query.data == "polite_off":
        context.user_data["polite"] = "반말로 친근하게 대답해줘"
        await query.edit_message_text(text=f"반말로 친근하게 대답할게{siren}")


async def verbose_tf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    logger.info(f"verbose_tf: {query.data}")

    options = [
        [
            InlineKeyboardButton(
                text=f"{good} 최대한 자세하고 길게 대답해주세요 {good}", callback_data="verbose_on"
            ),
            InlineKeyboardButton(
                text=f"{siren} 간결하고 짧게 대답해주세요 {siren}", callback_data="verbose_off"
            ),
        ],
    ]

    # Buttons' layout markup
    reply_markup = InlineKeyboardMarkup(options)

    # Message with the buttons
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="길고 상세한 답변을 원하시나요?",
        reply_markup=reply_markup,
    )


async def verbose_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "verbose_on":
        context.user_data["verbose"] = True
        await query.edit_message_text(text=f"좋아요! 최대한 자세하게 대답할게요{good}")

    elif query.data == "verbose_off":
        context.user_data["verbose"] = False
        await query.edit_message_text(text=f"네, 간결하게 대답할게요{siren}")

    return PLAN


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    await update.message.reply_text(f"{user.first_name}님의 대화를 종료합니다! 다음에 또 만나요!")

    return ConversationHandler.END


@send_typing_action
async def response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=agent.response(update.message.text, last_n=5),
    )
    return PLAN


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the gathered info."""
    await update.message.reply_text(
        f"This is what you already told me: {facts_to_str(context.user_data)}"
    )


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(callback_start)],
            EMOJI: [CallbackQueryHandler(emoji_tf)],
            POLITE: [CallbackQueryHandler(polite_tf)],
            VERBOSE: [CallbackQueryHandler(verbose_tf)],
            PLAN: [MessageHandler(filters.TEXT & (~filters.COMMAND), response)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    application.add_handler(conversation)

    show_data_handler = CommandHandler("show_data", show_data)
    application.add_handler(show_data_handler)

    application.run_polling()


if __name__ == "__main__":
    main()

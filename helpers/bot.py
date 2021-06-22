import logging
import re

from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    [
        InlineKeyboardButton("DEL", callback_data="DEL"),
        InlineKeyboardButton("AC", callback_data="AC"),
    ],
    [
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")"),
    ],
    [
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("/", callback_data="/"),
    ],
    [
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("*", callback_data="*"),
    ],
    [
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-"),
    ],
    [
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("=", callback_data="="),
        InlineKeyboardButton("+", callback_data="+"),
    ],
]
banner = "{:.^34}".format(" Calculator by @odbots ")
logger = logging.getLogger(__name__)


def start_handler(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        text=banner, reply_markup=InlineKeyboardMarkup(buttons), quote=True
    )


def calcExpression(text):
    try:
        return float(eval(text))
    except (SyntaxError, ZeroDivisionError):
        return ""
    except TypeError:
        return float(eval(text.replace('(', '*(')))
    except Exception as e:
        logger.error(e, exc_info=True)
        return ""


def button_press(update, context):
    """Function to handle the button press"""
    callback_query = update.callback_query
    callback_query.answer()
    text = callback_query.message.text.split("\n")[0].strip().split("=")[0].strip()
    text = '' if banner in text else text
    data = callback_query.data
    inpt = text + data
    result = ''
    if data == "=" and text:
        result = calcExpression(text)
        text = ""
    elif data == "DEL" and text:
        text = text[:-1]
    elif data == "AC":
        text = ""
    else:
        dot_dot_check = re.findall(r"(\d*\.\.|\d*\.\d+\.)", inpt)
        opcheck = re.findall(r"([*/\+-]{2,})", inpt)
        if not dot_dot_check and not opcheck:
            strOperands = re.findall(r"(\.\d+|\d+\.\d+|\d+)", inpt)
            if strOperands:
                text += data
                result = calcExpression(text)

    text = f"{text:<50}"
    if result:
        if text:
            text += f"\n{result:>50}"
        else:
            text = result
    text += '\n\n' + banner
    try:
        callback_query.edit_message_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.info(e)
        pass


def get_dispatcher(bot):
    """Create and return dispatcher instances"""
    dispatcher = Dispatcher(bot, None, workers=0)

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(button_press))

    return dispatcher

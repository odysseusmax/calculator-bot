from threading import Thread
from queue import Queue

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
oprs = (
    "/",
    "*",
    "-",
    "+",
)
non_oprs = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "(", ")", ".")


def start_handler(update, context):
    """Send a message when the command /start is issued."""
    text = "<" + " " * 78 + ">"
    update.message.reply_text(
        text=text, reply_markup=InlineKeyboardMarkup(buttons), quote=True
    )


def button_press(update, context):
    """Function to handle the button press"""
    callback_query = update.callback_query
    callback_query.answer()
    text = (
        callback_query.message.text.replace("<", "").replace(">", "").replace(" ", "")
    )
    data = callback_query.data
    d = "<" + " " * 78 + ">"
    try:
        if (text == "") or ("Divisionbyzero" in text) or ("Invalidsyntax" in text):
            text = ""
        elif ("=" in text) and data in oprs:
            text = text.split("=")[-1]
        elif ("=" in text) and (data in non_oprs):
            text = ""

        if data == "DEL":
            text = text[:-1]
            if text == "":
                text = d
        elif (data == "AC") or (text == "" and ((data in oprs) or (data == "="))):
            text = d
        elif data == "=":
            text = text + " = " + str(eval(text))
        else:
            text = text + data
    except ZeroDivisionError:
        text = "Division by zero"
    except (SyntaxError, TypeError):
        text = "Invalid syntax"

    text = text + d[len(text):]
    try:
        callback_query.edit_message_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception:
        pass


def get_update_queue(bot):
    """Create dispatcher instances"""
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue)

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CallbackQueryHandler(button_press))

    thread = Thread(target=dispatcher.start, name="dispatcher")
    thread.start()

    return update_queue

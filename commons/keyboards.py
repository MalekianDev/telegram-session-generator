from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

from commons.texts import CREATE_PYRO_SESSION_BTN_TEXT

main_menu = ReplyKeyboardMarkup(
    [
        [KeyboardButton(CREATE_PYRO_SESSION_BTN_TEXT)],
    ]
)

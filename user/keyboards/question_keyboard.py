from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_options_kb(options: list):
    kb_options = InlineKeyboardMarkup(row_width=2)
    for button in options:
        kb_options.insert(InlineKeyboardButton(text=button, callback_data=button))

    return kb_options


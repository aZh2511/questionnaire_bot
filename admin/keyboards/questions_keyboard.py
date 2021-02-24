from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_kb(data: list, *args):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in data:
        keyboard.insert(InlineKeyboardButton(text=button, callback_data=button))

    if args:
        keyboard.insert(InlineKeyboardButton(text='Create new', callback_data='create_new'))
    keyboard.insert(InlineKeyboardButton(text='Back to main menu', callback_data='back_to_main'))
    return keyboard

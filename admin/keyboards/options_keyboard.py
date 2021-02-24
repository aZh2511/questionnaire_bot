from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_options_kb(data: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in data:
        keyboard.insert(InlineKeyboardButton(text=button, callback_data=button))

    keyboard.insert(InlineKeyboardButton(text='Create new', callback_data='create_new'))
    keyboard.insert(InlineKeyboardButton(text='Back to questions', callback_data='back_to_questions'))
    return keyboard

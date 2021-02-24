from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Start questionnaire', callback_data='start_q')]
])

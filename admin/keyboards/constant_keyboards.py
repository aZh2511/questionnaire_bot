from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Manage questions', callback_data='questions')],
    [InlineKeyboardButton(text='Manage options', callback_data='options')],
    [InlineKeyboardButton(text='Manage order', callback_data='order')],
    [InlineKeyboardButton(text='Manage texts', callback_data='texts')]
])

kb_change_delete = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Change', callback_data='change')],
    [InlineKeyboardButton(text='Delete', callback_data='delete')],
    [InlineKeyboardButton(text='Back', callback_data='back')]
])

kb_manage_texts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='First Message', callback_data='first_message')],
    [InlineKeyboardButton(text='Second Message', callback_data='second_message')]
])

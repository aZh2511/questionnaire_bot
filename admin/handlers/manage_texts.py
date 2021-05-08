from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from database.db_commands import database
from loader import dp, bot
from ..keyboards import create_kb, kb_change_delete, kb_manage_texts
from ..state import Admin


@dp.callback_query_handler(lambda c: c.data in ['texts'])
async def choose_question(call: types.CallbackQuery):
    """Choose text from existing one in db to be changed."""
    # Get all the questions and transform them to a list.
    data = await database.get_texts()
    data = [data[i][0] for i in range(len(data))]

    # Create text and keyboard.
    text = f'-----------   Managing texts   -----------\n\nFirst message: {data[0]}\n\n' \
           f'Second message: {data[1]}'

    await Admin.ManageTexts.set()

    await call.message.edit_text(text, reply_markup=kb_manage_texts)


@dp.callback_query_handler(lambda c: c.data == 'first_message', state=Admin.ManageTexts)
async def change_first_message(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(q_id=1)
    text = 'Send me new text please'
    await call.message.edit_text(text)
    await Admin.ChangeText.set()


@dp.callback_query_handler(lambda c: c.data == 'second_message', state=Admin.ManageTexts)
async def change_first_message(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(q_id=2)
    text = 'Send me new text please'
    await call.message.edit_text(text)
    await Admin.ChangeText.set()


@dp.message_handler(state=Admin.ChangeText)
async def update(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get('q_id')

    # try:
    await database.change_text(message.text, question_id)
    await bot.send_message(message.from_user.id, 'Changed!')
    # except :
    #     await bot.send_message(message.from_user.id, 'Changed!')

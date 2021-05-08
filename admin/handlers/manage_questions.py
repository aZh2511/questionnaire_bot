from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from database.db_commands import database
from loader import dp
from ..keyboards import create_kb, kb_change_delete
from ..state import Admin


@dp.callback_query_handler(lambda c: c.data in ['questions'])
async def choose_question(call: types.CallbackQuery):
    """Choose question from existing one in db."""
    # Get all the questions and transform them to a list.
    data = await database.get_questions()
    data = [data[i][0] for i in range(len(data))]

    # Create text and keyboard.
    text = '-----------   Managing questions   -----------\n\nChoose a question or create a new one.'
    keyboard = create_kb(data, 'questions')
    await Admin.ManageQuestions.set()

    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ["create_new"], state=Admin.ManageQuestions)
async def manage_questions(call: types.CallbackQuery, state: FSMContext):
    """Ask for an answer text for new answer."""
    text = f'To create new question send me:\n\n' \
           f'<b><i>New question text _ order of question</i></b>' \
           f'\n\nExample: What is your name? _ 1'

    await state.update_data(type='question')

    await call.message.edit_text(text, parse_mode=ParseMode.HTML)
    await Admin.CreateNew.set()


@dp.callback_query_handler(lambda c: c.data not in ["back_to_main"], state=Admin.ManageQuestions)
async def manage_questions(call: types.CallbackQuery, state: FSMContext):
    """Manage chosen question (change/delete)."""
    text = f'Chosen question: <b>{call.data}</b>\n\nChoose:'

    # Save the question.
    await state.update_data(question=call.data)
    await state.update_data(type='question')

    await call.message.edit_text(text, reply_markup=kb_change_delete, parse_mode=ParseMode.HTML)
    await Admin.ChangeDelete.set()

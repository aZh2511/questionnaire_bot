from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from database.db_commands import database
from loader import dp
from ..keyboards import create_kb, kb_change_delete, create_options_kb
from ..state import Admin


@dp.callback_query_handler(lambda c: c.data in ['options'])
async def choose_question(call: types.CallbackQuery):
    """Choose question from existing one in db."""

    # Get all the questions and transform them to a list.
    data = await database.get_questions()
    data = [data[i][0] for i in range(len(data))]

    # Create text and keyboard.
    text = '-----------   Managing options   -----------\n\nChoose a question to manage its options:'
    keyboard = create_kb(data)

    await Admin.ManageOptions.set()
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data not in ["back_to_main"], state=Admin.ManageOptions)
async def choose_option(call: types.CallbackQuery, state: FSMContext):
    """Return back to main menu of admin-panel."""
    # Update type of managing and question text value.
    await state.update_data(question=call.data)
    await state.update_data(type='option')

    # Save question_id.
    question_id = await database.get_question_id(call.data)
    question_id = question_id[0]
    await state.update_data(question_id=question_id)

    # Create keyboard
    data = await database.get_options(question_id)
    keyboard = create_options_kb(data)

    text = f'Chosen question: <b>{call.data}</b>\n\nChoose an option to manage or create a new one.'

    await call.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin.ChooseOption.set()


@dp.callback_query_handler(lambda c: c.data in ["back_to_questions"], state=Admin.ChooseOption)
async def manage_questions(call: types.CallbackQuery,):
    """Send a question choosing for options managing."""
    # Get all the questions and create a keyboard.
    data = await database.get_questions()
    data = [data[i][0] for i in range(len(data))]
    keyboard = create_kb(data)

    text = '-----------   Managing options   -----------\n\nChoose a question to manage its options:'

    await Admin.ManageOptions.set()
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == "create_new", state=Admin.ChooseOption)
async def manage_questions(call: types.CallbackQuery, state: FSMContext):
    """Ask for an option text for new option."""
    text = f'To create new option send me:\n\n' \
           f'<b><i>New question text</i></b>' \
           f'\n\nExample: USA, Washington'

    await state.update_data(type='option')

    await call.message.edit_text(text, parse_mode=ParseMode.HTML)
    await Admin.CreateNew.set()


@dp.callback_query_handler(state=Admin.ChooseOption)
async def manage_questions(call: types.CallbackQuery, state: FSMContext):
    """Manage chosen option (change/delete)."""
    text = f'Chosen option: <b>{call.data}</b>\n\nChoose:'

    # Save the option.
    await state.update_data(option=call.data)

    await call.message.edit_text(text, reply_markup=kb_change_delete, parse_mode=ParseMode.HTML)
    await Admin.ChangeDelete.set()

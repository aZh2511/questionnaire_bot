from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from config import IP_WHITELIST
from database.db_commands import database
from loader import dp, bot
from ..keyboards import kb_admin_panel, create_kb, create_options_kb
from ..state import Admin


@dp.message_handler(lambda message: message.from_user.id in IP_WHITELIST,
                    commands=['admin'], state='*')
async def admin_panel(message: types.Message, state: FSMContext):
    """Process /admin, send admin-panel."""
    await state.finish()
    text = 'Welcome to admin panel!\nChoose what you want to do:'
    await bot.send_message(message.from_user.id, text, reply_markup=kb_admin_panel)


@dp.callback_query_handler(lambda c: c.data == 'back_to_main', state=[Admin.ManageOptions, Admin.ManageQuestions,
                                                                      Admin.ManageOrder])
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = 'Welcome to admin panel!\nChoose what you want to do:'
    await call.message.edit_text(text, reply_markup=kb_admin_panel)


@dp.callback_query_handler(lambda c: c.data == "change", state=Admin.ChangeDelete)
async def change_delete(call: types.CallbackQuery, state: FSMContext):
    """Ask for a new text to change question or option text value."""
    await state.update_data(command=call.data)
    data = await state.get_data()

    if data.get('type') == 'question':
        question = data.get('question')
        text = f'Chosen question: <b>{question}</b>\n\nSend me new text for that question:'
        await call.message.edit_text(text, parse_mode=ParseMode.HTML)
        await Admin.ChangeCommand.set()

    elif data.get('type') == 'option':
        option = data.get('option')
        text = f'Chosen option: <b>{option}</b>\n\nSend me new text for that option:'
        await call.message.edit_text(text, parse_mode=ParseMode.HTML)
        await Admin.ChangeCommand.set()


@dp.callback_query_handler(lambda c: c.data == "delete", state=Admin.ChangeDelete)
async def change_delete(call: types.CallbackQuery, state: FSMContext):
    """Delete chosen question or option."""
    await state.update_data(command=call.data)
    data = await state.get_data()

    if data.get('type') == 'question':

        await database.delete_question(data.get('question'))
        text = 'Deleted!'
        await call.message.edit_text(text)

    elif data.get('type') == 'option':

        await database.delete_option(data.get('option'))
        text = 'Deleted!'
        await call.message.edit_text(text)

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "back", state=Admin.ChangeDelete)
async def change_delete(call: types.CallbackQuery, state: FSMContext):
    """Return back depending on type (managing questions or options)."""
    await state.update_data(command=call.data)
    data = await state.get_data()

    questions = await database.get_questions()
    questions = [questions[i][0] for i in range(len(questions))]

    if data.get('type') == 'question':
        text = '-----------   Managing options   -----------\n\nChoose a question to manage its options:'
        keyboard = create_kb(questions)
        await Admin.ManageOptions.set()
        await call.message.edit_text(text, reply_markup=keyboard)

    elif data.get('type') == 'option':
        await state.update_data(type='option')
        question_id = await database.get_question_id(data.get('question'))
        question_id = question_id[0]
        questions = await database.get_options(question_id)
        keyboard = create_options_kb(questions)
        text = f'Chosen question: <b>{data.get("question")}</b>\n\nChoose an option to manage or create a new one.'
        await call.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await Admin.ChooseOption.set()


@dp.message_handler(state=Admin.ChangeCommand)
async def change_text(message: types.Message, state: FSMContext):
    """Change question or option."""
    data = await state.get_data()
    command = data.get('type')
    if command == 'question':
        new_question_text = message.text

        await database.change_question(new_question_text, data.get('question'))
        await bot.send_message(message.from_user.id, 'Updated!')

    elif command == 'option':
        new_option_text = message.text

        await database.change_option(new_option_text, data.get('option'))
        await bot.send_message(message.from_user.id, 'Updated!')


@dp.message_handler(state=Admin.CreateNew)
async def create_new(message: types.Message, state: FSMContext):
    """Create new question or option depending on type (managing questions or options)."""
    data = await state.get_data()
    command = data.get('type')
    if command == 'question':
        try:
            question_text = message.text.split(' _ ')
            await database.add_new_question(question_text[0], int(question_text[-1]))
            await bot.send_message(message.from_user.id, 'Added!')
            await state.finish()
        except ValueError:
            text = f'Incorrect input!\n\nTo create new question send me:\n\n' \
                   f'<b><i>New question text _ order of question</i></b>' \
                   f'\n\nExample: What is your name? _ 1'
            await bot.send_message(message.from_user.id, text)
    elif command == 'option':
        await database.add_option(message.text, data.get('question_id'))
        await bot.send_message(message.from_user.id, 'Added!')
        await state.finish()


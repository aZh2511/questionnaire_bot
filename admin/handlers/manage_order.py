from aiogram import types
from aiogram.dispatcher import FSMContext

from database.db_commands import database
from loader import dp
from ..keyboards import create_kb
from ..state import Admin


@dp.callback_query_handler(lambda c: c.data in ['order'])
async def choose_question(call: types.CallbackQuery, state: FSMContext):
    """Choose question from existing one in db."""
    # Get all the questions.
    questions = await database.get_questions()

    # Save max order of questions.
    max_order = len(questions)
    await state.update_data(max_order=max_order)

    # Create text.
    text = 'Question            |            Order\n'
    for row in questions:
        text += f'{row[0]}                              {row[2]}\n'

    # Create keyboard.
    questions = [questions[i][0] for i in range(len(questions))]
    keyboard = create_kb(questions)

    await Admin.ManageOrder.set()
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(state=Admin.ManageOrder)
async def choose_question(call: types.CallbackQuery, state: FSMContext):
    """Change question order."""
    # Get needed data.
    data = await state.get_data()
    question_order = await database.get_question_id(call.data)
    question_order = question_order[1]
    max_order = data.get('max_order')

    # Change question order.
    if question_order < max_order:
        question_order += 1
    else:
        question_order = 1
    await database.change_question_order(question_order, call.data)

    # Create text.
    questions = await database.get_questions()
    text = 'Question            |            Order\n'
    for row in questions:
        text += f'{row[0]}                              {row[2]}\n'

    # Create keyboard.
    questions = [questions[i][0] for i in range(len(questions))]
    keyboard = create_kb(questions)

    await call.message.edit_text(text, reply_markup=keyboard)

from aiogram import types
from aiogram.dispatcher import FSMContext

from database.db_commands import database
from loader import dp, bot
from ..keyboards import kb_start, create_options_kb
from ..states import Questionnaire
from sheets import insert_answer


@dp.message_handler(commands=['start'], state='*')
async def starting(message: types.Message):
    await database.add_new_user()
    text = 'Welcome to ___\nTo get started press the button "Start questionnaire"'
    await bot.send_message(message.from_user.id, text, reply_markup=kb_start)
    await Questionnaire.Questions.set()


@dp.callback_query_handler(state=Questionnaire.Questions)
async def ask_questions(call: types.CallbackQuery, state: FSMContext):

    state_get = await state.get_data()
    if call.data == 'start_q':
        data = await database.get_questions()
    else:
        data = state_get.get('questions')

        current_answers = state_get.get('answers')
        if current_answers:
            current_answers.append(call.data)
            await state.update_data(answers=current_answers)
        else:
            await state.update_data(answers=[call.data])

    try:
        options = await database.get_options(data[0][1])
        question = data.pop(0)[0]
    except KeyError:
        question = list(data.keys())[0]
        options = await database.get_options(data.get(question))
        data.pop(question)

    # Insert to google sheet
    # if call.data != 'start_q':
    #     insert_answer(call, question)

    await call.message.edit_text(question, reply_markup=create_options_kb(options))

    await state.update_data(questions=data)
    if not data:
        await Questionnaire.EndQuestions.set()


@dp.callback_query_handler(state=Questionnaire.EndQuestions)
async def end_questions(call: types.CallbackQuery, state: FSMContext):
    """End of questionnaire. Save the data."""
    text = 'Thanks!'
    await call.message.edit_text(text)
    state_get = await state.get_data()

    current_answers = state_get.get('answers')
    current_answers.append(call.data)
    questions = await database.get_questions()
    questions = [questions[i][0] for i in range(len(questions))]

    data = list(zip(questions, current_answers))
    insert_answer(data)

    await state.finish()

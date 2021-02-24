from aiogram.dispatcher.filters.state import StatesGroup, State


class Questionnaire(StatesGroup):
    Questions = State()
    EndQuestions = State()

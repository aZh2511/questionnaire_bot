from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    ManageQuestions = State()
    CreateNew = State()
    ChangeDelete = State()
    ChangeCommand = State()
    ChooseOption = State()
    ManageOptions = State()
    ManageOrder = State()

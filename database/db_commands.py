from datetime import datetime

from aiogram import types
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from loader import db


class DBCommands:
    """Class for working with DB."""
    pool: Connection = db

    ADD_NEW_USER = "INSERT INTO users (chat_id, username, full_name, adding_date) " \
                   "VALUES ($1, $2, $3, $4)"
    COUNT_USERS = "SELECT COUNT (*) FROM users"
    GET_USERS = "SELECT (username, full_name) FROM users"
    GET_QUESTIONS = "SELECT (question, question_id, q_order) FROM questions ORDER BY q_order ASC"
    GET_OPTIONS = "SELECT (option_text) FROM options WHERE question_id=$1"
    ADD_QUESTION = "INSERT INTO questions (question, q_order) VALUES ($1, $2)"
    CHANGE_QUESTION = "UPDATE questions SET question=$1 WHERE question=$2"
    DELETE_QUESTION = "DELETE FROM questions WHERE question=$1"
    GET_ID_QUESTION = "SELECT (question_id, q_order) FROM questions WHERE question=$1"
    ADD_OPTION = "INSERT INTO options (option_text, question_id) VALUES ($1, $2)"
    CHANGE_OPTION = "UPDATE options SET option_text=$1 WHERE option_text=$2"
    DELETE_OPTION = "DELETE FROM options WHERE option_text=$1"
    CHANGE_QUESTION_ORDER = "UPDATE questions SET q_order=$1 WHERE question=$2"

    async def add_new_user(self):
        """Add new user to db."""
        user = types.User.get_current()
        command = self.ADD_NEW_USER

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        adding_date = datetime.now()

        args = chat_id, username, full_name, adding_date

        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def count_users(self):
        """Count users in db."""
        command = self.COUNT_USERS
        record = await self.pool.fetchval(command)
        return record

    async def get_users(self):
        """Get all users from the db."""
        command = self.GET_USERS
        data = await self.pool.fetch(command)

        data = [data[i][0] for i in range(len(data))]

        text = ''
        for num, row in enumerate(data):
            text += f'{num + 1}. @{row[0]} {row[1]}\n'
        return text

    async def get_questions(self):
        """Get questions for questionnaire."""
        command = self.GET_QUESTIONS
        data = await self.pool.fetch(command)
        data = [data[i][0] for i in range(len(data))]
        return data

    async def get_options(self, question_id: int):
        """Get options for question."""
        command = self.GET_OPTIONS
        data = await self.pool.fetch(command, question_id)
        data = [data[i][0] for i in range(len(data))]
        return data

    async def add_new_question(self, question: str, order: int):
        """Add new question."""
        command = self.ADD_QUESTION
        return await self.pool.fetchval(command, question, order)

    async def change_question(self, text: str, question: str):
        """Change question question value (text)."""
        command = self.CHANGE_QUESTION
        return await self.pool.fetchval(command, text, question)

    async def delete_question(self, question: str):
        """Delete the question. On delete deletes all the referred options."""
        command = self.DELETE_QUESTION
        return await self.pool.fetchval(command, question)

    async def get_question_id(self, question: str):
        """Get the question ID and ORDER."""
        command = self.GET_ID_QUESTION
        return await self.pool.fetchval(command, question)

    async def add_option(self, text: str, question_id: int):
        """Add new option."""
        command = self.ADD_OPTION
        return await self.pool.fetchval(command, text, question_id)

    async def change_option(self, text: str, option: str):
        """Change the option option value (text). """
        command = self.CHANGE_OPTION
        return await self.pool.fetchval(command, text, option)

    async def delete_option(self, option: str):
        """Delete the option."""
        command = self.DELETE_OPTION
        return await self.pool.fetchval(command, option)

    async def change_question_order(self, new_order: int, question: str):
        """Change an order of the question."""
        command = self.CHANGE_QUESTION_ORDER
        return await self.pool.fetchval(command, new_order, question)


database = DBCommands()

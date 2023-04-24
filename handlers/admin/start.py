from loader import dp
from loader import bot
from data.config import admins_id
from aiogram import types
from utils.db_api import db_users
from utils.inline_btn import create_markup
from static.text import admin
from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    user = State()
    one_mailing = State()
    one_mailing_button = State()
    one_mailing_button_compilet = State()
    is_good_mailing = State()
    is_good_mailing_all = State()
    mailing = State()
    mailing_button = State()
    mailing_button_compilet = State()


MAIN_MARKUP = create_markup('reply', 2, ['🎲 Играть'], ['⚡ Топ рейтинг'], ['⚒ Все пользователи'], ['📨 Рассылка'])


@dp.message_handler(chat_type='private', commands=['start'], chat_id=admins_id)
async def start_message(message: types.Message):
    if not db_users.check_user(message.chat.id):
        db_users.add_user(message.chat.id, message.chat.username, message.chat.full_name)
    await bot.send_message(message.chat.id, admin.text_start.format(message.chat.first_name), reply_markup=MAIN_MARKUP)

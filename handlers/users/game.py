from loader import dp
from loader import bot
from data.config import rate, channel_id, admins_id

from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.users.start import UserState, anti_flood, MAIN_MARKUP
from asyncio import sleep

from static.text import users
from utils.inline_btn import create_markup
from utils.db_api import db_users

from handlers.admin.start import MAIN_MARKUP as admin_markup


@dp.message_handler(chat_type='private', regexp='🎲 Играть')
@dp.throttled(anti_flood, rate=rate)
async def games_message(message: types.Message):
    await UserState.games.set()
    markup = create_markup('reply', 3, ['⚽'], ['🏀'], ['🎲'], ['🎯'], ['🎳'], ['🎰'], ['❌ Отмена'])
    await bot.send_message(message.chat.id, users.text_games, reply_markup=markup)


@dp.message_handler(chat_type='private', state=UserState.games, content_types=['dice', 'text'], is_forwarded=False)
@dp.throttled(anti_flood, rate=rate)
async def game_message(message: types.Message, state: FSMContext):
    if message.dice:
        await sleep(3)
        if db_users.add_game(message.chat.id, message.dice.emoji, message.dice.value):
            await message.reply(users.text_win_game.format(message.chat.first_name, message.dice.emoji,
                                                            message.dice.value))
        else:
            channel = await bot.get_chat_member(channel_id[0], message.chat.id)
            if channel.status == 'left':
                markup = create_markup('inline', 1, ['🚀 Наш канал', 'u3l*https://t.me/DiceOfFire'])
            else:
                markup = None
            await message.reply(users.text_no_win_game.format(message.chat.first_name, message.dice.emoji,
                                                               message.dice.value),
                                reply_markup=markup)
    elif message.text == '❌ Отмена':
        await state.finish()
        if message.chat.id not in admins_id:
            await bot.send_message(message.chat.id, users.cancel, reply_markup=MAIN_MARKUP)
        else:
            await bot.send_message(message.chat.id, users.cancel, reply_markup=admin_markup)
    else:
        await bot.send_message(message.chat.id, users.vote_games)


@dp.message_handler(chat_type='private', state=UserState.games, content_types=['dice', 'text'], is_forwarded=True)
@dp.throttled(anti_flood, rate=rate)
async def cheat_message(message: types.Message):
    await bot.send_message(message.chat.id, users.text_cheat)

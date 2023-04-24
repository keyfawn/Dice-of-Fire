from aiogram.dispatcher import FSMContext
from loader import dp
from loader import bot
from data.config import admins_id
from aiogram import types
from utils.db_api import db_users
from utils.inline_btn import create_markup
from static.text import admin
from handlers.admin.start import AdminState
from utils.top_rating import check


@dp.message_handler(chat_type='private', regexp='⚒ Все пользователи', chat_id=admins_id)
async def all_users_message(message: types.Message, target=None):
    markup = create_markup('inline', 2, *db_users.return_all())
    if target:
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/all_users.png', 'rb'),
                                                           caption=admin.text_all_users), message.chat.id,
                                     message.message_id,
                                     reply_markup=markup)
    else:
        await bot.send_photo(message.chat.id, open('static/img/all_users.png', 'rb'), caption=admin.text_all_users,
                             reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data[:2] == 'id', chat_type='private', chat_id=admins_id)
async def user_callback(call: types.CallbackQuery, state: FSMContext):
    await AdminState.user.set()
    data = db_users.deanon(call.data[2:])
    await state.update_data(id=data.id)
    markup = create_markup('inline', 2, ['⚔ Посмотреть', f'u3l*tg://user?id={data.id}'],
                           ['📨 Написать', 'mailing'], ['❌ Назад', 'cancel'])
    try:
        ava = await bot.get_user_profile_photos(data.id)
        photo = ava.photos[0][-1].file_id if ava.photos else open('static/img/no_ava.png', 'rb')

        teht = check(data)

        await bot.edit_message_media(types.InputMediaPhoto(photo, caption=admin.text_top_info.format(
            data.first_name, data.id, data.username,
            round((data.win_count / data.all_count) * 100, 2) if data.all_count else 0,
            data.date, data.all_count, data.win_count, teht)), call.from_user.id, call.message.message_id,
                                     reply_markup=markup)
    except Exception:
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/bad_mailing.png', 'rb'),
                                                           caption=admin.text_bad_mailing),
                                     call.from_user.id, call.message.message_id)


@dp.callback_query_handler(chat_type='private', state=AdminState.user, chat_id=admins_id)
async def userka_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancel':
        await state.finish()
        await call.answer(admin.cancel_top)
        await all_users_message(call.message, 'yes')
    elif call.data == 'mailing':
        await AdminState.one_mailing.set()
        markup = create_markup('inline', 1, ['❌ Отмена', 'cancel'])
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/one_mailing.png', 'rb'),
                                                           caption=admin.text_one_mailing), call.from_user.id,
                                     call.message.message_id,
                                     reply_markup=markup)

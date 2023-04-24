from aiogram.dispatcher import FSMContext
from loader import dp
from loader import bot
from data.config import admins_id
from aiogram import types
from utils.db_api import db_users
from utils.inline_btn import create_markup
from static.text import admin
from handlers.admin.start import AdminState


@dp.message_handler(chat_type='private', regexp='📨 Рассылка', chat_id=admins_id)
async def mailing_message(message: types.Message):
    markup = create_markup('inline', 1, ['❌ Отмена', 'cancel'])
    await bot.send_message(message.chat.id, admin.text_mailing, reply_markup=markup)
    await AdminState.mailing.set()


@dp.callback_query_handler(chat_type='private', state=AdminState.mailing, chat_id=admins_id)
async def mailing_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancel':
        await call.answer(admin.cancel)
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await state.finish()


@dp.message_handler(chat_type='private', state=AdminState.mailing, chat_id=admins_id, content_types=['text', 'photo'])
async def text_mailing_message(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
    await state.update_data(text=message.html_text)
    markup = create_markup('inline', 2, ['✅ Да', 'yes'], ['❌ Нет', 'no'], ['❌ Отмена', 'cancel'])
    await bot.send_photo(message.chat.id, open('static/img/saved_text_mailing.png', 'rb'),
                         caption=admin.text_saved_mailing, reply_markup=markup)
    await AdminState.mailing_button.set()


@dp.callback_query_handler(chat_type='private', state=AdminState.mailing_button, chat_id=admins_id)
async def mailing_button_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        await AdminState.mailing_button_compilet.set()
        markup = create_markup('inline', 1, ['❌ Отмена', 'cancel'])
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/saved_button_mailing.png', 'rb'),
                                                           caption=admin.text_mailing_button),
                                     call.from_user.id, call.message.message_id, reply_markup=markup)
    elif call.data == 'no':
        await AdminState.mailing_button_compilet.set()
        await state.update_data(markup=None)
        call.message.text = 'None'
        await mailing_button_message(call.message, state)
    elif call.data == 'cancel':
        await mailing_callback(call, state)


@dp.message_handler(chat_type='private', state=AdminState.mailing_button_compilet, chat_id=admins_id)
async def mailing_button_message(message: types.Message, state: FSMContext):
    if message.text == 'None':
        data = await state.get_data()
        if 'photo' in data.keys():
            await bot.send_photo(message.chat.id, data['photo'], caption=data['text'],
                                 parse_mode='html')
        else:
            await bot.send_message(message.chat.id, data['text'],
                                   parse_mode='html')
    else:
        data = message.text.split('\n')
        markup = create_markup('inline', int(data[0]), *list(map(lambda x: [x.split(':::')[0], x.split(':::')[1].split(']')[0]], data[1].split('[')[1:])))
        await state.update_data(markup=markup)
        data = await state.get_data()
        if 'photo' in data.keys():
            await bot.send_photo(message.chat.id, data['photo'], caption=data['text'], reply_markup=markup,
                                 parse_mode='html')
        else:
            await bot.send_message(message.chat.id, data['text'], reply_markup=markup,
                                   parse_mode='html')
    markup = create_markup('inline', 2, ['✅ Да', 'yes'], ['❌ Нет', 'no'], ['❌ Отмена', 'cancel'])
    await bot.send_photo(message.chat.id, open('static/img/mailing.png', 'rb'), caption=admin.text_is_good_mailing, reply_markup=markup)
    await AdminState.is_good_mailing_all.set()


@dp.callback_query_handler(chat_type='private', state=AdminState.mailing_button_compilet, chat_id=admins_id)
async def mailing_button_compilet_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancel':
        await mailing_callback(call, state)


@dp.callback_query_handler(chat_type='private', state=AdminState.is_good_mailing_all, chat_id=admins_id)
async def mailing_good_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        await state.finish()
        for id_user in db_users.return_id():
            try:
                if 'photo' in data.keys():
                    await bot.send_photo(id_user, data['photo'], caption=data['text'], reply_markup=data['markup'],
                                         parse_mode='html')
                else:
                    await bot.send_message(id_user, data['text'], reply_markup=data['markup'],
                                           parse_mode='html')
            except Exception:
                ...
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/good_mailing.png', 'rb'),
                                                           caption=admin.text_good_mailing.format(
                                                               call.from_user.first_name)),
                                     call.from_user.id, call.message.message_id)
    elif call.data == 'no' or call.data == 'cancel':
        await mailing_callback(call, state)

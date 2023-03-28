from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', '💥 Запустить бота'),
            types.BotCommand('profile', '🌟 Профиль'),
            types.BotCommand('rating', '🔥 Топ рейтинг'),
            types.BotCommand('about', '⚡ О нас')
        ]
    )

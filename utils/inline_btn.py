from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def create_markup(tip, row_width, *args):
    """
    Создаёт готовый markup с кнопками\n
    Если нужно inline: tip="inline", если reply: tip="reply"\n
    row_width указывает на количество столбцов\n
    *args - списки, в которых\n
    [0]="название кнопки",\n
    [1] (только для inline)="data for callback" или [1] (только для inline)="u3l*{url}"\n
    :param tip: "inline" or "reply"
    :param row_width: int
    :param args: list, list, list, ...
    :return: aiogram.types.Markup
    """
    if tip == 'inline':
        markup = InlineKeyboardMarkup(row_width=row_width)
        markup.add(*create_btns(tip, *args))
    else:
        markup = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
        markup.add(*create_btns(tip, *args))
    return markup


def create_btns(tip, *args):
    """
    Создаёт готовые кнопки для markup\n
    Если нужны inline, то tip="inline", если reply - tip="reply"\n
    *args - списки, в которых [0]="название кнопки", [1] (только для inline)="data for callback"\n
    :param tip: "inline" or "reply"
    :param args: list, list, list, ...
    :return: [aiogram.types.Buttons, aiogram.types.Buttons, ...]
    """
    result = []
    for params in args:
        if tip == 'inline':
            if 'u3l*' in params[1]:
                result.append(InlineKeyboardButton(params[0], url=params[1][4:]))
            else:
                result.append(InlineKeyboardButton(params[0], callback_data=params[1]))
        else:
            result.append(KeyboardButton(params[0]))
    return result

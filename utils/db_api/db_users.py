import pendulum
from utils.db_api import db_session
from utils.db_api.schemas.user import User


def create_session():
    db_session.global_init('db/users.db')
    db_sess = db_session.create_session()
    return db_sess


def check_user(id_user: int):
    """
    Проверяет id в бд\n
    :param id_user: id
    :return: True или False
    """
    db_sess = create_session()
    for user in db_sess.query(User).filter(User.id == id_user):
        db_sess.close()
        return True
    db_sess.close()
    return False


def add_user(id_user: int, username: str, first_name: str):
    """
    Добавляет пользователя в бд\n
    :param id_user: id
    :param username: username
    :param first_name: first_name
    :return: add user in db
    """
    user = User()
    user.id = id_user
    user.username = username
    user.first_name = first_name
    user.date = pendulum.now('Europe/Moscow').to_datetime_string()

    db_sess = create_session()
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()


def add_game(id_user: int, game: str, count: int):
    db_sess = create_session()

    db_sess.query(User).filter(User.id == id_user).update({'all_count': User.all_count + 1})

    win = False
    if game == '🎯':
        if count == 6:
            add_win(db_sess, id_user)
            win = True
        db_sess.query(User).filter(User.id == id_user).update({'darts': User.darts + 1})
    elif game == '🏀':
        if count == 5:
            add_win(db_sess, id_user)
            win = True
        db_sess.query(User).filter(User.id == id_user).update({'basketball': User.basketball + 1})
    elif game == '🎲':
        if count == 1:
            add_win(db_sess, id_user)
            win = True
        db_sess.query(User).filter(User.id == id_user).update({'dice': User.dice + 1})
    elif game == '⚽':
        if count == 5:
            add_win(db_sess, id_user)
            win = True
        db_sess.query(User).filter(User.id == id_user).update({'football': User.football + 1})
    elif game == '🎳':
        if count == 6:
            add_win(db_sess, id_user)
            win = True
        db_sess.query(User).filter(User.id == id_user).update({'bowling': User.bowling + 1})
    elif game == '🎰':
        if count == 64:
            add_win(db_sess, id_user, True)
            win = True
        db_sess.query(User).filter(User.id == id_user).update({'slot': User.slot + 1})

    db_sess.commit()
    db_sess.close()

    return win


def add_win(db_sess, id_user: int, casino=False):
    if not casino:
        db_sess.query(User).filter(User.id == id_user).update({'win_count': User.win_count + 1})
    else:
        db_sess.query(User).filter(User.id == id_user).update({'win_count': User.win_count + 10})

    db_sess.commit()
    db_sess.close()


def return_all():
    db_sess = create_session()
    l1st = list(map(lambda x: [str(x.first_name), f'id{x.id}'], db_sess.query(User).all()))
    db_sess.close()
    return l1st


def return_id():
    db_sess = create_session()
    l1st = list(map(lambda x: x.id, db_sess.query(User).all()))
    db_sess.close()
    return l1st


def return_win():
    db_sess = create_session()
    l1st = list(map(lambda x: [str(x.first_name), str(x.id), x.all_count, x.win_count] if x.all_count else None,
                    db_sess.query(User).all()))
    db_sess.close()

    l1st = list(filter(lambda x: x[-1] / x[-2] if x else None, l1st))
    l1st = sorted(l1st, key=lambda x: x[-1] / x[-2])

    return l1st[::-1]


def deanon(id_user: int):
    db_sess = create_session()
    return db_sess.query(User).filter(User.id == int(id_user)).first()

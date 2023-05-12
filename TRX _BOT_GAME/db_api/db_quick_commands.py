import datetime
import random
from typing import List, Tuple

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from db_api.schemas.crush_game import Crush_base
from db_api.schemas.lottery import Lottery_model, Lottery_base
from db_api.schemas.paymants import Paymants_base, Paymants_model
from db_api.schemas.say_hi import Say_base, Say_model
from db_api.schemas.stats import Stats_base, Stats_model
from db_api.schemas.users import Users_base, Users_model
from db_api.schemas.bonus import Bonus_base, Bonus_model
from db_api.schemas.achievement import Achievement_base, Achievement_model
from db_api.schemas.promo_code import Promo_base, Promo_model
from db_api.schemas.promo_code_count import Promo_count_base,Promo_count_model
from settings import db, session


def register_user(message):
    user_id = message.from_user.id
    name = f"{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username if message.from_user.username else None}"
    user_level = 1
    bal_usd = 0
    bal_trx = 1
    bet = 1.0
    join_date = datetime.datetime.now()
    first_referrer_id = 404
    second_referrer_id = 404
    third_referrer_id = 404
    captcha = 0
    mail = ''
    phone = ''
    wallet_trx = 0
    wallet_usdt = 0
    user_language = 'en'
    ban = 0
    patron = 0
    user = Users_base(user_id=int(user_id), name=str(name), user_level=int(user_level), bal_usd=int(bal_usd),
                 bal_trx=int(bal_trx), bet=float(bet), join_date=join_date, first_referrer_id=int(first_referrer_id),
                 second_referrer_id=int(second_referrer_id), third_referrer_id=int(third_referrer_id),
                 captcha=int(captcha), mail=str(mail), phone=str(phone), wallet_trx=str(wallet_trx),
                 wallet_usdt=str(wallet_usdt), user_language=str(user_language), ban=int(ban), patron=int(patron))
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_user_bonus(message):
    user_id = message.from_user.id
    daily_date = '2020-01-01 10:00:00'
    week_date = '2020-01-01 10:00:00'
    user = Bonus_base(user_id=int(user_id), daily_date=daily_date, week_date=week_date)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_user_achievement(message):
    user_id = message.from_user.id
    daily_bonus = 0
    c_daily_bonus = 0
    week_bonus = 0
    c_week_bonus = 0
    pay_trx = 0
    c_pay_trx = 0
    pay_trx_th = 0
    c_pay_trx_th = 0
    game_dice = 0
    c_game_dice = 0
    game_mine = 0
    c_game_mine = 0
    game_fifty = 0
    c_game_fifty = 0
    game_case = 0
    c_game_case = 0
    game_slot = 0
    c_game_slot = 0
    game_num = 0
    c_game_num = 0
    game_num_win_hun = 0
    c_game_num_win_hun = 0
    win_lot = 0
    c_win_lot = 0
    c_f_ref = 0
    c_s_ref = 0
    c_a_ref = 0
    user = Achievement_base(user_id=int(user_id), daily_bonus=daily_bonus, c_daily_bonus=c_daily_bonus, week_bonus=week_bonus,
                      c_week_bonus=c_week_bonus, pay_trx=pay_trx, c_pay_trx=c_pay_trx, pay_trx_th=pay_trx_th,
                      c_pay_trx_th=c_pay_trx_th, game_dice=game_dice, c_game_dice=c_game_dice, game_mine=game_mine,
                      c_game_mine=c_game_mine, game_fifty=game_fifty, c_game_fifty=c_game_fifty, game_case=game_case,
                      c_game_case=c_game_case, game_slot=game_slot, c_game_slot=c_game_slot, game_num=game_num,
                      c_game_num=c_game_num, game_num_win_hun=game_num_win_hun, c_game_num_win_hun=c_game_num_win_hun,
                      win_lot=win_lot, c_win_lot=c_win_lot, c_f_ref=c_f_ref, c_s_ref=c_s_ref, c_a_ref=c_a_ref)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_user_promo(message, promo_code):
    user_id = message.from_user.id
    c_promo_code = 0
    user = Promo_base(user_id=int(user_id), promo_code=promo_code, c_promo_code=c_promo_code)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_promo_count(promo_code):
    count = 0
    user = Promo_count_base(promo_code=promo_code, count_promo_code=count)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_stats():
    stats = Stats_base(all_acc=12412, day_acc=453, active_acc=4247, pay_trx=15171.08644261892)
    session.add(stats)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_say_hi(user_id, text_message, photo, audio):
    date = datetime.datetime.now()
    acces = 0
    say_hi = Say_base(user_id=user_id, text_message=text_message, acces=acces, photo=photo, audio=audio, date=date)
    session.add(say_hi)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def register_user_crush(user_id):
    import numpy as np
    min_val = 1.0
    max_val = 10.0
    k = 2.2
    probabilities = []
    for val in np.arange(min_val, max_val + 0.1, 0.1):
        probability = 1.0 / (val ** k)
        probabilities.append(probability)
    probabilities /= np.sum(probabilities)
    random_val = round(np.random.choice(np.arange(min_val, max_val + 0.1, 0.1), p=probabilities), 1)
    num_game = random_val
    coef = 1.0
    stop = False
    user = Crush_base(user_id=int(user_id), num_game=num_game, coef=coef, stop=stop)
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False

async def select_all_users():
    users = await Users_model.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(Users_model.user_id).gino.scalar()
    return count

async def count_first_ref(user_id):
    count = await (db.select([db.func.count()]).where(Users_model.first_referrer_id == user_id).gino.scalar())
    return count

async def count_second_ref(user_id):
    count = await (db.select([db.func.count()]).where(Users_model.second_referrer_id == user_id).gino.scalar())
    return count

async def count_third_ref(user_id):
    count = await (db.select([db.func.count()]).where(Users_model.third_referrer_id == user_id).gino.scalar())
    return count


async def count_del_trx_admin(user_id):
    count = await (db.select([db.func.count()]).where((Paymants_model.del_trx != 0) & (Paymants_model.acces == 0)).gino.scalar())
    return count


async def count_add_trx_admin(user_id):
    count = await (db.select([db.func.count()]).where((Paymants_model.add_trx != 0) & (Paymants_model.acces == 0)).gino.scalar())
    return count


async def count_add_usd_admin(user_id):
    count = await (db.select([db.func.count()]).where((Paymants_model.add_usd != 0) & (Paymants_model.acces == 0)).gino.scalar())
    return count


async def count_say_hi_admin(user_id):
    count = await (db.select([db.func.count()]).where(Say_model.acces == 0).gino.scalar())
    return count


async def get_users():
    # Получение всех записей из таблицы users
    all_users = await Users_model.query.gino.all()
    # Получение всех user_id из записей
    all_user_ids = [user.user_id for user in all_users]
    return all_user_ids


async def get_user_id_by_language(language):
    # Получение всех записей из таблицы users с заданным языком
    users = await Users_model.query.where(Users_model.user_language == language).gino.all()
    # Получение всех user_id из записей
    user_ids = [user.user_id for user in users]
    return user_ids


async def get_users_patron():
    users = await Users_model.query.where(Users_model.patron == 1).gino.all()
    return users


async def get_patreon_list() -> List[Tuple[int, int, str, int]]:
    query = Users_model.query.where(Users_model.patron == 1)
    users = await query.gino.all()
    return [(user.bal_trx, user.bal_usd, user.name, user.user_id) for user in users]


async def get_ban_list() -> List[Tuple[int, int, str, int]]:
    query = Users_model.query.where(Users_model.ban == 1)
    users = await query.gino.all()
    return [(user.bal_trx, user.bal_usd, user.name, user.user_id) for user in users]


async def select_user(user_id):
    user = await Users_model.query.where(Users_model.user_id == user_id).gino.first()
    return user


async def select_lottery_user(user_id):
    user = await Lottery_model.query.where(Lottery_model.user_id == user_id).gino.first()
    return user


async def select_user_bonus(user_id):
    bonus = await Bonus_model.query.where(Bonus_model.user_id == user_id).gino.first()
    return bonus


async def select_user_achievement(user_id):
    achievement = await Achievement_model.query.where(Achievement_model.user_id == user_id).gino.first()
    return achievement


async def select_user_promo_code(promo_code, user_id):
    promo_code = await Promo_model.query.where((Promo_model.promo_code == promo_code) & (Promo_model.user_id == user_id)).gino.first()
    return promo_code


async def select_user_promo_code_count(promo_code):
    promo_code_count = await Promo_count_model.query.where(Promo_count_model.promo_code == promo_code).gino.first()
    return promo_code_count


async def del_lot_db():
    await Lottery_model.delete.gino.status()
    return session.commit()


async def give_achivement_day(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 2.5).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_daily_bonus=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_achivement_pay(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 5).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_pay_trx=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_achivement_pay_th(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 25).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_pay_trx_th=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_achivement_f(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 6.5).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_f_ref=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_achivement_s(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 3.5).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_s_ref=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_achivement_a(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 10).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_a_ref=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()

async def give_achivement_cub(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 3.5).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_game_dice=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()

async def give_achivement_win_lot(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 17.5).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_win_lot=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()

async def give_achivement_miner(user_id):
    """Перевірка ачівки"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 4).where(Users_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(c_game_mine=1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_level_2(user_id):
    """Даємо другий рівень аккаунта"""
    await Users_model.update.values(user_level=2).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def give_level_3(user_id):
    """Даємо третій рівень аккаунта"""
    await Users_model.update.values(user_level=3).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def give_bonus_ref(user_id):
    """Pеферальний бонус"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 1).where(Users_model.user_id == user_id).gino.status()
    return session.commit()

async def give_bonus_sec_ref(user_id):
    """Pеферальний бонус 2 рівень"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 0.5).where(Users_model.user_id == user_id).gino.status()
    return session.commit()

async def give_bonus_thi_ref(user_id):
    """Pеферальний бонус 3 рівень"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 0.2).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def give_bonus_daily_lvl_1(user_id):
    """Даємо щоденний бонус"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 1).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def give_bonus_daily_lvl_2(user_id):
    """Даємо щоденний бонус"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 1.05).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def give_bonus_daily_lvl_3(user_id):
    """Даємо щоденний бонус"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 1.15).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def update_bonus_daily(user_id):
    """Оновлюємо дату"""
    await Bonus_model.update.values(daily_date=datetime.datetime.now()).where(Bonus_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(daily_bonus=Achievement_model.daily_bonus + 1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def give_bonus_week(user_id):
    """Даємо тижневий бонус"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 1.75).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def give_bonus_week_lvl_3(user_id):
    """Даємо тижневий бонус"""
    await Users_model.update.values(bal_trx=Users_model.bal_trx + 2.5).where(Users_model.user_id == user_id).gino.status()
    return session.commit()


async def update_bonus_week(user_id):
    """Оновлюємо дату"""
    await Bonus_model.update.values(week_date=datetime.datetime.now()).where(Bonus_model.user_id == user_id).gino.status()
    await Achievement_model.update.values(week_bonus=Achievement_model.week_bonus + 1).where(Achievement_model.user_id == user_id).gino.status()
    return session.commit()


async def all_acc_stats():
    all_acc = random.randint(25, 85)
    await Stats_model.update.values(all_acc=Stats_model.all_acc + all_acc).gino.status()
    return session.commit()


async def pay_trx_stats():
    await Stats_model.update.values(pay_trx=Stats_model.pay_trx * 1.0085).gino.status()
    return session.commit()


async def day_acc_stats():
    day_acs = random.randint(-25, 25)
    if day_acs <= 10:
        day_acs = random.randint(-25, 25)
    if day_acs == 0:
        day_acs = random.randint(-25, 25)
    await Stats_model.update.values(day_acc=Stats_model.day_acc + day_acs).gino.status()
    return session.commit()


async def active_acc_stats():
    active_acc = random.randint(10, 25)
    await Stats_model.update.values(active_acc=Stats_model.active_acc + active_acc).gino.status()
    return session.commit()


async def add_lot(user_id):
    """Добавляем юзера в базу"""
    user = Lottery_base(user_id=int(user_id))
    session.add(user)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


async def add_del_trx(state):
    """Добавляем платеж в базу"""
    async with state.proxy() as data:
        user_id = data['id_del_trx']
        add_usd = 0
        add_trx = 0
        del_trx = data['del_trx']
        date = datetime.datetime.now()
        adress = data['del_trx_get_adress']
        acces = 0

        user = Paymants_base(user_id=int(user_id), add_usd=add_usd, add_trx=add_trx, del_trx=del_trx, date=date, adress=adress, acces=acces)
        session.add(user)
        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

async def add_add_trx(state):
    """Добавляем платеж в базу"""
    async with state.proxy() as data:
        user_id = data['id_del_trx']
        add_usd = 0
        add_trx = data['add_trx']
        del_trx = 0
        date = datetime.datetime.now()
        adress = data['add_trx_get_adress']
        acces = 0

        user = Paymants_base(user_id=int(user_id), add_usd=add_usd, add_trx=add_trx, del_trx=del_trx, date=date, adress=adress, acces=acces)
        session.add(user)
        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

async def add_add_usd(state):
    """Добавляем платеж в базу"""
    async with state.proxy() as data:
        user_id = data['id_del_trx']
        add_usd = data['add_usd']
        add_trx = 0
        del_trx = 0
        date = datetime.datetime.now()
        adress = data['add_usd_get_adress']
        acces = 0

        user = Paymants_base(user_id=int(user_id), add_usd=add_usd, add_trx=add_trx, del_trx=del_trx, date=date, adress=adress, acces=acces)
        session.add(user)
        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

async def get_records(user_id, within="all"):
    """Получаем историю о доходах/расходах"""
    if within == "day":
        result = await Paymants_model.query.where(
            (Paymants_model.user_id == user_id) &
            (Paymants_model.date >= datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)) &
            (Paymants_model.date < datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999))
        ).order_by(Paymants_model.date).gino.all()
    elif within == "week":
        result = await Paymants_model.query.where(
            (Paymants_model.user_id == user_id) &
            (Paymants_model.date >= datetime.datetime.now() - datetime.timedelta(days=6)) &
            (Paymants_model.date <= datetime.datetime.now())
        ).order_by(Paymants_model.date).gino.all()
    elif within == "month":
        result = await Paymants_model.query.where(
            (Paymants_model.user_id == user_id) &
            (Paymants_model.date >= datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)) &
            (Paymants_model.date < datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999))
        ).order_by(Paymants_model.date).gino.all()
    else:
        result = await Paymants_model.query.where(Paymants_model.user_id == user_id).order_by(Paymants_model.date).gino.all()
    return result


async def get_say_hi(user_id, within="all"):
    """Получаем историю о доходах/расходах"""
    query = Say_model.query.where(Say_model.user_id == user_id).order_by(Say_model.date)

    if within == "day":
        query = query.where(Say_model.date.between(datetime.datetime.now().date(), datetime.datetime.now()))
    elif within == "week":
        query = query.where(Say_model.date.between(datetime.date.today() - datetime.timedelta(days=6), datetime.datetime.now()))
    elif within == "month":
        now = datetime.utcnow()
        query = query.where(Say_model.date.between(datetime(now.year, now.month, 1), now))

    return await query.gino.all()





class DBCommands_middleware:
    async def get_user(self, user_id):
        user = await Users_model.query.where(Users_model.user_id == user_id).gino.first()
        return user
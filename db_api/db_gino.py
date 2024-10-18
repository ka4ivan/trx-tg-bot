from gino import Gino
from aiogram import Dispatcher

from db_api import db_quick_commands
from db_api.schemas.users import Users_model
from db_api.schemas.bonus import Bonus_model
from db_api.schemas.achievement import Achievement_model
from db_api.schemas.promo_code import Promo_model
from db_api.schemas.promo_code_count import Promo_count_model
from db_api.schemas.say_hi import Say_model
from db_api.schemas.paymants import Paymants_model
from db_api.schemas.lottery import Lottery_model
from db_api.schemas.crush_game import Crush_model
from db_api.schemas.stats import Stats_model
from settings import DATABASE_STR, db


async def on_startup_db(dispatcher: Dispatcher) -> None:
    await db.set_bind(DATABASE_STR)
    await db.gino.create_all()
    count = await db.func.count(Stats_model.all_acc).gino.scalar()
    if count > 0:
        pass
    else:
        db_quick_commands.register_stats()
    print('PostgreSQL connected')


async def on_shutdown_db(dispatcher: Dispatcher) -> None:
    await db.pop_bind().close()

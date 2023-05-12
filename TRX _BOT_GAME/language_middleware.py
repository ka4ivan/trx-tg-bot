from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from settings import I18N_DOMAIN, LOCALES_DIR
from db_api.db_quick_commands import DBCommands_middleware

db = DBCommands_middleware()

async def get_lang(user_id):
    # Делаем запрос к базе, узнаем установленный язык
    user = await db.get_user(user_id)
    if user:
        # Если пользователь найден - возвращаем его
        return user.user_language


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale



def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n












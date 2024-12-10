import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from data.config import load_config
from handlers.users.main.start import router as start_router
from handlers.users.main.menu import router as menu_router
from handlers.users.admin.admin import router as admin_router
from middlewares.checksub import CheckSubscriptionMiddleware
from middlewares.throttling import ThrottlingMiddleware
from utils.database.db_init import init_db
from utils.set_bot_commands import set_default_commands
from utils.database import db

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    config = load_config()
    bot = Bot(token=config.bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(CheckSubscriptionMiddleware())
    dp.callback_query.middleware(CheckSubscriptionMiddleware())
    await init_db()
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(menu_router)

    try:
        await db.create_pool(config)
        await set_default_commands(bot)
        print("Bot ishga tushdi...")
        await dp.start_polling(bot)
    finally:
        if hasattr(db, "pool") and db.pool is not None:
            await db.pool.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot to'xtatildi!")

from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram import types
from aiogram.enums import ChatType

from src import Database


class RegisterChatMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]], event: types.Message,
                       data: Dict[str, Any]
                       ):
        db: Database | None = data.get("db", None)
        if db is None:
            raise Exception("Database Not Found")

        chat = await db.chat.get_chat(event.chat.id)
        if event.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP] and not chat:
            await db.chat.add_chat(event.chat.id)
        return await handler(event, data)


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]], event: types.Message,
                       data: Dict[str, Any]
                       ):
        db: Database | None = data.get("db", None)
        if db is None:
            raise Exception("Database Not Found")
        if not event.from_user:
            return await handler(event, data)

        if not await db.user.get_user(event.from_user.id):
            await db.user.add_user(event.from_user.id, event.from_user.username)
            await event.reply(f"🥳 {event.from_user.mention_markdown()}, вітаю\\! Ти тепер граєш у русофобію")

        if event.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            return await handler(event, data)
        if not await db.chat_user.get_chat_user(event.chat.id, event.from_user.id):
            await db.chat_user.add_chat_user(event.chat.id, event.from_user.id)
            await db.cooldown.add_user_cooldown(event.chat.id, event.from_user.id)
        return await handler(event, data)

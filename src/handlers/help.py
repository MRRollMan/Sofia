from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.handlers.commands import commands_router
from src.types import (HelpCallback, Games)
from src.utils import TextBuilder, reply_and_delete


def get_help_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Основне - /killru", callback_data=HelpCallback(game=Games.KILLRU).pack()),
           width=1)

    buttons = [
        InlineKeyboardButton(text="🎲", callback_data=HelpCallback(game=Games.DICE).pack()),
        InlineKeyboardButton(text="🎯", callback_data=HelpCallback(game=Games.DARTS).pack()),
        InlineKeyboardButton(text="🎳", callback_data=HelpCallback(game=Games.BOWLING).pack()),
        InlineKeyboardButton(text="🏀", callback_data=HelpCallback(game=Games.BASKETBALL).pack()),
        InlineKeyboardButton(text="⚽", callback_data=HelpCallback(game=Games.FOOTBALL).pack()),
        InlineKeyboardButton(text="🎰", callback_data=HelpCallback(game=Games.CASINO).pack())
    ]

    kb.row(*buttons, width=4)
    return kb


@commands_router.message(Command("help"))
async def help_command(message: types.Message):
    kb = get_help_keyboard()
    await reply_and_delete(message, text="⚙️ Тут ти можеш почитати\nпро мене все", reply_markup=kb.as_markup())


@commands_router.callback_query(F.data == "back_to_help")
async def back_to_help(query: CallbackQuery):
    kb = get_help_keyboard()
    await query.message.edit_text("⚙️ Тут ти можеш почитати\nпро мене все", reply_markup=kb.as_markup())


@commands_router.callback_query(HelpCallback.filter())
async def callback_help(query: CallbackQuery, callback_data: HelpCallback):
    game_emojis = {
        "killru":
            f"Русофобія"
            "\nУ гру можна дрочити кожен день два рази, виконавши /killru"
            "\nПри цьому кількість русофобії випадковим чином збільшиться(до +1000) або зменшиться(до -500)"
            "\nРейтинг можна подивитися в /top. і укорочене /top10, і глобальний топ"
            "серед усіх піздюків /globaltop і укорочене /globaltop10"
            "\nВ /my можна дізнатися свої кг русофобії"
            "\nПередати кг русофобії іншому можна командою /give, вказавши кількість кг + реплай"
            "\nІнформацію про бота в /about"
            "\nСлужбова інформація: /ping"
            "\nВаріанти міні ігор можна переглянути в /help, вибравши знизу емодзі, що характеризує гру"
            "\nВ /settings можна вимкнути в чаті міні ігри та передачу русофобії. Налаштування доступні "
            "тільки адмінам чату"
            "\nВийти з гри (прогрес видаляється): /leave"
            "\n\n\nЯкщо мені видати права адміна (видалення повідомлень), то я через годину буду видаляти "
            "повідомлення від мене і які мене викликали. Залишаючи тільки про зміни в русофобії"
            "\n\n\nKillru. Смерть всьому російському. 🫡",

        "game":
            f"🧌 Знайди і вбий москаля. Суть гри вгадати де знаходиться москаль на сітці 3х3"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /game",

        "dice":
            f"🎲 Гра у кості. Суть гри вгадати яке випаде число, парне чи непарне"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 10, 50, 100, 200, 300, 400, 500, 1000"
            "\n🚀 Команда гри: /dice",

        "darts":
            f"🎯 Гра в дартс. Суть гри потрапити в центр"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 10, 50, 100, 200, 300, 400, 500, 1000"
            "\n🚀 Команда гри: /darts",

        "basketball":
            f"🏀 Гра в баскетбол. Суть гри потрапити в кошик м'ячем"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 10, 50, 100, 200, 300, 400, 500, 1000"
            "\n🚀 Команда гри: /basketball",

        "football":
            f"⚽️ Гра у футбол. Суть гри потрапити м'ячем у ворота"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 1.5. Було 50 кг. При виграші зі ставкою 10, отримуєш 15. Буде 65"
            "\n💰 Ставки: 10, 50, 100, 200, 300, 400, 500, 1000"
            "\n🚀 Команда гри: /football",

        "bowling":
            f"🎳 Гра в боулінг. Суть гри вибити страйк"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 3 або на 2 (Дивлячись скільки виб'єш)"
            "\n💰 Ставки: 10, 50, 100, 200, 300, 400, 500, 1000"
            "\n🚀 Команда гри: /bowling",

        "casino":
            f"🎰 Гра в казино. Суть гри вибити джекпот"
            "\n⏱️ Можна зіграти раз на 3 години"
            "\n🔀 Приз: ставка множиться на 2, 5 або 10.Якщо вибити джекпот (777), то ставка множиться на 50"
            "\n💰 Ставки: 10, 50, 100, 200, 300, 400, 500, 1000"
            "\n🚀 Команда гри: /casino",
    }
    tb = TextBuilder()
    tb.add(game_emojis[callback_data.game])
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_help"))
    await query.message.edit_text(tb.render(), reply_markup=kb.as_markup())

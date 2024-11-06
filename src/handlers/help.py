from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.handlers.commands import commands_router
from src.types import (HelpCallback, Games)
from src.utils import TextBuilder, reply_and_delete


def get_help_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Основна гра - /killru", callback_data=HelpCallback(game=Games.KILLRU).pack()),
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
    await reply_and_delete(message, text="⚙️ Тут ти зможеш дізнатися\nпро мене все", reply_markup=kb.as_markup())


@commands_router.callback_query(F.data == "back_to_help")
async def back_to_help(query: CallbackQuery):
    kb = get_help_keyboard()
    await query.message.edit_text("⚙️ Тут ти зможеш дізнатися\nпро мене все", reply_markup=kb.as_markup())


@commands_router.callback_query(HelpCallback.filter())
async def callback_help(query: CallbackQuery, callback_data: HelpCallback):
    game_emojis = {
        "killru":
            f"Гра в русофобію"
            "\nУ гру можна зіграти кожен день один раз, виконавши /killru"
            "\nПри цьому кількість русофобії випадковим чином збільшиться(до +25) або зменшиться(до -5)"
            "\nРейтинг можна подивитися виконавши /top. Є маленький варіант /top10, і глобальний топ, показує топ "
            "серед усіх учасників /globaltop10 і маленький варіант /globaltop10"
            "\nВиконавши /my можна дізнатися свою кількість русофобії"
            "\nПередати свою русофобію іншому користувачу, можна відповівши йому командою /give, вказавши кількість "
            "русофобії"
            "\nІнформацію про бота можна подивитися, виконавши /about"
            "\nСлужбова інформація: /ping"
            "\nВаріанти міні-ігор можна переглянути за командою /help, вибравши знизу емодзі, що вказує на гру"
            "\nЗа командою /settings можна вимкнути в чаті міні-ігри та передачу русофобії. Налаштування доступні "
            "тільки адмінам чату"
            "\nВийти з гри (прогрес видаляється): /leave"
            "\n\n\nЯкщо мені видати права адміна (видалення повідомлень), то я через годину буду видаляти "
            "повідомлення від мене і які мене викликали. Залишаючи тільки про зміни в русофобії"
            "\n\n\nKillru. Смерть всьому російському. 🫡",

        "game":
            f"🧌 Знайди і вбий москаля. Суть гри вгадати де знаходиться москаль на сітці 3х3"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 1.5. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /game",

        "dice":
            f"🎲 Гра у кості. Суть гри вгадати яке випаде число, парне чи непарне"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 1.5. Було 50 кг. При виграші зі ставкою 10, отримуєш 15. Буде 65"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /dice",

        "darts":
            f"🎯 Гра в дартс. Суть гри потрапити в центр"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /darts",

        "basketball":
            f"🏀 Гра в баскетбол. Суть гри потрапити в кошик м'ячем"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 1.5. Було 50 кг. При виграші зі ставкою 10, отримуєш 15. Буде 65"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /basketball",

        "football":
            f"⚽️ Гра у футбол. Суть гри потрапити м'ячем у ворота"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 1.5. Було 50 кг. При виграші зі ставкою 10, отримуєш 15. Буде 65"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /football",

        "bowling":
            f"🎳 Гра в боулінг. Суть гри вибити страйк"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /bowling",

        "casino":
            f"🎰 Гра в казино. Суть гри вибити джекпот"
            "\n⏱️ Можна зіграти раз на 2 години"
            "\n🔀 Приз: ставка множиться на 2. Було 50 кг. При виграші зі ставкою 10, отримуєш 20. Буде 70. Якщо "
            "вибити джекпот (777), то ставка множиться на 10"
            "\n💰 Ставки: 1, 5, 10, 20, 30, 40, 50, 100"
            "\n🚀 Команда гри: /casino",
    }
    tb = TextBuilder()
    tb.add(game_emojis[callback_data.game])
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_help"))
    await query.message.edit_text(tb.render(), reply_markup=kb.as_markup())

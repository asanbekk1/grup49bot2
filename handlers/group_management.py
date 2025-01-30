import re
from datetime import timedelta
from aiogram import Router, types
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command

group_router = Router()

BANNED_WORDS = ["запрещенное_слово1", "запрещенное_слово2", "запрещенное_слово3"]

def create_banned_word_pattern(word):
    return r"\b" + re.escape(word) + r"\b"

@group_router.message()
async def check_message_for_banned_words(message: types.Message):
    text = message.text.lower() if message.text else ""

    if not text:
        return

    for word in BANNED_WORDS:
        pattern = create_banned_word_pattern(word)

        if re.search(pattern, text):
            try:
                await message.chat.ban(user_id=message.from_user.id)
                await message.reply(
                    f"Пользователь {message.from_user.username} забанен за использование запрещённого слова.",
                    parse_mode='Markdown'
                )
                break
            except TelegramAPIError as e:
                await message.reply(f"У меня нет прав для бана пользователей. Ошибка: {e}")
            except Exception as e:
                await message.reply(f"Ошибка при попытке забанить пользователя: {e}")
            break

@group_router.message(Command("ban"))
async def ban_user_with_time(message: types.Message):
    if not message.from_user.id == message.chat.id:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
            command_parts = message.text.split()
            if len(command_parts) > 1:
                time_str = command_parts[1].lower()
                time_mapping = {
                    'д': 'days',
                    'ч': 'hours',
                    'м': 'minutes',
                    'н': 'weeks'
                }

                time_period = None
                for unit, mapping in time_mapping.items():
                    if time_str.endswith(unit):
                        try:
                            amount = int(time_str[:-1])
                            time_period = timedelta(**{mapping: amount})
                            break
                        except ValueError:
                            await message.reply(f"Неправильный формат времени: {time_str}. Пример: бан 1д")
                            return

                if time_period:
                    await message.chat.ban(
                        user_id=user.id,
                        until_date=message.date + time_period
                    )
                    await message.reply(
                        f"Пользователь {user.username} забанен на {time_period}.",
                        parse_mode='HTML'
                    )
                else:
                    await message.reply("Не удалось разобрать временной период. Пример: бан 1д")
            else:
                await message.reply("Укажите время бана. Пример: бан 1д")

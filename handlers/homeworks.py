from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command


homework_router = Router()


class HomeworkForm(StatesGroup):
    name = State()
    homework_number = State()
    github_link = State()

@homework_router.message(Command("homework"))
async def start_homework(message: types.Message, state: FSMContext):
    print(message.text)
    await message.answer("Введите ваше имя:")
    await state.set_state(HomeworkForm.name)


@homework_router.message(HomeworkForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите номер домашнего задания (от 1 до 8):")
    await state.set_state(HomeworkForm.homework_number)


@homework_router.message(HomeworkForm.homework_number)
async def process_homework_number(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > 8:
        await message.answer("Пожалуйста, введите число от 1 до 8.")
        return
    await state.update_data(homework_number=message.text)
    await message.answer("Введите ссылку на GitHub:")
    await state.set_state(HomeworkForm.github_link)


@homework_router.message(HomeworkForm.github_link)
async def process_github_link(message: types.Message, state: FSMContext):
    await state.update_data(github_link=message.text)
    data = await state.get_data()
    await message.answer(f"Спасибо, {data['name']}! Ваше домашнее задание №{data['homework_number']} принято.")

    await state.clear()
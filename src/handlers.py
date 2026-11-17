from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from db.users import get_or_create_user
from db.tasks import add_task, get_tasks, task_done, get_stats

router = Router()


class AddTask(StatesGroup):
    waiting_title = State()


class DoneTask(StatesGroup):
    waiting_number = State()

@router.message(Command('start'))
async def cmd_start(message: Message):
    user = message.from_user
    get_or_create_user(user.id, user.username)
    await message.answer(
        f'Привет, {user.first_name}!\n'
        'Я помогу вести список задач.\n'
        '/add — добавить задачу\n'
        '/tasks — мои задачи\n'
        '/done — отметить задачу выполненной\n'
        '/stats — статистика'
    )

@router.message(Command('add'))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddTask.waiting_title)
    await message.answer('Введите название задачи:')


@router.message(AddTask.waiting_title)
async def process_task_title(message: Message, state: FSMContext):
    title = (message.text or '').strip()
    if not title:
        await message.answer('Название не может быть пустым. Введите название задачи:')
        return

    user = get_or_create_user(message.from_user.id, message.from_user.username)
    add_task(user['id'], title)
    await state.clear()
    await message.answer(f'Задача «{title}» добавлена :)')

@router.message(Command('tasks'))
async def cmd_tasks(message: Message):
    tasks = get_tasks(message.from_user.id)
    if not tasks:
        await message.answer('У вас пока нет задач. Добавьте первую через /add')
        return

    lines = [
        f"{'✅' if task['is_done'] else '⬜'} {task['id']}. {task['title']}"
        for task in tasks
    ]
    await message.answer('Ваши задачи:\n\n' + '\n'.join(lines))

@router.message(Command('done'))
async def cmd_done(message: Message, state: FSMContext):
    await state.set_state(DoneTask.waiting_number)
    await message.answer('Введите номер задачи, которую нужно отметить выполненной:')


@router.message(DoneTask.waiting_number)
async def process_done_number(message: Message, state: FSMContext):
    text = (message.text or '').strip()
    if not text.isdigit():
        await message.answer('Это не число! Пожалуйста, введите номер задачи цифрами:')
        return

    user = get_or_create_user(message.from_user.id, message.from_user.username)
    if task_done(int(text), user['id']):
        await message.answer(f'Задача №{text} отмечена выполненной ✅')
    else:
        await message.answer(
            'Ошибка: задача не найдена или принадлежит другому пользователю.'
        )
    await state.clear()

@router.message(Command('stats'))
async def cmd_stats(message: Message):
    user = get_or_create_user(message.from_user.id, message.from_user.username)
    stats = get_stats(user['id'])
    await message.answer(
        'Статистика:\n'
        f"Всего задач: {stats['total']}\n"
        f"Выполнено: {stats['done']}\n"
        f"Не выполнено: {stats['not_done']}"
    )
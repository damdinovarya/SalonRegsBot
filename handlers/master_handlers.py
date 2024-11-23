from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards

router = Router()


class main_state(StatesGroup):
    get_person_name = State()

from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F, types
from yclients_things import DataProcessor
from aiogram.types import FSInputFile, InputMediaPhoto
from handlers import keyboards
from database import User, Claim
from datetime import datetime
from utils import eng_to_rus

router = Router()


class ClientAdminState(StatesGroup):
    user_await = State()

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types
from yclients_things import DataProcessor
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.types import Message
from handlers import keyboards
from database import db, User, Claim
from datetime import datetime, time
from utils import rus_to_eng, eng_to_rus
import time

router = Router()

class ClientAdminState(StatesGroup):
    user_await = State()
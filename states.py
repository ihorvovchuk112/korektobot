from aiogram.fsm.state import State, StatesGroup

class CorrectionProcess(StatesGroup):
    WAITING_FOR_TEXT = State()
    CHOOSING_MODE = State()
    PROCESSING = State()
    DISPLAYING_RESULT = State()
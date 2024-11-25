from aiogram.filters.callback_data import CallbackData

class CreationOptCallback(CallbackData, prefix="СОЗДАНИЕ ОПТА"):
    channel_id: str
    step: str
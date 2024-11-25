from aiogram.filters.callback_data import CallbackData

class CreationOptCallback(CallbackData, prefix="CREATION OPT"):
    channel_id: int
    step: str
    value: str

from aiogram.filters.callback_data import CallbackData

class SetCategoryCallback(CallbackData, prefix="SET CATEGORY"):
    channel_id: int
    step: str
    value: str

class CreationOptCallback(CallbackData, prefix="CREATION OPT"):
    channel_id: int
    step: str
    value: str

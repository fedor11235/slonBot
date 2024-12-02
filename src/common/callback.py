from aiogram.filters.callback_data import CallbackData

class SetCategoryCallback(CallbackData, prefix="SET CATEGORY"):
    channel_id: int
    step: str
    value: str

class CreationOptCallback(CallbackData, prefix="CREATION OPT"):
    channel_id: int
    step: str
    value: str

class SelectDateOpt(CallbackData, prefix="SELECT DATE OPT"):
    channel_id: int
    step: str
    value: str
    page: int

class SelectTimeOpt(CallbackData, prefix="SELECT TIME OPT"):
    channel_id: int
    step: str
    value: str

class SelectCategoryIntoOptCallback(CallbackData, prefix="SELECT CATEGORY INTO OPT"):
    step: str
    value: str

class SelectDateIntoOpt(CallbackData, prefix="SELECT DATE INTO OPT"):
    channel_id: int
    step: str
    value: str
    page: int

class CreationIntoOptCallback(CallbackData, prefix="CREATION INOPT"):
    channel_id: int
    step: str
    value: str

class SelectTimeIntoOpt(CallbackData, prefix="SELECT TIME INTOPT"):
    channel_id: int
    step: str
    value: str

class SelectCategoryIntoSuggestionsCallback(CallbackData, prefix="SELECT CATEGORY INTO SUGGESTIONS"):
    step: str
    value: str

from aiogram import Router, F, types

from prisma.models import User, Opt

from common.callback import ProfileCallback

router = Router()

@router.callback_query(ProfileCallback.filter(F.step == "MY OPT"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id

@router.callback_query(ProfileCallback.filter(F.step == "RELEASE SCHEDULE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id

@router.callback_query(ProfileCallback.filter(F.step == "STATISTICS"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id

@router.callback_query(ProfileCallback.filter(F.step == "BALANCE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id
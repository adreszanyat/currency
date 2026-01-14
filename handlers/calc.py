from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import CommissionStates
from deps import get_db  # Импортируем функцию для получения db

router = Router()

@router.message(Command("calc"))
@router.message(F.text.contains("Калькулятор комиссий"))
@router.message(F.text.contains("Fee Calculator"))
async def cmd_calc(message: types.Message, state: FSMContext):
    db = get_db()  # Получаем базу данных
    
    user = await db.get_user(message.from_user.id)
    lang = user[1] if user else 'ru'
    
    await state.set_state(CommissionStates.waiting_for_amount)
    
    if lang == 'ru':
        text = "🧮 *Калькулятор комиссий*\n\nВведите сумму для обмена:"
    else:
        text = "🧮 *Fee Calculator*\n\nEnter the amount to exchange:"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(CommissionStates.waiting_for_amount)
async def process_calc_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))
        await state.update_data(amount=amount)
        await state.set_state(CommissionStates.waiting_for_rate)
        
        await message.answer("Введите курс обмена (сколько дают за 1 единицу валюты):")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число")

@router.message(CommissionStates.waiting_for_rate)
async def process_calc_rate(message: types.Message, state: FSMContext):
    try:
        rate = float(message.text.replace(',', '.'))
        await state.update_data(rate=rate)
        await state.set_state(CommissionStates.waiting_for_commission)
        
        await message.answer("Введите комиссию в процентах (например, 1.5):")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число")

@router.message(CommissionStates.waiting_for_commission)
async def process_calc_commission(message: types.Message, state: FSMContext):
    db = get_db()  # Получаем базу данных
    
    try:
        commission = float(message.text.replace(',', '.'))
        data = await state.get_data()
        amount = data.get('amount')
        rate = data.get('rate')
        
        # Расчет
        without_commission = amount * rate
        commission_amount = without_commission * (commission / 100)
        result = without_commission - commission_amount
        
        user = await db.get_user(message.from_user.id)
        lang = user[1] if user else 'ru'
        
        if lang == 'ru':
            text = (
                f"🧮 *Результат расчета:*\n\n"
                f"💵 Исходная сумма: {amount:.2f}\n"
                f"📊 Курс обмена: {rate:.2f}\n"
                f"💸 Комиссия: {commission}%\n\n"
                f"💰 Без комиссии: {without_commission:.2f}\n"
                f"📉 Комиссия: {commission_amount:.2f}\n"
                f"✅ На руки: *{result:.2f}*"
            )
        else:
            text = (
                f"🧮 *Calculation Result:*\n\n"
                f"💵 Initial amount: {amount:.2f}\n"
                f"📊 Exchange rate: {rate:.2f}\n"
                f"💸 Commission: {commission}%\n\n"
                f"💰 Without commission: {without_commission:.2f}\n"
                f"📉 Commission amount: {commission_amount:.2f}\n"
                f"✅ To receive: *{result:.2f}*"
            )
        
        await message.answer(text, parse_mode="Markdown")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число")
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import Database
from states import TipsStates

router = Router()

@router.message(Command("tips"))
@router.message(F.text.contains("Чаевые"))
@router.message(F.text.contains("Tips"))
async def cmd_tips(message: types.Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    lang = user[1] if user else 'ru'
    
    await state.set_state(TipsStates.waiting_for_bill)
    
    if lang == 'ru':
        text = "💸 *Калькулятор чаевых*\n\nВведите общую сумму счета:"
    else:
        text = "💸 *Tips Calculator*\n\nEnter the total bill amount:"
    
    await message.answer(text, parse_mode="Markdown")

@router.message(TipsStates.waiting_for_bill)
async def process_tips_bill(message: types.Message, state: FSMContext):
    try:
        bill = float(message.text.replace(',', '.'))
        await state.update_data(bill=bill)
        await state.set_state(TipsStates.waiting_for_people)
        
        await message.answer("На сколько человек разделить счет?")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число")

@router.message(TipsStates.waiting_for_people)
async def process_tips_people(message: types.Message, state: FSMContext):
    try:
        people = int(message.text)
        await state.update_data(people=people)
        await state.set_state(TipsStates.waiting_for_tip)
        
        await message.answer("Сколько процентов чаевых оставить? (например: 10)")
    except ValueError:
        await message.answer("Пожалуйста, введите целое число")

@router.message(TipsStates.waiting_for_tip)
async def process_tips_percent(message: types.Message, state: FSMContext, db: Database):
    try:
        tip_percent = float(message.text.replace(',', '.'))
        data = await state.get_data()
        bill = data.get('bill')
        people = data.get('people')
        
        # Расчет
        tip_amount = bill * (tip_percent / 100)
        total_with_tip = bill + tip_amount
        per_person = total_with_tip / people if people > 0 else total_with_tip
        
        user = await db.get_user(message.from_user.id)
        lang = user[1] if user else 'ru'
        
        if lang == 'ru':
            text = (
                f"💸 *Результат расчета:*\n\n"
                f"🍽️ Сумма счета: {bill:.2f}\n"
                f"👥 Количество человек: {people}\n"
                f"💵 Чаевые: {tip_percent}%\n\n"
                f"💰 Сумма чаевых: {tip_amount:.2f}\n"
                f"📊 Итого к оплате: {total_with_tip:.2f}\n"
                f"👤 С каждого: *{per_person:.2f}*"
            )
        else:
            text = (
                f"💸 *Calculation Result:*\n\n"
                f"🍽️ Bill amount: {bill:.2f}\n"
                f"👥 Number of people: {people}\n"
                f"💵 Tips: {tip_percent}%\n\n"
                f"💰 Tips amount: {tip_amount:.2f}\n"
                f"📊 Total to pay: {total_with_tip:.2f}\n"
                f"👤 Per person: *{per_person:.2f}*"
            )
        
        await message.answer(text, parse_mode="Markdown")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число")
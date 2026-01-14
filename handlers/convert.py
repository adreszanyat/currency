from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import get_currency_keyboard
from utils import convert_currency
from states import ConvertStates
from deps import get_db  # Импортируем из deps.py

router = Router()

@router.message(Command("convert"))
@router.message(F.text.contains("Конвертировать"))
@router.message(F.text.contains("Convert"))
async def cmd_convert(message: types.Message, state: FSMContext):
    db = get_db()  # Получаем базу данных
    
    user = await db.get_user(message.from_user.id)
    lang = user[1] if user else 'ru'
    
    await state.set_state(ConvertStates.waiting_for_from_currency)
    
    if lang == 'ru':
        text = "Выберите исходную валюту:"
    else:
        text = "Select source currency:"
    
    await message.answer(
        text,
        reply_markup=get_currency_keyboard(action="convert_from")
    )

@router.callback_query(F.data.startswith("convert_from"))
async def process_from_currency(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split(":")[1]
    await state.update_data(from_currency=currency)
    
    await state.set_state(ConvertStates.waiting_for_to_currency)
    await callback.message.edit_text(
        f"Выбрана валюта: {currency}\nТеперь выберите целевую валюту:",
        reply_markup=get_currency_keyboard(action="convert_to")
    )
    await callback.answer()

@router.callback_query(F.data.startswith("convert_to"))
async def process_to_currency(callback: types.CallbackQuery, state: FSMContext):
    db = get_db()  # Получаем базу данных
    
    to_currency = callback.data.split(":")[1]
    data = await state.get_data()
    from_currency = data.get('from_currency')
    
    await state.update_data(to_currency=to_currency)
    await state.set_state(ConvertStates.waiting_for_amount)
    
    user = await db.get_user(callback.from_user.id)
    lang = user[1] if user else 'ru'
    
    if lang == 'ru':
        text = f"Конвертация: {from_currency} → {to_currency}\nВведите сумму для конвертации:"
    else:
        text = f"Conversion: {from_currency} → {to_currency}\nEnter amount to convert:"
    
    await callback.message.edit_text(text)
    await callback.answer()

@router.message(ConvertStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    db = get_db()  # Получаем базу данных
    
    try:
        amount = float(message.text.replace(',', '.'))
        data = await state.get_data()
        from_currency = data.get('from_currency')
        to_currency = data.get('to_currency')
        
        result, rate = await convert_currency(amount, from_currency, to_currency)
        
        if result and rate:
            # Сохраняем в историю
            await db.add_to_history(
                message.from_user.id,
                from_currency,
                to_currency,
                amount,
                result,
                rate
            )
            
            user = await db.get_user(message.from_user.id)
            lang = user[1] if user else 'ru'
            
            if lang == 'ru':
                text = (
                    f"✅ *Результат конвертации*\n\n"
                    f"💵 Сумма: {amount:.2f} {from_currency}\n"
                    f"📊 Курс: 1 {from_currency} = {rate:.4f} {to_currency}\n"
                    f"💰 Итого: {result:.2f} {to_currency}\n\n"
                    f"💾 Операция сохранена в историю"
                )
            else:
                text = (
                    f"✅ *Conversion Result*\n\n"
                    f"💵 Amount: {amount:.2f} {from_currency}\n"
                    f"📊 Rate: 1 {from_currency} = {rate:.4f} {to_currency}\n"
                    f"💰 Total: {result:.2f} {to_currency}\n\n"
                    f"💾 Operation saved to history"
                )
            
            await message.answer(text, parse_mode="Markdown")
            await state.clear()
        else:
            if lang == 'ru':
                await message.answer("Ошибка получения курса. Попробуйте позже.")
            else:
                await message.answer("Error getting exchange rate. Try again later.")
    except ValueError:
        if lang == 'ru':
            await message.answer("Пожалуйста, введите корректное число")
        else:
            await message.answer("Please enter a valid number")
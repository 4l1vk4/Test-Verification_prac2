from typing import Dict

def calculate_compound_interest(principal: float, rate: float, years: int, compounds_per_year: int = 1) -> float:
    if principal < 0:
        raise ValueError("Начальный капитал не может быть отрицательным.")
    if rate < 0:
        raise ValueError("Процентная ставка не может быть отрицательной.")
    if years < 0:
        raise ValueError("Срок в годах не может быть отрицательным.")
    if compounds_per_year <= 0:
        raise ValueError("Частота начисления процентов должна быть строго положительной.")
    
    amount = principal * ((1.0 + rate / compounds_per_year) ** (compounds_per_year * years))
    return round(amount, 2)


def calculate_loan_payment(principal: float, annual_rate: float, months: int) -> float:
    if principal <= 0:
        raise ValueError("Сумма кредита должна быть строго больше нуля.")
    if annual_rate < 0:
        raise ValueError("Процентная ставка не может быть отрицательной.")
    if months <= 0:
        raise ValueError("Срок кредита должен быть строго больше нуля месяцев.")
    
    if annual_rate == 0.0:
        return round(principal / months, 2)
    
    monthly_rate = annual_rate / 12.0
    payment = principal * (monthly_rate * ((1.0 + monthly_rate) ** months)) / (((1.0 + monthly_rate) ** months) - 1.0)
    return round(payment, 2)


def deposit_funds(balance: float, amount: float, bonus_rate: float = 0.0) -> float:
    if balance < 0:
        raise ValueError("Текущий баланс не может быть отрицательным.")
    if amount <= 0:
        raise ValueError("Сумма пополнения должна быть больше нуля.")
    if not (0.0 <= bonus_rate <= 1.0):
        raise ValueError("Бонусная ставка должна быть в диапазоне от 0.0 до 1.0.")
    
    bonus = amount * bonus_rate
    new_balance = balance + amount + bonus
    return round(new_balance, 2)


def withdraw_funds(balance: float, amount: float, fee: float = 0.0) -> float:
    if balance < 0:
        raise ValueError("Баланс счета не может быть отрицательным.")
    if amount <= 0:
        raise ValueError("Сумма снятия должна быть положительной.")
    if fee < 0:
        raise ValueError("Комиссия не может быть отрицательной.")
    
    if balance < amount:
        raise ValueError("Недостаточно средств на счете для совершения операции с учетом комиссии.")
    
    new_balance = balance - amount + fee
    return round(new_balance, 2)


def convert_currency(amount: float, from_curr: str, to_curr: str, rates: Dict[str, float]) -> float:
    if amount < 0:
        raise ValueError("Сумма для конвертации не может быть отрицательной.")
    if from_curr not in rates:
        raise KeyError(f"Неизвестная исходная валюта: {from_curr}")
    if to_curr not in rates:
        raise KeyError(f"Неизвестная целевая валюта: {to_curr}")
    if rates[from_curr] <= 0 or rates[to_curr] <= 0:
        raise ValueError("Курс валюты должен быть строго положительным.")
    
    base_val = amount / rates[from_curr]
    converted = base_val * rates[to_curr]
    return round(converted, 2)

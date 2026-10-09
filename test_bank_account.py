import unittest
import sys
import os
class TestBankAccount(unittest.TestCase):

    def setUp(self):
        import bank_account_bugs
        self.mod = bank_account_bugs
        self.rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "RUB": 95.5,
            "CNY": 7.2
        }

    # --- 1. calculate_compound_interest ---
    def test_compound_interest_basic(self):
        # 1000 под 5% на 2 года с начислением раз в год: 1000 * 1.05^2 = 1102.50
        res = self.mod.calculate_compound_interest(1000.0, 0.05, 2, 1)
        self.assertEqual(res, 1102.50)

    def test_compound_interest_quarterly(self):
        # 5000 под 6% на 3 года ежеквартально (n=4): 5000 * (1 + 0.06/4)^(12) = 5978.09
        res = self.mod.calculate_compound_interest(5000.0, 0.06, 3, 4)
        self.assertEqual(res, 5978.09)

    def test_compound_interest_zero_rate(self):
        res = self.mod.calculate_compound_interest(1000.0, 0.0, 5, 1)
        self.assertEqual(res, 1000.0)

    def test_compound_interest_invalid_params(self):
        with self.assertRaises(ValueError):
            self.mod.calculate_compound_interest(-100.0, 0.05, 2, 1)
        with self.assertRaises(ValueError):
            self.mod.calculate_compound_interest(1000.0, -0.05, 2, 1)
        with self.assertRaises(ValueError):
            self.mod.calculate_compound_interest(1000.0, 0.05, -1, 1)
        with self.assertRaises(ValueError):
            self.mod.calculate_compound_interest(1000.0, 0.05, 2, 0)

    # --- 2. calculate_loan_payment ---
    def test_loan_payment_standard(self):
        # Кредит 100000 под 12% годовых на 12 месяцев (1 год): платеж ~ 8884.88
        pmt = self.mod.calculate_loan_payment(100000.0, 0.12, 12)
        self.assertEqual(pmt, 8884.88)

    def test_loan_payment_zero_interest(self):
        # Беспроцентная рассрочка 120000 на 12 месяцев: 10000 в месяц
        pmt = self.mod.calculate_loan_payment(120000.0, 0.0, 12)
        self.assertEqual(pmt, 10000.0)

    def test_loan_payment_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.mod.calculate_loan_payment(0, 0.10, 12)
        with self.assertRaises(ValueError):
            self.mod.calculate_loan_payment(10000, -0.01, 12)
        with self.assertRaises(ValueError):
            self.mod.calculate_loan_payment(10000, 0.10, 0)

    # --- 3. deposit_funds ---
    def test_deposit_simple(self):
        bal = self.mod.deposit_funds(1000.0, 500.0, 0.0)
        self.assertEqual(bal, 1500.0)

    def test_deposit_with_bonus(self):
        # 1000 + 500 + 500 * 0.10 = 1550.0
        bal = self.mod.deposit_funds(1000.0, 500.0, 0.10)
        self.assertEqual(bal, 1550.0)

    def test_deposit_invalid_values(self):
        with self.assertRaises(ValueError):
            self.mod.deposit_funds(-50.0, 100.0, 0.0)
        with self.assertRaises(ValueError):
            self.mod.deposit_funds(100.0, 0.0, 0.0)
        with self.assertRaises(ValueError):
            self.mod.deposit_funds(100.0, 50.0, 1.5)

    # --- 4. withdraw_funds ---
    def test_withdraw_standard(self):
        # 1000 - 300 = 700
        bal = self.mod.withdraw_funds(1000.0, 300.0, 0.0)
        self.assertEqual(bal, 700.0)

    def test_withdraw_with_fee(self):
        # 1000 - (300 + 20) = 680.0
        bal = self.mod.withdraw_funds(1000.0, 300.0, 20.0)
        self.assertEqual(bal, 680.0)

    def test_withdraw_exact_funds(self):
        # 500 - (480 + 20) = 0.0
        bal = self.mod.withdraw_funds(500.0, 480.0, 20.0)
        self.assertEqual(bal, 0.0)

    def test_withdraw_insufficient_funds_with_fee(self):
        # Баланс 100, снятие 95, комиссия 10. Требуется 105 > 100 -> исключение
        with self.assertRaises(ValueError):
            self.mod.withdraw_funds(100.0, 95.0, 10.0)

    def test_withdraw_negative_fee_or_amount(self):
        with self.assertRaises(ValueError):
            self.mod.withdraw_funds(100.0, -20.0, 0.0)
        with self.assertRaises(ValueError):
            self.mod.withdraw_funds(100.0, 20.0, -5.0)

    # --- 5. convert_currency ---
    def test_convert_same_currency(self):
        res = self.mod.convert_currency(100.0, "USD", "USD", self.rates)
        self.assertEqual(res, 100.0)

    def test_convert_usd_to_rub(self):
        res = self.mod.convert_currency(10.0, "USD", "RUB", self.rates)
        self.assertEqual(res, 955.0)

    def test_convert_unknown_currency(self):
        with self.assertRaises(KeyError):
            self.mod.convert_currency(100.0, "GBP", "USD", self.rates)

    def test_convert_invalid_amount_or_rates(self):
        with self.assertRaises(ValueError):
            self.mod.convert_currency(-50.0, "USD", "RUB", self.rates)
        bad_rates = {"USD": 1.0, "RUB": -10.0}
        with self.assertRaises(ValueError):
            self.mod.convert_currency(100.0, "USD", "RUB", bad_rates)

if __name__ == '__main__':
    unittest.main()

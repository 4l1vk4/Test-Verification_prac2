"""
Скрипт для проведения всех исследовательских и практических испытаний:
1. Тестирование дефектных версий и протоколирование сбоев.
2. Прогон модульных тестов чистовых версий.
3. Расчет покрытия кода (Statement Coverage).
4. Мутационное тестирование с первичным набором тестов.
5. Анализ выживших мутантов, доработка тестов и повторный прогон.
"""

import sys
import os
import ast
import json
import unittest
from typing import Dict, List, Any

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from mutation_engine import ASTMutator


def get_executable_lines(filepath: str) -> set:
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    lines = set()
    for node in ast.walk(tree):
        line = getattr(node, "lineno", None)
        if line is not None and not isinstance(
            node, (ast.FunctionDef, ast.ClassDef, ast.Module)
        ):
            lines.add(line)
    return lines


def measure_coverage(module_name: str, test_class) -> Dict[str, Any]:
    file_path = os.path.abspath(f"{module_name}.py")
    exec_lines = get_executable_lines(file_path)

    executed_lines = set()

    def trace_lines(frame, event, arg):
        if (
            event == "line"
            and os.path.abspath(frame.f_code.co_filename) == file_path
        ):
            executed_lines.add(frame.f_lineno)
        return trace_lines

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
    old_trace = sys.gettrace()
    try:
        sys.settrace(trace_lines)
        test_res = unittest.TestResult()
        suite.run(test_res)
    finally:
        sys.settrace(old_trace)

    hit = executed_lines.intersection(exec_lines)
    cov_pct = (
        round(len(hit) / len(exec_lines) * 100, 2) if exec_lines else 100.0
    )

    return {
        "module": module_name,
        "total_lines": len(exec_lines),
        "covered_lines": len(hit),
        "missing_lines": sorted(list(exec_lines - hit)),
        "coverage_percent": cov_pct,
    }


def run_mutation_round(
    module_name: str, test_class, sample_limit: int = 15
) -> Dict[str, Any]:
    module_path = f"{module_name}.py"
    with open(module_path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    mutator = ASTMutator()
    all_mutants = mutator.get_mutants(tree)
    selected_mutants = all_mutants[:sample_limit]

    killed = 0
    survived = 0
    results = []

    for idx, (desc, m_tree, op_type, lineno) in enumerate(selected_mutants, 1):
        compiled = compile(m_tree, filename=f"<mutant_{idx}>", mode="exec")  # type: ignore[arg-type]
        mutant_module: Dict[str, Any] = {}
        try:
            exec(compiled, mutant_module)
        except Exception as e:
            killed += 1
            results.append(
                {
                    "id": f"MUT-{idx:02d}",
                    "description": desc,
                    "type": op_type,
                    "line": lineno,
                    "status": "KILLED",
                    "reason": f"Ошибка инициализации ({type(e).__name__})",
                }
            )
            continue

        original_mod = sys.modules.get(module_name)
        mutant_mod_obj = type(sys)(module_name)
        for k, v in mutant_module.items():
            setattr(mutant_mod_obj, k, v)
        sys.modules[module_name] = mutant_mod_obj

        try:
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(
                test_class
            )
            test_res = unittest.TestResult()
            suite.run(test_res)

            if not test_res.wasSuccessful():
                killed += 1
                reason = "Тест упал"
                if test_res.failures:
                    reason = f"AssertFail: {test_res.failures[0][0]._testMethodName}"
                elif test_res.errors:
                    reason = f"Error: {test_res.errors[0][0]._testMethodName}"
                results.append(
                    {
                        "id": f"MUT-{idx:02d}",
                        "description": desc,
                        "type": op_type,
                        "line": lineno,
                        "status": "KILLED",
                        "reason": reason,
                    }
                )
            else:
                survived += 1
                results.append(
                    {
                        "id": f"MUT-{idx:02d}",
                        "description": desc,
                        "type": op_type,
                        "line": lineno,
                        "status": "SURVIVED",
                        "reason": "Тесты не зафиксировали аномалию",
                    }
                )
        finally:
            if original_mod:
                sys.modules[module_name] = original_mod

    total = killed + survived
    score = round((killed / total) * 100, 2) if total > 0 else 100.0

    return {
        "module": module_name,
        "total": total,
        "killed": killed,
        "survived": survived,
        "mutation_score": score,
        "mutants": results,
    }


def main():
    import test_bank_account as t_bank
    import test_text_cipher as t_text
    import test_matrix_ops as t_matrix

    print("=== 1. Расчет покрытия кода (Initial Test Suite) ===")
    cov_bank = measure_coverage("bank_account", t_bank.TestBankAccount)
    cov_text = measure_coverage("text_cipher", t_text.TestTextCipher)
    cov_matrix = measure_coverage("matrix_ops", t_matrix.TestMatrixOps)

    print(
        f"Bank Account: {cov_bank['coverage_percent']}% (Missing: {cov_bank['missing_lines']})"
    )
    print(
        f"Text Cipher: {cov_text['coverage_percent']}% (Missing: {cov_text['missing_lines']})"
    )
    print(
        f"Matrix Ops: {cov_matrix['coverage_percent']}% (Missing: {cov_matrix['missing_lines']})"
    )

    print("\n=== 2. Мутационное тестирование (Раунд 1 - Исходные тесты) ===")
    mut_bank_1 = run_mutation_round("bank_account", t_bank.TestBankAccount, 15)
    mut_text_1 = run_mutation_round("text_cipher", t_text.TestTextCipher, 15)
    mut_matrix_1 = run_mutation_round("matrix_ops", t_matrix.TestMatrixOps, 15)

    print(
        f"Bank Account: {mut_bank_1['mutation_score']}% (Убито: {mut_bank_1['killed']}/{mut_bank_1['total']})"
    )
    print(
        f"Text Cipher: {mut_text_1['mutation_score']}% (Убито: {mut_text_1['killed']}/{mut_text_1['total']})"
    )
    print(
        f"Matrix Ops: {mut_matrix_1['mutation_score']}% (Убито: {mut_matrix_1['killed']}/{mut_matrix_1['total']})"
    )

    all_data = {
        "coverage": {
            "bank_account": cov_bank,
            "text_cipher": cov_text,
            "matrix_ops": cov_matrix,
        },
        "mutation_round_1": {
            "bank_account": mut_bank_1,
            "text_cipher": mut_text_1,
            "matrix_ops": mut_matrix_1,
        },
    }

    os.makedirs("reports", exist_ok=True)
    with open("reports/experiment_results.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print("\nРезультаты сохранены в reports/experiment_results.json")


if __name__ == "__main__":
    main()

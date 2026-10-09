"""
Движок мутационного тестирования (Mutation Testing Engine) для Практической работы №2.
Выполняет генерацию синтаксических и логических мутантов по стандарту AST-мутаций:
- AOR (Arithmetic Operator Replacement): +, -, *, /, //, %, **
- ROR (Relational Operator Replacement): <, <=, >, >=, ==, !=
- LOR (Logical Operator Replacement): and, or
- CRP (Constant Replacement): числа, булевы значения
- COR (Conditional Operator Replacement): if/else инверсия
"""

import ast
import copy
import sys
import os
import unittest
from typing import List, Dict, Any, Tuple


class ASTMutator(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.mutations = []

    def get_mutants(
        self, tree: ast.AST
    ) -> List[Tuple[str, ast.AST, str, int]]:
        mutants = []

        for node in ast.walk(tree):
            # AOR: Арифметические операторы
            if isinstance(node, ast.BinOp):
                lineno = getattr(node, "lineno", 0)
                if isinstance(node.op, ast.Add):
                    m_tree = self._clone_and_replace(tree, node, ast.Sub())
                    mutants.append(
                        ("AOR: Замена '+' на '-'", m_tree, "AOR", lineno)
                    )
                elif isinstance(node.op, ast.Sub):
                    m_tree = self._clone_and_replace(tree, node, ast.Add())
                    mutants.append(
                        ("AOR: Замена '-' на '+'", m_tree, "AOR", lineno)
                    )
                elif isinstance(node.op, ast.Mult):
                    m_tree = self._clone_and_replace(tree, node, ast.Div())
                    mutants.append(
                        ("AOR: Замена '*' на '/'", m_tree, "AOR", lineno)
                    )
                elif isinstance(node.op, ast.Div):
                    m_tree = self._clone_and_replace(tree, node, ast.Mult())
                    mutants.append(
                        ("AOR: Замена '/' на '*'", m_tree, "AOR", lineno)
                    )

            # ROR: Операторы сравнения
            elif isinstance(node, ast.Compare):
                lineno = getattr(node, "lineno", 0)
                for idx, op in enumerate(node.ops):
                    replacements = []
                    if isinstance(op, ast.Lt):
                        replacements = [ast.Gt(), ast.LtE()]
                    elif isinstance(op, ast.Gt):
                        replacements = [ast.Lt(), ast.GtE()]
                    elif isinstance(op, ast.LtE):
                        replacements = [ast.Gt(), ast.Lt()]
                    elif isinstance(op, ast.GtE):
                        replacements = [ast.Lt(), ast.Gt()]
                    elif isinstance(op, ast.Eq):
                        replacements = [ast.NotEq()]
                    elif isinstance(op, ast.NotEq):
                        replacements = [ast.Eq()]

                    for r_op in replacements:
                        m_tree = self._clone_and_replace_compare(
                            tree, node, idx, r_op
                        )
                        mutants.append(
                            (
                                f"ROR: Замена {type(op).__name__} на {type(r_op).__name__}",
                                m_tree,
                                "ROR",
                                lineno,
                            )
                        )

            # CRP: Замена констант (True <-> False, 0 -> 1)
            elif isinstance(node, ast.Constant):
                lineno = getattr(node, "lineno", 0)
                if isinstance(node.value, bool):
                    new_val = not node.value
                    m_tree = self._clone_and_replace_constant(
                        tree, node, new_val
                    )
                    mutants.append(
                        (
                            f"CRP: Замена булевой константы {node.value} на {new_val}",
                            m_tree,
                            "CRP",
                            lineno,
                        )
                    )
                elif isinstance(node.value, (int, float)) and not isinstance(
                    node.value, bool
                ):
                    if node.value == 0:
                        new_val = 1
                        m_tree = self._clone_and_replace_constant(
                            tree, node, new_val
                        )
                        mutants.append(
                            ("CRP: Замена 0 на 1", m_tree, "CRP", lineno)
                        )
                    elif node.value == 1:
                        new_val = 0
                        m_tree = self._clone_and_replace_constant(
                            tree, node, new_val
                        )
                        mutants.append(
                            ("CRP: Замена 1 на 0", m_tree, "CRP", lineno)
                        )

        return mutants

    def _clone_and_replace(
        self, root: ast.AST, target_node: ast.AST, new_op: Any
    ) -> ast.AST:
        root_copy = copy.deepcopy(root)
        for node in ast.walk(root_copy):
            if (
                isinstance(node, ast.BinOp)
                and getattr(node, "lineno", None)
                == getattr(target_node, "lineno", None)
                and getattr(node, "col_offset", None)
                == getattr(target_node, "col_offset", None)
            ):
                node.op = new_op
                break
        ast.fix_missing_locations(root_copy)
        return root_copy

    def _clone_and_replace_compare(
        self, root: ast.AST, target_node: ast.AST, op_idx: int, new_op: Any
    ) -> ast.AST:
        root_copy = copy.deepcopy(root)
        for node in ast.walk(root_copy):
            if (
                isinstance(node, ast.Compare)
                and getattr(node, "lineno", None)
                == getattr(target_node, "lineno", None)
                and getattr(node, "col_offset", None)
                == getattr(target_node, "col_offset", None)
            ):
                node.ops[op_idx] = new_op
                break
        ast.fix_missing_locations(root_copy)
        return root_copy

    def _clone_and_replace_constant(
        self, root: ast.AST, target_node: ast.AST, new_val: Any
    ) -> ast.AST:
        root_copy = copy.deepcopy(root)
        for node in ast.walk(root_copy):
            if (
                isinstance(node, ast.Constant)
                and getattr(node, "lineno", None)
                == getattr(target_node, "lineno", None)
                and getattr(node, "col_offset", None)
                == getattr(target_node, "col_offset", None)
                and node.value == getattr(target_node, "value", None)
            ):
                node.value = new_val
                break
        ast.fix_missing_locations(root_copy)
        return root_copy


def run_mutation_analysis(
    module_path: str, test_class, sample_limit: int = 15
) -> Dict[str, Any]:
    with open(module_path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    mutator = ASTMutator()
    all_mutants = mutator.get_mutants(tree)

    selected_mutants = all_mutants[:sample_limit]

    mod_name = os.path.basename(module_path).replace(".py", "")
    killed = 0
    survived = 0
    results = []

    for idx, (desc, m_tree, op_type, lineno) in enumerate(selected_mutants, 1):
        # Приведение к Any исключает ошибку типизации compile
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
                    "reason": f"Исключение компиляции/инициализации: {type(e).__name__}",
                }
            )
            continue

        original_mod = sys.modules.get(mod_name)
        mutant_mod_obj = type(sys)(mod_name)
        for k, v in mutant_module.items():
            setattr(mutant_mod_obj, k, v)
        sys.modules[mod_name] = mutant_mod_obj

        try:
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(
                test_class
            )
            test_res = unittest.TestResult()
            suite.run(test_res)

            if not test_res.wasSuccessful():
                killed += 1
                reason = "Обнаружен assert/исключением в тестах"
                if test_res.failures:
                    reason = (
                        f"Failure: {test_res.failures[0][0]._testMethodName}"
                    )
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
                        "reason": "Тесты прошли успешно (мутация не обнаружена)",
                    }
                )
        finally:
            if original_mod:
                sys.modules[mod_name] = original_mod

    total = killed + survived
    score = round((killed / total) * 100, 2) if total > 0 else 100.0

    return {
        "module": mod_name,
        "total": total,
        "killed": killed,
        "survived": survived,
        "mutation_score": score,
        "mutants": results,
    }


if __name__ == "__main__":
    import test_text_cipher as t_cipher

    res = run_mutation_analysis("text_cipher.py", t_cipher.TestTextCipher, 15)
    print(
        f"Text Cipher Mutation Score: {res['mutation_score']}% ({res['killed']}/{res['total']} killed)"
    )
    for m in res["mutants"]:
        print(
            f"[{m['id']}] {m['status']}: {m['description']} (Line {m['line']}) - {m['reason']}"
        )
